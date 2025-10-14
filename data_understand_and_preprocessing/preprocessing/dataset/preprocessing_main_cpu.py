import os
import subprocess
import multiprocessing
import numpy as np
INPUT_FOLDERS = ['non_violence', 'violence']
OUTPUT_FOLDERS = ['non_violence_output', 'violence_output']
MIN_DIMENSION = 128
TARGET_FPS = 12
TARGET_SIZE = 256
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
GPU_TYPE = 'NVIDIA' 
NUM_PROCESSES = multiprocessing.cpu_count() 
def get_video_dimensions(video_path):
    try:
        command = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', video_path
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        width, height = map(int, result.stdout.strip().split('x'))
        return width, height
    except Exception:
        return None, None
def build_ffmpeg_command(input_path, gpu_type):
    hwaccel_options = []
    if gpu_type == 'NVIDIA':
        hwaccel_options = ['-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda']
    elif gpu_type == 'INTEL':
        hwaccel_options = ['-hwaccel', 'qsv', '-c:v', 'h264_qsv']
    elif gpu_type == 'AMD':
        hwaccel_options = ['-hwaccel', 'dxva2']
    video_filters = f'scale={TARGET_SIZE}:{TARGET_SIZE}:force_original_aspect_ratio=decrease,pad={TARGET_SIZE}:{TARGET_SIZE}:(ow-iw)/2:(oh-ih)/2:color=black,fps={TARGET_FPS}'
    command = ['ffmpeg'] + hwaccel_options + [
        '-i', input_path,
        '-vf', video_filters,
        '-f', 'rawvideo',
        '-pix_fmt', 'rgb24',
        '-an',
        'pipe:1'
    ]
    return command
def run_conversion(input_path, output_path, gpu_type):
    command = build_ffmpeg_command(input_path, gpu_type)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_bytes, err_bytes = proc.communicate()
    return proc.returncode, out_bytes, err_bytes

def process_single_video(task_info):
    input_path, output_path, gpu_type = task_info
    filename = os.path.basename(input_path)
    
    width, height = get_video_dimensions(input_path)
    if width is None or height is None:
        return f"SKIPPED (file read error): '{filename}'"
    if width < MIN_DIMENSION or height < MIN_DIMENSION:
        return f"SKIPPED (too small): '{filename}' ({width}x{height})px"

    try:
        returncode, out_bytes, err_bytes = run_conversion(input_path, output_path, gpu_type)

        if returncode != 0:
            err_str = err_bytes.decode('utf-8', errors='ignore')
            if "Cannot load nvcuda.dll" in err_str or "No device available for decoder" in err_str:
                returncode, out_bytes, err_bytes = run_conversion(input_path, output_path, 'CPU')
                if returncode == 0:
                    pass
                else:
                    return f"FAILED (CPU fallback also failed): '{filename}'"
            else:
                return f"FAILED (ffmpeg error): '{filename}'. Details: {err_str.strip()}"

        frame_size = TARGET_SIZE * TARGET_SIZE * 3
        if not out_bytes or len(out_bytes) % frame_size != 0:
             return f"FAILED (corrupted output stream): '{filename}'"

        tensor = np.frombuffer(out_bytes, dtype=np.uint8)
        tensor = tensor.reshape(-1, TARGET_SIZE, TARGET_SIZE, 3)
        tensor = tensor.astype(np.float32) / 255.0
        
        np.save(output_path, tensor)
        
        # Determine if GPU was used for the success message
        used_mode = gpu_type if "Cannot load nvcuda.dll" not in err_bytes.decode('utf-8', errors='ignore') else 'CPU_fallback'
        return f"SUCCESS ({used_mode}): '{filename}' -> '{os.path.basename(output_path)}' | Shape: {tensor.shape}"

    except Exception as e:
        return f"FAILED (Python error): '{filename}' | Details: {str(e)}"

def main():
    all_tasks = []
    for i, input_folder in enumerate(INPUT_FOLDERS):
        output_folder = OUTPUT_FOLDERS[i]
        if not os.path.isdir(input_folder):
            print(f"WARNING: Input folder '{input_folder}' does not exist.")
            continue
            
        os.makedirs(output_folder, exist_ok=True)
        
        video_files = [f for f in os.listdir(input_folder) if f.lower().endswith(VIDEO_EXTENSIONS)]
        
        file_counter = 1
        for filename in video_files:
            input_path = os.path.join(input_folder, filename)
            output_filename = f"{file_counter}.npy"
            output_path = os.path.join(output_folder, output_filename)
            all_tasks.append((input_path, output_path, GPU_TYPE))
            file_counter += 1
    
    if not all_tasks:
        print("No videos found to process.")
        return

    print(f"\n>>> Found {len(all_tasks)} videos. Starting tensor conversion with {NUM_PROCESSES} workers and GPU ({GPU_TYPE})...")
    with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
        for result in pool.imap_unordered(process_single_video, all_tasks):
            print(result)

    print("\n--- ALL TASKS COMPLETED! ---")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
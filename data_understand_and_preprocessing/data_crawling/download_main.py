import os
import subprocess

INPUT_FILE = 'result.dat'
OUTPUT_DIR = 'output'
ARCHIVE_FILE = 'download_archive.txt'

def download_videos():
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        print(f"Directory '{OUTPUT_DIR}' is ready.")
    except OSError as e:
        print(f"Error creating directory {OUTPUT_DIR}: {e}")
        return

    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        return

    print(f"Reading URLs from '{INPUT_FILE}'...")
    with open(INPUT_FILE, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        print("No URLs found in the input file.")
        return
        
    print(f"Found {len(urls)} URLs. Starting download process...")

    for index, url in enumerate(urls):
        print("\n" + "="*50)
        print(f"Downloading video {index + 1}/{len(urls)}: {url}")
        print("="*50)
        
        command = [
            'yt-dlp',
            '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            '--output', f'{OUTPUT_DIR}/%(title)s [%(id)s].%(ext)s',
            '--download-archive', ARCHIVE_FILE,
            '--no-overwrites',
            '--ignore-errors',
        ]
        
        command.append(url)

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while downloading {url}: {e}")
        except FileNotFoundError:
            print("Error: 'yt-dlp' command not found.")
            print("Please ensure yt-dlp is installed and in your system's PATH.")
            return

    print("\n" + "="*50)
    print("Download process finished!")
    print("="*50)


if __name__ == "__main__":
    download_videos()

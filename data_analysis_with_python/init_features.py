import sqlite3
import numpy as np
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os
from VideoWorker import extract
from concurrent.futures import ThreadPoolExecutor

load_dotenv(find_dotenv())
root = os.getenv('ROOT')
dtb_path = os.path.join(root, 'data_analysis_with_sql', 'data.db')
non_dataset_path = os.path.join(root, 'data_understand_and_preprocessing', 'preprocessing', 'dataset', 'non_violence_output')
vio_dataset_path = os.path.join(root, 'data_understand_and_preprocessing', 'preprocessing', 'dataset', 'violence_output')
MAX_THREADS = 10

def get_max_feature(feature_list):
    if feature_list is not None and len(feature_list) > 0:
        return float(np.max(feature_list))
    return None

def get_video_path(video_id):
    if video_id.startswith('n_'):
        idx = video_id.split('_')[1]
        folder = non_dataset_path
    elif video_id.startswith('v_'):
        idx = video_id.split('_')[1]
        folder = vio_dataset_path
    else:
        return None
    for f in os.listdir(folder):
        if f.split('.')[0] == idx:
            return os.path.join(folder, f)
    return None

def process_video(video_data):
    video_id, _ = video_data
    db = None
    try:
        file_path = get_video_path(video_id)
        if file_path is None:
            print(f"File not found for {video_id}")
            return

        db = sqlite3.connect(dtb_path, timeout=10)
        cur = db.cursor()

        if str(file_path).endswith(".npy"):
            frames = np.load(file_path)
        else:
            print(f"Skipping non-npy file: {file_path}")
            return

        if frames.dtype != np.uint8:
            frames = np.clip(frames, 0, 1)
            frames = (frames * 255).astype(np.uint8)

        features = extract(frames)

        update_data = (
            get_max_feature(features.get("frame_diff_mean")),
            get_max_feature(features.get("frame_diff_var")),
            get_max_feature(features.get("blur")),
            get_max_feature(features.get("brightness")),
            get_max_feature(features.get("contrast")),
            get_max_feature(features.get("optical_flow")),
            video_id
        )

        cur.execute("SELECT COUNT(*) FROM Analysis_result WHERE video_id = ?", (video_id,))
        if cur.fetchone()[0] > 0:
            update_query = """
                UPDATE Analysis_result
                SET frame_diff_mean = ?, frame_diff_var = ?, blur = ?, brightness = ?, contrast = ?, optical_flow = ?
                WHERE video_id = ?;
            """
            cur.execute(update_query, update_data)
            print('[UPDATE]', end='')
        else:
            insert_query = """
                INSERT INTO Analysis_result (
                    frame_diff_mean, frame_diff_var, blur, brightness, contrast, optical_flow, video_id, violence_probability
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 0.0);
            """
            cur.execute(insert_query, update_data)
            print('[INSERT]', end='')
        db.commit()
        print(f"Processed video_id: {video_id}")

    except Exception as e:
        print(f"Error processing {video_id}: {e}")

    finally:
        if db:
            db.close()


def main():
    try:
        with sqlite3.connect(dtb_path) as db:
            cur = db.cursor()
            cur.execute("PRAGMA foreign_keys = ON;")
            columns_to_add = [
                ("frame_diff_mean", "REAL"),
                ("frame_diff_var", "REAL"),
                ("blur", "REAL"),
                ("brightness", "REAL"),
                ("contrast", "REAL"),
                ("optical_flow", "REAL"),
            ]
            for col, dtype in columns_to_add:
                try:
                    cur.execute(f"ALTER TABLE Analysis_result ADD COLUMN {col} {dtype};")
                except sqlite3.OperationalError as e:
                    if "duplicate column" not in str(e).lower():
                        raise e
            print("Columns checked/added successfully.")
            cur.execute("SELECT video_id, file_path FROM Metadata;")
            videos = cur.fetchall()
    except sqlite3.Error as e:
        print(f"Initial database error: {e}")
        return

    print(f"Found {len(videos)} videos to process.")
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(process_video, videos)

if __name__ == "__main__":
    main()

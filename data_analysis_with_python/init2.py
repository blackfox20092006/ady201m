import sqlite3
import numpy as np
from dotenv import find_dotenv, load_dotenv
import os
from VideoWorker import extract, get_vio_prob
from concurrent.futures import ThreadPoolExecutor
import cv2

load_dotenv(find_dotenv())
root = os.getenv('ROOT')
dtb_path = os.path.join(root, 'data_analysis_with_sql', 'data.db')
MAX_THREADS = 10
TARGET_FPS = 12
TARGET_SIZE = (256, 256)

def get_max_feature(feature_list):
    if feature_list is not None and len(feature_list) > 0:
        return float(np.max(feature_list))
    return None

def process_video(video_data):
    video_id, file_path = video_data
    try:
        if not os.path.exists(file_path):
            print(f"File not found at path: {file_path} for video_id: {video_id}")
            return None

        frames = []
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print(f"Error opening video file: {file_path}")
            return None

        original_fps = cap.get(cv2.CAP_PROP_FPS)
        if original_fps == 0:
            print(f"Warning: Could not get FPS for {video_id}. Assuming 30.")
            original_fps = 30.0

        step = round(original_fps / TARGET_FPS)
        step = max(1, step)

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % step == 0:
                resized_frame = cv2.resize(frame, TARGET_SIZE)
                frames.append(resized_frame)
            frame_count += 1
        
        cap.release()

        if not frames:
            print(f"No frames extracted for {video_id}")
            return None

        frames_np = np.array(frames)
        features = extract(frames_np)

        processed_data = (
            get_max_feature(features.get("frame_diff_mean")),
            get_max_feature(features.get("frame_diff_var")),
            get_max_feature(features.get("blur")),
            get_max_feature(features.get("brightness")),
            get_max_feature(features.get("contrast")),
            get_max_feature(features.get("optical_flow")),
            video_id,
            get_vio_prob(file_path)[0]
        )
        
        print(f"Processed video_id: {video_id}")
        return processed_data

    except Exception as e:
        print(f"Error processing {video_id}: {e}")
        return None

def main():
    try:
        with sqlite3.connect(dtb_path) as db:
            cur = db.cursor()
            cur.execute("PRAGMA foreign_keys = ON;")
            
            columns_to_add = [
                ("frame_diff_mean", "REAL"), ("frame_diff_var", "REAL"),
                ("blur", "REAL"), ("brightness", "REAL"),
                ("contrast", "REAL"), ("optical_flow", "REAL"),
            ]
            for col, dtype in columns_to_add:
                try:
                    cur.execute(f"ALTER TABLE Analysis_result ADD COLUMN {col} {dtype};")
                except sqlite3.OperationalError as e:
                    if "duplicate column" not in str(e).lower():
                        raise e
            print("Columns checked/added successfully.")
            
            cur.execute("SELECT video_id, file_path FROM Metadata;")
            videos_to_process = cur.fetchall()

    except sqlite3.Error as e:
        print(f"Initial database error: {e}")
        return

    print(f"Found {len(videos_to_process)} videos to process.")
    
    results = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        results = list(executor.map(process_video, videos_to_process))

    valid_results = [r for r in results if r is not None]
    print(f"\nProcessing complete. Writing {len(valid_results)} valid results to database...")

    try:
        with sqlite3.connect(dtb_path, timeout=10) as db:
            cur = db.cursor()
            
            update_query = """
                UPDATE Analysis_result
                SET frame_diff_mean = ?, frame_diff_var = ?, blur = ?, brightness = ?, contrast = ?, optical_flow = ?, violence_probability=?
                WHERE video_id = ?;
            """
            insert_query = """
                INSERT INTO Analysis_result (
                    frame_diff_mean, frame_diff_var, blur, brightness, contrast, optical_flow, video_id, violence_probability
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """

            for data in valid_results:
                video_id = data[6]
                try:
                    cur.execute("SELECT COUNT(*) FROM Analysis_result WHERE video_id = ?", (video_id,))
                    if cur.fetchone()[0] > 0:
                        update_tuple = (data[0], data[1], data[2], data[3], data[4], data[5], data[7], data[6])
                        cur.execute(update_query, update_tuple)
                        print(f'[UPDATE] Wrote data for video_id: {video_id}')
                    else:
                        cur.execute(insert_query, data)
                        print(f'[INSERT] Wrote data for video_id: {video_id}')
                except Exception as e:
                    print(f"Error writing data for video_id {video_id}: {e}")
            
            db.commit()
            print("Database writing complete.")
    
    except sqlite3.Error as e:
        print(f"Database error during bulk write: {e}")

if __name__ == "__main__":
    main()
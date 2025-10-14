import cv2
import numpy as np
import os

def load_video(video_input):
    if isinstance(video_input, str):
        cap = cv2.VideoCapture(video_input)
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        frames = np.array(frames)
        return frames
    elif isinstance(video_input, np.ndarray):
        return video_input
    else:
        raise TypeError("video_input must be a string path or numpy array")

def frame_difference_mean_color(frames):
    values = []
    for i in range(1, len(frames)):
        difference = cv2.absdiff(frames[i], frames[i - 1])
        values.append(np.mean(difference))
    return values

def frame_difference_variance_color(frames):
    values = []
    for i in range(1, len(frames)):
        difference = cv2.absdiff(frames[i], frames[i - 1])
        values.append(np.var(difference))
    return values

def brightness_variation_color(frames):
    return [np.mean(frame) for frame in frames]

def contrast_variation_color(frames):
    return [np.std(frame) for frame in frames]

def blur_level_variation(frames):
    values = []
    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        values.append(np.var(lap))
    return values

def optical_flow_magnitude_from_frames(frames):
    magnitudes = []
    if len(frames) < 2:
        return magnitudes
    prev_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
    for i in range(1, len(frames)):
        curr_gray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, curr_gray, None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0
        )
        mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        magnitudes.append(np.mean(mag))
        prev_gray = curr_gray
    return magnitudes

def optical_flow_magnitude(video_input):
    if isinstance(video_input, str):
        cap = cv2.VideoCapture(video_input)
        magnitudes = []
        ret, prev_frame = cap.read()
        if not ret:
            cap.release()
            return magnitudes
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        while True:
            ret, curr_frame = cap.read()
            if not ret:
                break
            curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, curr_gray, None,
                pyr_scale=0.5,
                levels=3,
                winsize=15,
                iterations=3,
                poly_n=5,
                poly_sigma=1.2,
                flags=0
            )
            mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            magnitudes.append(np.mean(mag))
            prev_gray = curr_gray
        cap.release()
        return magnitudes
    elif isinstance(video_input, np.ndarray):
        return optical_flow_magnitude_from_frames(video_input)
    else:
        raise TypeError("video_input must be a file path or numpy array")

def extract(video_input):
    frames = load_video(video_input)
    features = {}
    features["frame_diff_mean"] = frame_difference_mean_color(frames)
    features["frame_diff_var"] = frame_difference_variance_color(frames)
    features["brightness"] = brightness_variation_color(frames)
    features["contrast"] = contrast_variation_color(frames)
    features["blur"] = blur_level_variation(frames)
    features["optical_flow"] = optical_flow_magnitude(video_input)
    return features

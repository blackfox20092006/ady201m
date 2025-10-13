import cv2
import numpy as np

def load_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    frames = np.array(frames)
    return frames


def frame_difference_mean_color(frames):
    values = []
    for i in range(1, len(frames)):
        current_frame = frames[i]
        previous_frame = frames[i - 1]
        difference = cv2.absdiff(current_frame, previous_frame)
        mean_value = np.mean(difference)
        values.append(mean_value)
    return values


def frame_difference_variance_color(frames):
    values = []
    for i in range(1, len(frames)):
        current_frame = frames[i]
        previous_frame = frames[i - 1]
        difference = cv2.absdiff(current_frame, previous_frame)
        variance_value = np.var(difference)
        values.append(variance_value)
    return values


def brightness_variation_color(frames):
    values = []
    for frame in frames:
        mean_brightness = np.mean(frame)
        values.append(mean_brightness)
    return values


def contrast_variation_color(frames):
    values = []
    for frame in frames:
        std_contrast = np.std(frame)
        values.append(std_contrast)
    return values


def blur_level_variation(frames):
    values = []
    for frame in frames:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray_frame, cv2.CV_64F)
        variance_value = np.var(laplacian)
        values.append(variance_value)
    return values


def optical_flow_magnitude(video_path):
    cap = cv2.VideoCapture(video_path)
    magnitudes = []

    ret, previous_frame = cap.read()
    if not ret:
        cap.release()
        return magnitudes

    previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

    while True:
        ret, current_frame = cap.read()
        if not ret:
            break

        current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(
            previous_gray,
            current_gray,
            None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0
        )
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        mean_magnitude = np.mean(magnitude)
        magnitudes.append(mean_magnitude)
        previous_gray = current_gray

    cap.release()
    return magnitudes


def extract(video_path):
    frames = load_video(video_path)
    features = {}
    features["frame_diff_mean"] = frame_difference_mean_color(frames)
    features["frame_diff_var"] = frame_difference_variance_color(frames)
    features["brightness"] = brightness_variation_color(frames)
    features["contrast"] = contrast_variation_color(frames)
    features["blur"] = blur_level_variation(frames)
    features["optical_flow"] = optical_flow_magnitude(video_path)
    return features

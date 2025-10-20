import cv2
import numpy as np
import os, sys
import tensorflow as tf
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
root = os.getenv('ROOT')
model_path = os.path.join(root, model, "model.tflite")

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
def get_vio_prob(video_path):
    def load_video_tensor(video_path, size=(224,224), fps=12):
        cap = cv2.VideoCapture(video_path)
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(cv2.resize(frame, size), cv2.COLOR_BGR2RGB)
            frames.append(frame)
        cap.release()
        video = np.array(frames, dtype=np.float32) / 255.0
        return tf.convert_to_tensor(video, dtype=tf.float32)
    interpreter = tf.lite.Interpreter(model_path=model_path)
    runner = interpreter.get_signature_runner()
    init_states = {
        name: tf.zeros(x['shape'], dtype=x['dtype'])
        for name, x in runner.get_input_details().items()
    }
    del init_states['image']
    video = load_video_tensor(video_path, size=(172,172), fps=12)
    clips = tf.split(video[tf.newaxis], video.shape[0], axis=1)
    states = init_states
    for clip in clips:
        outputs = runner(**states, image=clip)
        logits = outputs.pop('logits')[0]
        states = outputs

    probs = tf.nn.softmax(logits)
    labels = ["Fight", "No_Fight"]
    ans = [float(probs[0].numpy()), float(probs[1].numpy())]
    return ans

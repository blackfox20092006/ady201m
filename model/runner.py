import tensorflow as tf
import numpy as np
import cv2, sys, os
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
def main(video_path):
    print(f"[INFO] Loading model.tflite")
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
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
    top_k = tf.argsort(probs, direction='DESCENDING')[:2].numpy()
    print("\nPrediction:")
    for idx in top_k:
        print(f"  {labels[idx]:10s}: {probs[idx].numpy():.3f}")
    print(f"\nFinal result: {labels[int(tf.argmax(probs))]}")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 runner.py <video_path>")
        sys.exit(1)
    main(sys.argv[1])
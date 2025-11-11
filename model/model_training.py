import os
import sys
import glob
import numpy as np
import cv2
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers, Model

IMAGE_SIZE = 256
NUM_FRAMES = 16
BATCH_SIZE = 8
EPOCHS = 10
DATA_DIR = 'data'
TFLITE_MODEL_PATH = 'model.tflite'

def py_load_video(path_b):
    path = path_b.decode('utf-8')
    cap = cv2.VideoCapture(path)
    
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (IMAGE_SIZE, IMAGE_SIZE))
        frames.append(frame)
    cap.release()

    if not frames:
        return np.zeros((NUM_FRAMES, IMAGE_SIZE, IMAGE_SIZE, 3), dtype=np.float32)

    video = np.array(frames, dtype=np.float32)
    
    total_frames = video.shape[0]
    if total_frames >= NUM_FRAMES:
        indices = np.linspace(0, total_frames - 1, NUM_FRAMES, dtype=int)
        sampled_video = video[indices, ...]
    else:
        padding = np.tile(video[-1:], (NUM_FRAMES - total_frames, 1, 1, 1))
        sampled_video = np.concatenate([video, padding], axis=0)
        
    sampled_video = sampled_video / 255.0
    return sampled_video.astype(np.float32)

def load_video(path, label):
    video = tf.py_function(py_load_video, [path], tf.float32)
    video.set_shape([NUM_FRAMES, IMAGE_SIZE, IMAGE_SIZE, 3])
    return video, label

def create_dataset(data_dir):
    violence_files = glob.glob(os.path.join(data_dir, 'violence', '*.*'))
    violence_labels = [0] * len(violence_files)
    
    non_violence_files = glob.glob(os.path.join(data_dir, 'non_violence', '*.*'))
    non_violence_labels = [1] * len(non_violence_files)
    
    files = violence_files + non_violence_files
    labels = violence_labels + non_violence_labels
    
    if not files:
        sys.exit(1)
        
    ds = tf.data.Dataset.from_tensor_slices((files, labels))
    ds = ds.shuffle(len(files), reshuffle_each_iteration=True)
    
    dataset_size = len(files)
    train_size = int(0.8 * dataset_size)
    
    train_ds = ds.take(train_size)
    val_ds = ds.skip(train_size)
    
    train_ds = train_ds.map(load_video, num_parallel_calls=tf.data.AUTOTUNE)
    train_ds = train_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    
    val_ds = val_ds.map(load_video, num_parallel_calls=tf.data.AUTOTUNE)
    val_ds = val_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    
    return train_ds, val_ds

def build_base_model():
    hub_url = "https://tfhub.dev/tensorflow/movinet/a3/base/kinetics-600/feature-vector/3"
    
    encoder = hub.KerasLayer(hub_url, trainable=True, name='movinet_encoder')
    
    inputs = tf.keras.layers.Input(
        shape=[NUM_FRAMES, IMAGE_SIZE, IMAGE_SIZE, 3],
        dtype=tf.float32,
        name='image'
    )
    
    features = encoder(inputs)
    
    x = layers.Dense(128, activation='relu', name='head_dense_1')(features)
    x = layers.Dropout(0.2)(x)
    
    outputs = layers.Dense(2, name='head_logits')(x)
    
    model = Model(inputs, outputs)
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    
    return model

def export_streaming_model(base_model):
    base_encoder = base_model.get_layer('movinet_encoder')
    head_dense_1 = base_model.get_layer('head_dense_1')
    head_logits = base_model.get_layer('head_logits')
    
    hub_url_stream = "https://tfhub.dev/tensorflow/movinet/a3/stream/kinetics-600/feature-vector/3"
    stream_encoder_layer = hub.KerasLayer(hub_url_stream, trainable=False, name='movinet_stream_encoder')
    
    stream_encoder_layer.set_weights(base_encoder.get_weights())
    
    head_dense_1_stream = layers.Dense.from_config(head_dense_1.get_config())
    head_logits_stream = layers.Dense.from_config(head_logits.get_config())
    
    head_dense_1_stream.set_weights(head_dense_1.get_weights())
    head_logits_stream.set_weights(head_logits.get_weights())

    # Thêm lớp Softmax
    head_softmax_stream = layers.Softmax()

    class StreamingModelModule(tf.Module):
        def __init__(self, encoder, dense1, logits, softmax):
            super().__init__()
            self.encoder = encoder
            self.dense1 = dense1
            self.logits = logits
            self.softmax = softmax # Thêm softmax

        @tf.function
        def __call__(self, image, states):
            features, new_states = self.encoder(image, states=states)
            x = self.dense1(features)
            logits_output = self.logits(x)
            probs_output = self.softmax(logits_output) # Áp dụng softmax
            
            # Đổi tên output từ 'logits' thành 'probabilities'
            return {'probabilities': probs_output, **new_states}

        @tf.function
        def __call__(self, image, states):
            features, new_states = self.encoder(image, states=states)
            x = self.dense1(features)
            logits_output = self.logits(x)
            
            return {'logits': logits_output, **new_states}

        @tf.function
        def init_states(self, batch_size):
            return self.encoder.init_states(batch_size)

    streaming_module = StreamingModelModule(
        encoder=stream_encoder_layer,
        dense1=head_dense_1_stream,
        logits=head_logits_stream,
        softmax=head_softmax_stream # Truyền lớp softmax vào
    )

    init_states = stream_encoder_layer.init_states(batch_size=1)
    state_specs = {
        name: tf.TensorSpec(tensor.shape, tensor.dtype, name=name)
        for name, tensor in init_states.items()
    }
    image_spec = tf.TensorSpec([1, 1, IMAGE_SIZE, IMAGE_SIZE, 3], tf.float32, name='image')

    saved_model_path = 'movinet_finetuned_stream_savedmodel'
    
    call_sig = streaming_module.__call__.get_concrete_function(image_spec, state_specs)
    init_states_sig = streaming_module.init_states.get_concrete_function(tf.TensorSpec([], tf.int32, name='batch_size'))

    tf.saved_model.save(
        streaming_module,
        saved_model_path,
        signatures={
            'run': call_sig, 
            'init_states': init_states_sig
        }
    )

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)
    converter.target_spec.supported_ops = [
        tf.lite.OpsSet.TFLITE_BUILTINS,
        tf.lite.OpsSet.SELECT_TF_OPS
    ]
    tflite_model = converter.convert()

    with open(TFLITE_MODEL_PATH, 'wb') as f:
        f.write(tflite_model)
    
def main():
    train_ds, val_ds = create_dataset(DATA_DIR)
    
    base_model = build_base_model()
    
    base_model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_accuracy', restore_best_weights=True)
        ],
        verbose=0
    )
    
    export_streaming_model(base_model)

if __name__ == "__main__":
    main()
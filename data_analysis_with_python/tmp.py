import os, sqlite3, numpy as np, tensorflow as tf
from huggingface_hub import hf_hub_download
from dotenv import find_dotenv, load_dotenv
from official.projects.movinet.modeling import movinet, movinet_model

load_dotenv(find_dotenv())
root = os.getenv('ROOT')
dtb_path = os.path.join(root, 'data_analysis_with_sql', 'data.db')

repo = "engares/MoViNet4Violence-Detection"
subdir = "trained_models_dropout_autolr_trlayers_NoAug/movinet_a3_12fps_64bs_0.001lr_0.3dr_0tl"
files = [
    "movinet_a3_stream_wbm.data-00000-of-00001",
    "movinet_a3_stream_wbm.index",
    "checkpoint"
]
ckpt_dir = "weights_movinet_a3"
os.makedirs(ckpt_dir, exist_ok=True)

for f in files:
    path = hf_hub_download(repo_id=repo, filename=f"{subdir}/{f}")
    dst = os.path.join(ckpt_dir, f)
    if not os.path.exists(dst):
        tf.io.gfile.copy(path, dst, overwrite=True)

def build_movinet_a3():
    backbone = movinet.Movinet(
        model_id='a3',
        causal=True,
        conv_type='2plus1d',
        se_type='2plus3d',
        activation='hard_swish',
        gating_activation='hard_sigmoid',
        use_external_states=True,
        use_positional_encoding=True
    )
    model = movinet_model.MovinetClassifier(backbone=backbone, num_classes=2, output_states=True)
    inputs = tf.ones([1, 1, 256, 256, 3])
    model.build(inputs.shape)
    ckpt = tf.train.Checkpoint(model=model)
    ckpt.restore(os.path.join(ckpt_dir, "movinet_a3_stream_wbm")).expect_partial()
    return model

model = build_movinet_a3()

def streaming_inference(video_arr, model):
    video = tf.convert_to_tensor(video_arr, dtype=tf.float32)
    if video.ndim == 4:
        video = video / 255.0
    elif video.ndim == 5:
        video = video[0] / 255.0
    images = tf.split(video[tf.newaxis], video.shape[0], axis=1)
    states = model.init_states(tf.shape(tf.ones(shape=[1, 1, 256, 256, 3])))
    all_logits = []
    for img in images:
        logits, states = model({**states, "image": img})
        all_logits.append(logits)
    logits = tf.concat(all_logits, 0)
    probs = tf.nn.softmax(logits, axis=-1)
    return float(probs[-1][0].numpy())

db = sqlite3.connect(dtb_path)
cur = db.cursor()

try:
    cur.execute("ALTER TABLE Analysis_result ADD COLUMN violence_probability REAL;")
    db.commit()
except sqlite3.OperationalError:
    pass

cur.execute("SELECT video_id, file_path FROM Metadata;")
videos = cur.fetchall()

for video_id, file_path in videos:
    try:
        arr = np.load(file_path)
        prob = streaming_inference(arr, model)
        cur.execute(
            "UPDATE Analysis_result SET violence_probability = ? WHERE video_id = ?;",
            (prob, video_id)
        )
        db.commit()
        print(f"[OK] {os.path.basename(file_path)} → {prob*100:.2f}% violent")
    except Exception as e:
        print(f"[SKIP] {file_path}: {e}")
        continue

cur.close()
db.close()

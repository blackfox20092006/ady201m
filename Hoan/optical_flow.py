import argparse
import json
from typing import Tuple, Dict, Optional

import cv2
import numpy as np


# --------- utils ---------
def _to_u8_no_gray(frame: np.ndarray) -> np.ndarray:
    """
    Normalize a frame to uint8 WITHOUT converting to grayscale.
    Supports (H, W), (H, W, 3), (H, W, 4). If alpha is present, it is dropped.
    """
    if frame.ndim == 2:
        arr = frame
    elif frame.ndim == 3 and frame.shape[-1] in (3, 4):
        arr = frame[..., :3]  # BGR, drop alpha if present
    else:
        raise ValueError(f"Unsupported frame shape: {frame.shape}")
    if arr.dtype == np.uint8:
        return arr
    if np.issubdtype(arr.dtype, np.floating):
        mn, mx = float(np.nanmin(arr)), float(np.nanmax(arr))
        if mn >= 0.0 and mx <= 1.0:
            arr = arr * 255.0
        else:
            arr = cv2.normalize(arr, None, 0, 255, cv2.NORM_MINMAX)
    else:
        arr = cv2.normalize(arr, None, 0, 255, cv2.NORM_MINMAX)
    return np.clip(arr, 0, 255).astype(np.uint8)


# --------- LK per-channel (no grayscale) ---------
def lk_magnitudes_color(
    prev_frame: np.ndarray,
    next_frame: np.ndarray,
    feature_params: Optional[Dict] = None,
    lk_params: Optional[Dict] = None,
):
    """
    Compute point-wise motion magnitudes using Lucas–Kanade on each color channel
    separately (to avoid grayscale conversion). Returns concatenated magnitudes
    across channels, as well as counts for tracking stats.
    """
    prev = _to_u8_no_gray(prev_frame)
    nxt  = _to_u8_no_gray(next_frame)

    if feature_params is None:
        feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
    if lk_params is None:
        lk_params = dict(winSize=(15, 15),
                         maxLevel=2,
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    if prev.ndim == 2:
        prev = prev[..., None]
        nxt  = nxt[..., None]

    mags = []
    tried = 0
    good  = 0
    C = prev.shape[-1]

    for c in range(C):
        prev_c = prev[..., c]
        nxt_c  = nxt[..., c]
        p0 = cv2.goodFeaturesToTrack(prev_c, mask=None, **feature_params)
        if p0 is None or len(p0) == 0:
            continue
        tried += int(len(p0))

        p1, st, err = cv2.calcOpticalFlowPyrLK(prev_c, nxt_c, p0, None, **lk_params)
        if p1 is None:
            continue
        good_new = p1[st == 1]
        good_old = p0[st == 1]
        good += int(len(good_new))
        if len(good_new) == 0:
            continue

        d = (good_new - good_old).reshape(-1, 2)  # (N,2)
        mag = np.sqrt(d[:, 0] * d[:, 0] + d[:, 1] * d[:, 1]).astype(np.float32)
        mags.append(mag)

    if len(mags) > 0:
        mags = np.concatenate(mags, axis=0)
    else:
        mags = np.empty((0,), dtype=np.float32)

    return mags, tried, good


# --------- main API ---------
def lk_features_for_video_array(
    video: np.ndarray,
    step: int = 1,
    feature_params: Optional[Dict] = None,
    lk_params: Optional[Dict] = None,
) -> Tuple[float, Dict[str, float]]:
    """
    Compute motion score and statistics from a video numpy array.
    video: (T,H,W) or (T,H,W,3/4) -- NO grayscale conversion is performed.
    Returns:
        (float_score, dict_stats)
    """
    if step < 1:
        step = 1
    if video.ndim not in (3, 4):
        raise ValueError(f"Unsupported video shape: {video.shape}")

    T = video.shape[0]
    h = int(video.shape[1]) if video.ndim >= 3 else 0
    w = int(video.shape[2]) if video.ndim >= 3 else 0

    if T < 2:
        return 0.0, {
            "num_pairs": 0, "mean": 0.0, "std": 0.0, "median": 0.0, "p95": 0.0,
            "max_frame_mean": 0.0, "max_point_magnitude": 0.0,
            "track_success_ratio_mean": 0.0, "points_tracked_mean": 0.0,
            "height": h, "width": w, "method": "LK_color",
        }

    pair_means = []
    pair_maxes = []
    track_ratios = []
    pts_tracked = []

    for t in range(0, T - step):
        prev, nxt = video[t], video[t + step]
        mags, tried, good = lk_magnitudes_color(prev, nxt, feature_params, lk_params)

        if mags.size > 0:
            pair_means.append(float(mags.mean()))
            pair_maxes.append(float(mags.max()))
        else:
            pair_means.append(0.0)
            pair_maxes.append(0.0)

        ratio = float(good) / float(tried) if tried > 0 else 0.0
        track_ratios.append(ratio)
        pts_tracked.append(float(good))

    pair_means = np.asarray(pair_means, dtype=np.float64)
    pair_maxes = np.asarray(pair_maxes, dtype=np.float64)
    track_ratios = np.asarray(track_ratios, dtype=np.float64)
    pts_tracked = np.asarray(pts_tracked, dtype=np.float64)

    score = float(pair_means.mean())

    stats: Dict[str, float] = {
        "num_pairs": int(pair_means.size),
        "mean": score,
        "std": float(pair_means.std(ddof=0)),
        "median": float(np.median(pair_means)),
        "p95": float(np.percentile(pair_means, 95)),
        "max_frame_mean": float(pair_means.max()),
        "max_point_magnitude": float(pair_maxes.max()),
        "track_success_ratio_mean": float(track_ratios.mean()),
        "points_tracked_mean": float(pts_tracked.mean()),
        "height": h,
        "width": w,
        "method": "LK_color",
    }
    return score, stats


# --------- optional helpers for CLI usage ---------
def read_video_to_numpy(path: str, max_frames: Optional[int] = None, stride: int = 1) -> np.ndarray:
    """
    Read a video file into a numpy array of shape (T, H, W, 3) in BGR order.
    Args:
        path: path to a video readable by OpenCV.
        max_frames: if given, stop after reading this many frames.
        stride: read every `stride`-th frame for speed (>=1).
    """
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {path}")

    frames = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if (idx % stride) == 0:
            frames.append(frame)
            if max_frames is not None and len(frames) >= max_frames:
                break
        idx += 1
    cap.release()

    if len(frames) == 0:
        return np.empty((0, ), dtype=np.uint8)

    return np.stack(frames, axis=0)  # (T,H,W,3)


def main():
    parser = argparse.ArgumentParser(description="LK optical flow per-channel (no grayscale).")
    parser.add_argument("--video", type=str, help="Path to a video file (e.g., .mp4).")
    parser.add_argument("--npy", type=str, help="Path to a .npy video array (T,H,W[,C]).")
    parser.add_argument("--step", type=int, default=1, help="Frame step for pairing (default: 1).")
    parser.add_argument("--max_frames", type=int, default=None, help="Optional cap on frames when reading a video.")
    parser.add_argument("--stride", type=int, default=1, help="Read every `stride`-th frame when loading a video.")
    args = parser.parse_args()

    if (args.video is None) == (args.npy is None):
        raise SystemExit("Specify exactly one of --video or --npy")

    if args.npy is not None:
        video = np.load(args.npy, allow_pickle=False)
    else:
        video = read_video_to_numpy(args.video, max_frames=args.max_frames, stride=max(args.stride, 1))

    score, stats = lk_features_for_video_array(video, step=max(args.step, 1))
    print(f"score_float: {score}")
    print("stats_dict:")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()

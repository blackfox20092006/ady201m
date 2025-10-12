import cv2
import numpy as np
from typing import Tuple, Dict

def _to_u8(img: np.ndarray) -> np.ndarray:
    if img.dtype == np.uint8:
        return img
    if np.issubdtype(img.dtype, np.floating):
        mn, mx = float(np.nanmin(img)), float(np.nanmax(img))
        if mn >= 0.0 and mx <= 1.0:
            img = img * 255.0
        else:
            img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    else:
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    return np.clip(img, 0, 255).astype(np.uint8)

def variance_of_laplacian_single(
    frame: np.ndarray,
    ksize: int = 3,
    pre_blur: int = 0,
    color_mode: str = "y",
) -> Tuple[float, Dict[str, float]]:
    f = _to_u8(frame)

    if pre_blur and pre_blur > 0:
        k = int(pre_blur) if int(pre_blur) % 2 == 1 else int(pre_blur) + 1
        f = cv2.GaussianBlur(f, (k, k), 0)

    def lap_var(img1c: np.ndarray) -> Tuple[float, float, float]:
        lap = cv2.Laplacian(img1c, cv2.CV_64F, ksize=ksize)
        v = float(lap.var())
        m = float(lap.mean())
        s = float(lap.std())
        return v, m, s

    if f.ndim == 2:
        v, m, s = lap_var(f)
        return v, {"lap_mean": m, "lap_std": s, "height": int(f.shape[0]), "width": int(f.shape[1]),
                   "ksize": int(ksize), "pre_blur": int(pre_blur), "mode": "single_channel"}

    bgr = f[..., :3]

    if color_mode == "y":
        y = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)[..., 0]
        v, m, s = lap_var(y)
        stats = {"lap_mean": m, "lap_std": s, "height": int(y.shape[0]), "width": int(y.shape[1]),
                 "ksize": int(ksize), "pre_blur": int(pre_blur), "mode": "Y"}
        return v, stats

    if color_mode == "gray":
        g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        v, m, s = lap_var(g)
        stats = {"lap_mean": m, "lap_std": s, "height": int(g.shape[0]), "width": int(g.shape[1]),
                 "ksize": int(ksize), "pre_blur": int(pre_blur), "mode": "gray"}
        return v, stats

    chans = cv2.split(bgr)
    vals, means, stds = [], [], []
    for ch in chans:
        v, m, s = lap_var(ch)
        vals.append(v); means.append(m); stds.append(s)

    if color_mode == "per_channel_median":
        agg = float(np.median(vals))
        mode = "per_channel_median"
    else:
        agg = float(np.mean(vals))
        mode = "per_channel_mean"

    stats = {
        "bgr_vars": [float(x) for x in vals],
        "lap_mean_avg": float(np.mean(means)),
        "lap_std_avg": float(np.mean(stds)),
        "height": int(bgr.shape[0]),
        "width": int(bgr.shape[1]),
        "ksize": int(ksize),
        "pre_blur": int(pre_blur),
        "mode": mode,
    }
    return agg, stats
def variance_of_laplacian_video(
    video: np.ndarray,
    ksize: int = 3,
    pre_blur: int = 0,
    color_mode: str = "y",
) -> Tuple[float, Dict[str, float]]:
    if video.ndim not in (3, 4):
        raise ValueError(f"Unsupported video shape: {video.shape}")
    T = video.shape[0]
    if T == 0:
        return 0.0, {"num_frames": 0}

    vals = []
    for t in range(T):
        v, _ = variance_of_laplacian_single(video[t], ksize=ksize, pre_blur=pre_blur, color_mode=color_mode)
        vals.append(v)
    vals = np.asarray(vals, dtype=np.float64)

    score = float(vals.mean())
    stats = {
        "num_frames": int(T),
        "mean": score,
        "std": float(vals.std(ddof=0)),
        "median": float(np.median(vals)),
        "p95": float(np.percentile(vals, 95)),
        "min": float(vals.min()),
        "max": float(vals.max()),
        "ksize": int(ksize),
        "pre_blur": int(pre_blur),
        "mode": color_mode,
    }
    return score, stats

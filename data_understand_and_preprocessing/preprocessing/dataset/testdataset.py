import numpy as np
import matplotlib.pyplot as plt
frames = np.load("1.npy")
print("Shape of frames:", frames.shape)
num_show = min(1, frames.shape[0])
plt.figure(figsize=(15, 3))
for i in range(num_show):
    plt.subplot(1, num_show, i + 1)
    plt.imshow(frames[i])
    plt.title(f"Frame {i}")
    plt.axis("on")
plt.show()

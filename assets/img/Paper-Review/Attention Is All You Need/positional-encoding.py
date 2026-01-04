import numpy as np
import matplotlib.pyplot as plt

# parameters
d_model = 512
max_len = 8

# positional encoding
pe = np.zeros((max_len, d_model))
pos = np.arange(max_len)[:, None]
i = np.arange(d_model)[None, :]

angle_rates = 1 / np.power(10000, (2 * (i // 2)) / d_model)
angles = pos * angle_rates

pe[:, 0::2] = np.sin(angles[:, 0::2])
pe[:, 1::2] = np.cos(angles[:, 1::2])

# visualization
plt.figure(figsize=(12, 6))
plt.imshow(pe, aspect='auto', cmap='viridis')
plt.colorbar()
plt.xlabel("Embedding Dimension")
plt.ylabel("Position")
plt.title("Positional Encoding (sin / cos)")
plt.show()

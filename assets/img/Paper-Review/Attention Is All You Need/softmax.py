import numpy as np
import matplotlib.pyplot as plt

def softmax_scalar(x):
    e = np.exp(x)
    return e / (e + 1)

x = np.linspace(-10, 10, 500)
y = softmax_scalar(x)

plt.figure(figsize=(7, 4))
plt.plot(x, y)
plt.xlabel("score")
plt.ylabel("attention weight")
plt.title("Softmax in Transformer Attention")
plt.ylim(0, 1)
plt.tight_layout()
plt.show()

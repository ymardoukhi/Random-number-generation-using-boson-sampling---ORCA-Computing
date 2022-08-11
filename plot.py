from typing import Counter
import numpy as np
import json
import matplotlib.pyplot as plt
from collections import Counter


res = np.load("data/output_tf.npy")
res = Counter(res)
total_count = np.sum(list(res.values()))
vals = [i/total_count for i in list(res.values())]

fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(111)
ax.bar(list(res.keys()), vals)
ax.set_xticklabels(list(res.keys()), rotation = 45)
ax.set_ylabel("Probability")
ax.set_xlabel("von Neumann Strings")
plt.savefig("data/von_neumann_dist_tf.png")
plt.close(fig)

with open("data/exact_dist_tf.json", "r") as f:
    res = json.load(f)

total_count = np.sum(list(res.values()))
vals = [i/total_count for i in list(res.values())]

fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(111)
ax.bar(list(res.keys()), vals)
ax.set_xticklabels(list(res.keys()), rotation = 45)
ax.set_ylabel("Probability")
ax.set_xlabel("Fock States")
plt.savefig("data/Fock_dist_tf.png")
plt.close(fig)

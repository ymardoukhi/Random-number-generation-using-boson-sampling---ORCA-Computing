import numpy as np
import json
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.ticker as mticker


res = np.load("data/output_tf.npy")
res = Counter(res)
total_count = np.sum(list(res.values()))
vals = [i/total_count for i in list(res.values())]

fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(111)
ax.bar(list(res.keys()), vals)
ticks_loc = list(ax.get_xticks())
ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
ax.set_xticklabels(list(res.keys()), rotation = 90)
ax.set_ylabel("Probability")
ax.set_xlabel("von Neumann Strings")
plt.savefig("data/von_neumann_dist_tf.png")
plt.close(fig)

res = np.load("data/huffman_uniform.npy")
res = Counter(res)
total_count = np.sum(list(res.values()))
vals = [i/total_count for i in list(res.values())]

fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(111)
ax.bar(list(res.keys()), vals)
ticks_loc = list(ax.get_xticks())
ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
ax.set_xticklabels(list(res.keys()), rotation = 90)
ax.set_ylabel("Probability")
ax.set_xlabel("von Neumann Strings")
plt.savefig("data/huffman_dist.png")
plt.close(fig)

with open("data/exact_dist_tf.json", "r") as f:
    res = json.load(f)

total_count = np.sum(list(res.values()))
vals = [i/total_count for i in list(res.values())]

fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(111)
ax.bar(list(res.keys()), vals)
ticks_loc = list(ax.get_xticks())
ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
ax.set_xticklabels(list(res.keys()), rotation = 90)
ax.set_ylabel("Probability")
ax.set_xlabel("Fock States")
plt.savefig("data/Fock_dist_tf.png")
plt.close(fig)

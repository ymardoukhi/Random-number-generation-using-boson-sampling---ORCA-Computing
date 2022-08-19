import os
import json
import argparse
import numpy as np
import joblib as jb
from collections import Counter
from src.PostProcessing import VonNeumann

def one_zero_ratio(binary_string: str) -> dict:
    binary_arr = np.asarray([*binary_string], dtype=int)
    ratio = np.sum(binary_arr)/binary_arr.shape[0]
    return {'0': 1-ratio, '1': ratio}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('N', type=int, help='number of shots')
    args = parser.parse_args()

    shots_ensemble = np.load("borealisoutput.npy")
    shots_ensemble = [
        (shots_ensemble[i][0], shots_ensemble[i+1][0]) 
        for i in range(shots_ensemble.shape[0] - 1)]
    
    neumann_enc = VonNeumann()
    
    output_strs = jb.Parallel(n_jobs=-2, verbose=5)(
        jb.delayed(neumann_enc.von_neumann_prot)(shots) for shots in shots_ensemble)
    
    # filter out '' strings
    output_strs = list(filter(lambda i: i != '', output_strs))
    # calculate the ratio of 1's and 0's in the concatenation of
    # all those binary strings
    ratio = one_zero_ratio("".join(output_strs))
    # calculate the statistics of the binary strings and sort 
    # the probability of their appearance in a descending manner
    output_strs = Counter(output_strs)
    output_strs = [(key, val) for key, val in output_strs.items()]
    output_strs.sort(key=lambda x: x[1], reverse=True)
    output_strs = {el[0]: el[1]/args.N/2 for el in output_strs}
    
    # save the statistics of 01 ratio and the binary strings
    output_path = "./data/borealis"
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    with open("{}/cloud_N{}.json".format(output_path, args.N), "w") as f:
        json.dump(output_strs, f)
    with open("{}/ratio_N{}.json".format(output_path, args.N), "w") as f:
        json.dump(ratio, f)

if __name__ == "__main__":
    main()
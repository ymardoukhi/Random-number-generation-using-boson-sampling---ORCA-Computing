import json
import argparse
import numpy as np
import joblib as jb
from collections import Counter
import strawberryfields as sf
from src.Architecture import SFArchitecture
from src.PostProcessing import Encoding
from src.Huffman import HuffmanEncoding

def sample_generator(n: int, m: int, num_params: int, v: int, sim_bool: bool, seed: float):
    np.random.seed(seed)

    arch = SFArchitecture(n, m, num_params, v, sim_bool)
    eng = sf.Engine(backend="fock", backend_options={"cutoff_dim": n+1})

    tf_theta_list = [np.pi/4 for _ in range(num_params)]
    args_dict = {}
    for i in range(num_params):
        args_dict["theta_{}".format(i)] = tf_theta_list[i]

    return eng.run(program=arch, args=args_dict).samples[0]

def hufmann_uniform_sim(encoding, fock_state):
    return encoding[fock_state]

def res_to_dict(result):
    count_dict = Counter(result)
    total = sum(list(count_dict.values()))
    return {key: val/total for key, val in count_dict.items()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='number of photos')
    parser.add_argument('m', type=int, help='number of modes')
    parser.add_argument('d', type=int, help='depth of the circuit')
    parser.add_argument('n_param', type=int, help='number of beam-spliters')
    parser.add_argument('v', type=int, help='version of the architecture')
    args = parser.parse_args()

    N = int(1e3)

    with open("data/exact_dist.json", "r") as f:
        fock_state_dist = json.load(f)
    
    encoding = HuffmanEncoding(fock_state_dist)
    encoding.huffman_encoding()

    np.random.seed(42)
    seeds = np.random.randint(N, size=N)

    output_strs = jb.Parallel(n_jobs=-1, verbose=5)(
        jb.delayed(hufmann_uniform_sim)(
            args.n, args.m, args.d, args.n_param,
            args.v, True, encoding.encoding, seed
            ) for seed in seeds)

    output_strs = list(filter(lambda i: i != '', output_strs))

    output_strs = res_to_dict(output_strs)
    
    with open("data/huffman.json", "w") as f:
        json.dump(output_strs, f)

if __name__ == "__main__":
    main()

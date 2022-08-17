import os
import json
import argparse
import numpy as np
import joblib as jb
import strawberryfields as sf
from collections import Counter
from src.Architecture import SFArchitecture
from src.PostProcessing import VonNeumann

def von_neumann_sim(n, m, num_params, v, sim_bool, seed):
    np.random.seed(seed)

    arch = SFArchitecture(n, m, num_params, v, sim_bool)
    eng = sf.Engine(backend="fock", backend_options={"cutoff_dim": n+1})

    tf_theta_list = [np.pi/4 for _ in range(num_params)]
    args_dict = {}
    for i in range(num_params):
        args_dict["theta_{}".format(i)] = tf_theta_list[i]
    
    shots = []
    for _ in range(2):
        shots.append(eng.run(program=arch.prog, args=args_dict).samples[0])

    von_neumann_enc = VonNeumann()
    von_neumann_str = von_neumann_enc.von_neumann_prot(shots)
    
    return von_neumann_str

def one_zero_ratio(binary_string: str) -> dict:
    binary_arr = np.asarray([*binary_string], dtype=int)
    ratio = np.sum(binary_arr)/binary_arr.shape[0]
    return {'0': 1-ratio, '1': ratio}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='number of photos')
    parser.add_argument('m', type=int, help='number of modes')
    parser.add_argument('n_param', type=int, help='number of beam-spliters')
    parser.add_argument('v', type=int, help='version of the architecture')
    parser.add_argument('N', type=int, help="total number of runs")
    args = parser.parse_args()

    np.random.seed(42)
    seeds = np.random.randint(args.N, size=args.N)

    print("Simulation has started for {} runs".format(args.N))
    output_strs = jb.Parallel(n_jobs=-2, verbose=5)(
        jb.delayed(von_neumann_sim)(
            args.n, args.m, args.n_param, args.v,
            True, seed) for seed in seeds)

    output_strs = list(filter(lambda i: i != '', output_strs))
    ratio = one_zero_ratio("".join(output_strs))
    output_strs = Counter(output_strs)
    output_strs = [(key, val) for key, val in output_strs.items()]
    output_strs.sort(key=lambda x: x[1], reverse=True)
    output_strs = {el[0]: el[1]/args.N for el in output_strs}
    
    output_path = "./data/n{}_m{}_nparam{}_v{}".format(args.n, args.m, args.n_param, args.v)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    with open("{}/simulation_result.json".format(output_path), "w") as f:
        json.dump(output_strs, f)
    with open("{}/ratio_simulation.json".format(output_path), "w") as f:
        json.dump(ratio, f)


main()

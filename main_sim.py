import os
import json
import argparse
import numpy as np
import joblib as jb
import strawberryfields as sf
from collections import Counter
from src.Architecture import SFArchitecture
from src.PostProcessing import VonNeumann

def naive_uniform_sim(n, m, d, num_params, v, sim_bool, seed):
    np.random.seed(seed)

    arch = SFArchitecture(n, m, d, num_params, v, sim_bool)
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
    
    return bose_sim.von_neumann_str

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='number of photos')
    parser.add_argument('m', type=int, help='number of modes')
    parser.add_argument('d', type=int, help='depth of the circuit')
    parser.add_argument('n_param', type=int, help='number of beam-spliters')
    parser.add_argument('v', type=int, help='version of the architecture')
    args = parser.parse_args()

    N = 10**3
    np.random.seed(42)
    seeds = np.random.randint(N, size=N)

    output_strs = jb.Parallel(n_jobs=-1, verbose=5)(
        jb.delayed(naive_uniform_sim)(
            args.n, args.m, args.d, args.n_param,
            args.v, True, seed
            ) for seed in seeds)

    output_strs = list(filter(lambda i: i != '', output_strs))
    
    output_path = "./data/n{}_m{}_nparam{}_v{}".format(args.n, args.m, args.n_param, args.v)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    with open("{}/simulation_result.json".format(output_path), "w") as f:
        json.dump(output_strs, f)
    with open("{}/ratio_simulation.json".format(output_path), "w") as f:
        json.dump(ratio, f)


main()

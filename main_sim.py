import os
import json
import argparse
import numpy as np
import joblib as jb
import strawberryfields as sf
from collections import Counter
from src.Architecture import SFArchitecture
from src.PostProcessing import VonNeumann

def boson_sampler(n, m, num_params, v, seed):
    """
    function that returns a sample from Boson sampler
    using the fock backend

    input:
        n (int): number of photons
        m (int): number of modes
        num_paramas (int): number of free parametres of the architecture
        v (int): version of the architecture
        seed (float): seed to make the simulation reproducible
    return:
        _ (np.ndarray): sampled fock state
    """
    
    # seed the RNG
    np.random.seed(seed)

    # initialise the architecture of the Boson Sampler 
    # and the Strawberryfields engine with fock backend
    arch = SFArchitecture(n, m, num_params, v, True)
    eng = sf.Engine(backend="fock", backend_options={"cutoff_dim": n+1})

    # set the beam splitters \theta parameter to pi/4
    tf_theta_list = [np.pi/4 for _ in range(num_params)]
    args_dict = {}
    for i in range(num_params):
        args_dict["theta_{}".format(i)] = tf_theta_list[i]
    
    return eng.run(program=arch.prog, args=args_dict).samples[0]

def one_zero_ratio(binary_string: str) -> dict:
    binary_arr = np.asarray([*binary_string], dtype=int)
    ratio = np.sum(binary_arr)/binary_arr.shape[0]
    return {'0': 1-ratio, '1': ratio}

def main():
    
    # parse the input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='number of photos')
    parser.add_argument('m', type=int, help='number of modes')
    parser.add_argument('n_param', type=int, help='number of beam-spliters')
    parser.add_argument('v', type=int, help='version of the architecture')
    parser.add_argument('N', type=int, help="total number of runs")
    args = parser.parse_args()
    output_path = "./data/n{}_m{}_nparam{}_v{}".format(args.n, args.m, args.n_param, args.v)

    # generate N random seeds where N is the total number of simulations
    # fixed the seed of the RNG such that I get N perdictable seeds for 
    # the sake of reproducibility
    np.random.seed(42)
    seeds = np.random.randint(args.N, size=args.N)

    # get N binary strings via Von Neumann protocol in parallel
    print("Simulation has started for {} runs".format(args.N))
    shots_ensemble = jb.Parallel(n_jobs=-2, verbose=5)(
        jb.delayed(boson_sampler)(
            args.n, args.m, args.n_param, args.v, seed) for seed in seeds)
    np.save("{}/samples_N{}.npy".format(output_path, args.N), shots_ensemble)

    # form tuples of shots such that we can apply the 
    # von Neumann post processing in a parallel fashion
    shots_ensemble = [
        (shots_ensemble[i][0], shots_ensemble[i+1][0]) 
        for i in range(len(shots_ensemble) - 1)]
    
    # initialise the von Neumann post-processing and 
    # get the binary strings
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
    output_strs = {el[0]: el[1]/args.N for el in output_strs}
    
    # save the statistics of 01 ratio and the binary strings
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    with open("{}/simulation_result_{}.json".format(output_path, args.N), "w") as f:
        json.dump(output_strs, f)
    with open("{}/ratio_simulation_{}.json".format(output_path, args.N), "w") as f:
        json.dump(ratio, f)


if __name__ == "__main__":
    main()

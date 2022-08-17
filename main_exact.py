import os
import json
import argparse
import numpy as np
import strawberryfields as sf
from src.BosonSamplingArch import FockProb
from src.Architecture import SFArchitecture

def exact_bose_samp(n, m, n_param, v):

    arch = SFArchitecture(n, m, n_param, v)
    eng = sf.Engine(backend="fock", backend_options={"cutoff_dim": n+1})

    tf_theta_list = [np.pi/4 for _ in range(n_param)]
    args_dict = {}
    for i in range(n_param):
        args_dict["theta_{}".format(i)] = tf_theta_list[i]
    
    device_output = eng.run(arch.prog, args=args_dict).state

    fock_states_stat = FockProb(device_output)
    return fock_states_stat

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='number of photos')
    parser.add_argument('m', type=int, help='number of modes')
    parser.add_argument('n_param', type=int, help='number of beam-spliters')
    parser.add_argument('v', type=int, help='version of the architecture')
    args = parser.parse_args()
    fock_states = exact_bose_samp(args.n, args.m, args.n_param, args.v)
    
    output_path = "./data/n{}_m{}_nparam{}_v{}".format(args.n, args.m, args.n_param, args.v)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    with open("{}/exact_result.json".format(output_path), "w") as f:
        json.dump(fock_states.fock_dict, f)

if __name__ == "__main__":
    main()
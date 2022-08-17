import os
import json
import argparse
import numpy as np
import strawberryfields as sf
from src.BosonSamplingStat import FockProb
from src.Architecture import SFArchitecture

def exact_bose_samp(n, m, n_param, v):
    """
    a wrapper function that retreives the exact state of 
    a given Boson Sampler and returs the statistics of the 
    fock states

    input:
        n (int): number of photos
        m (int): number of modes
        n_param (int): number of free parameters
        v (int): version of the architecture
    return:
        _ (FockProb): statistics of the fock states
    """

    # construct the Boson Sampler architecture and the 
    # straberryfields engine with the fock backend
    arch = SFArchitecture(n, m, n_param, v)
    eng = sf.Engine(backend="fock", backend_options={"cutoff_dim": n+1})

    # initialise all the beam splitters to \theta=pi/4
    tf_theta_list = [np.pi/4 for _ in range(n_param)]
    # attache the free paramaters of the architecture 
    # to the \theta variables defined above
    args_dict = {}
    for i in range(n_param):
        args_dict["theta_{}".format(i)] = tf_theta_list[i]
    
    # store the exact state of the Boson Sampler
    device_output = eng.run(arch.prog, args=args_dict).state

    # extract the fock states statistics
    fock_states_stat = FockProb(device_output)
    return fock_states_stat

def main():
    
    # parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='number of photos')
    parser.add_argument('m', type=int, help='number of modes')
    parser.add_argument('n_param', type=int, help='number of beam-spliters')
    parser.add_argument('v', type=int, help='version of the architecture')
    args = parser.parse_args()

    # get the exact statistics of the fock states
    fock_states = exact_bose_samp(args.n, args.m, args.n_param, args.v)
    ordered_fock_states = [(key, val) for key, val in fock_states.fock_dict.items()]
    ordered_fock_states.sort(key=lambda x: x[1], reverse=True)
    ordered_fock_states = {el[0]: el[1] for el in ordered_fock_states}
    
    # store the fock states probabilities as a dictionary
    output_path = "./data/n{}_m{}_nparam{}_v{}".format(args.n, args.m, args.n_param, args.v)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    with open("{}/exact_result.json".format(output_path), "w") as f:
        json.dump(ordered_fock_states, f)

if __name__ == "__main__":
    main()
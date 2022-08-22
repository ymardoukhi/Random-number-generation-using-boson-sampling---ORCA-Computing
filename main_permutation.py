import os
import json
import argparse
import numpy as np

def main():

    # parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='number of photos')
    parser.add_argument('m', type=int, help='number of modes')
    parser.add_argument('n_param', type=int, help='number of beam-spliters')
    parser.add_argument('v', type=int, help='version of the architecture')
    parser.add_argument('N', type=int, help='number of simulations (shots)')
    args = parser.parse_args()

    # set the data path to load the simulation results
    data_path = "data/n{}_m{}_nparam{}_v{}".format(args.n, args.m, args.n_param, args.v)
    if not os.path.exists(data_path):
        raise FileNotFoundError("path {} does not exists".format(data_path))

    # load the fock state samples generated previously 
    # by a Boson sampler
    fock_state_samples = np.load("{}/samples_N{}.npy".format(data_path, args.N))

    # construct an encoding such that degenerate fock states 
    # form a class. Those fock states in the same class are 
    # assigned to digits 0 and 1 in turn. Singleton classes 
    # encode the empty string ''
    encoding = {
        '(0, 0, 2, 2)': '0',
        '(2, 2, 0, 0)': '1',
        ####################
        '(0, 2, 1, 1)': '0',
        '(2, 0, 1, 1)': '1',
        '(1, 1, 2, 0)': '0',
        '(1, 1, 0, 2)': '1',
        ####################
        '(0, 0, 3, 1)': '0',
        '(0, 0, 1, 3)': '1',
        '(1, 3, 0, 0)': '0',
        '(3, 1, 0, 0)': '1',
        ####################
        '(0, 1, 0, 3)': '0',
        '(1, 0, 3, 0)': '1',
        '(3, 0, 1, 0)': '0',
        '(0, 3, 0, 1)': '1',
        ####################
        '(1, 0, 0, 3)': '0',
        '(0, 1, 3, 0)': '1',
        '(3, 0, 0, 1)': '0',
        '(0, 3, 1, 0)': '1',
        ####################
        '(0, 1, 2, 1)': '0',
        '(1, 0, 1, 2)': '1',
        '(1, 2, 1, 0)': '0',
        '(2, 1, 0, 1)': '1',
        ####################
        '(2, 1, 1, 0)': '0',
        '(1, 2, 0, 1)': '1',
        '(0, 1, 1, 2)': '0',
        '(1, 0, 2, 1)': '1',
        ####################
        '(0, 0, 0, 4)': '0',
        '(0, 0, 4, 0)': '1',
        '(4, 0, 0, 0)': '0',
        '(0, 4, 0, 0)': '1',
        ####################
        '(0, 2, 2, 0)': '0',
        '(2, 0, 0, 2)': '1',
        '(0, 2, 0, 2)': '0',
        '(2, 0, 2, 0)': '1',
        ####################
        '(1, 1, 1, 1)': ''
    }

    # get the binary strings using the encoding above
    output_strs = [encoding[str(tuple(fock_state))] for fock_state in fock_state_samples]

    # store the binary strings 
    with open("{}/permutation_strs_N{}.json".format(data_path, args.N), "w") as f:
        json.dump(output_strs, f)

if __name__ == "__main__":
    main()

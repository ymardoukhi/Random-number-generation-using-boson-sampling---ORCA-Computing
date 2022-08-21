import os
import json
import numpy as np
import joblib as jb
import strawberryfields as sf
from collections import Counter
from src.Borealis import Programme
from src.PostProcessing import VonNeumann

def borealis_sampler(prog: sf.program.Program) -> np.ndarray:
    """
    function that gets a Borealis programme and run it on 
    a local "gaussian" engine. It returns a fock state 
    sample of numpy array type
    
    input:
        prog (strawberryfields.program.Program): Borealis 
            Strawberryfields programme
    return:
        _ (np.ndarray): a sample fockstate
    """
    
    eng = sf.Engine(backend="gaussian")
    return eng.run(prog, crop=True).samples[0]

def one_zero_ratio(binary_string: str) -> dict:
    """
    a function that calculates the ration between zeros 
    and ones in a binary string

    input:
        binary_string (str): a given binary string e.g. 010001
    
    return:
        _ (dict): dictionary of the form {'0': 1-ratio, '1': ratio} 
            where ration is the ration between zeros and ones
    """
    # convert the binary strings into an array of zero and 
    # one integers
    binary_arr = np.asarray([*binary_string], dtype=int)
    # sum is the total number of ones
    ratio = np.sum(binary_arr)/binary_arr.shape[0]
    return {'0': 1-ratio, '1': ratio}


def main():

    modes = 4
    shots = int(1e2)
    output_path = "./data/borealis"

    # squeezing-gate parameters
    r = [1.234] * modes

    # rotation-gate parameters
    phi_0 = np.asarray([0] * modes)
    phi_1 = np.asarray([0] * modes)
    phi_2 = np.asarray([0] * modes)

    # beamsplitter parameters
    alpha_0 = np.asarray([np.pi/4] * modes)
    alpha_1 = np.asarray([np.pi/4] * modes)
    alpha_2 = np.asarray([np.pi/4] * modes)

    # the travel time per delay line in time bins
    delays = [1, 6, 36]

    # set the first beamsplitter arguments to 'T=1' ('alpha=0') to fill the
    # loops with pulses
    alpha_0[:delays[0]] = 0.0
    alpha_1[:delays[1]] = 0.0
    alpha_2[:delays[2]] = 0.0

    gate_args = {
        "Sgate": r,
        "loops": {
            0: {"Rgate": phi_0.tolist(), "BSgate": alpha_0.tolist()},
            1: {"Rgate": phi_1.tolist(), "BSgate": alpha_1.tolist()},
            2: {"Rgate": phi_2.tolist(), "BSgate": alpha_2.tolist()},
        },
    }

    borealis_prog = Programme(gate_args_dict=gate_args)

    shots_ensemble = jb.Parallel(n_jobs=-2, verbose=5)(
        jb.delayed(borealis_sampler)(borealis_prog.prog) for _ in range(shots))
    
    shots_ensemble = [
        (shots_ensemble[i][0], shots_ensemble[i+1][0]) 
        for i in range(len(shots_ensemble) - 1)]
    
    neumann_enc = VonNeumann()
    
    output_strs = jb.Parallel(n_jobs=-2, verbose=5)(
        jb.delayed(neumann_enc.von_neumann_prot)(shots) for shots in shots_ensemble)
    
    # filter out '' strings
    output_strs = list(filter(lambda i: i != '', output_strs))
    # same the output_strs for post analysis
    with open("{}/output_strs_local_N{}.json".format(output_path, shots), "w") as f:
        json.dump(output_strs, f)
    # calculate the ratio of 1's and 0's in the concatenation of
    # all those binary strings
    ratio = one_zero_ratio("".join(output_strs))
    # calculate the statistics of the binary strings and sort 
    # the probability of their appearance in a descending manner
    output_strs = Counter(output_strs)
    output_strs = [(key, val) for key, val in output_strs.items()]
    output_strs.sort(key=lambda x: x[1], reverse=True)
    output_strs = {el[0]: el[1]/shots/2 for el in output_strs}
    
    # save the statistics of 01 ratio and the binary strings
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    with open("{}/local_N{}.json".format(output_path, shots), "w") as f:
        json.dump(output_strs, f)
    with open("{}/ratio_local_N{}.json".format(output_path, shots), "w") as f:
        json.dump(ratio, f)

if __name__ == "__main__":
    main()
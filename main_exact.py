import numpy as np
import json
import strawberryfields as sf
from strawberryfields import ops
from src.BosonSamplingArch import FockProb

def exact_bose_samp():

    eng = sf.Engine(backend="fock", backend_options={"cutoff_dim": 4})

    boson_sampling = sf.Program(4)

    with boson_sampling.context as q:

        ops.Fock(1) | q[0]
        ops.Fock(1) | q[1]
        ops.Fock(1) | q[2]
        ops.Fock(0) | q[3]

        ops.BSgate(np.pi/4, 0.0) | (q[0], q[1])
        ops.BSgate(np.pi/4, 0.0) | (q[2], q[3])

        ops.BSgate(np.pi/4, 0.0) | (q[1], q[2])

        ops.BSgate(np.pi/4, 0.0) | (q[0], q[1])
        ops.BSgate(np.pi/4, 0.0) | (q[2], q[3])

    fock_states_stat = FockProb(eng.run(boson_sampling).state)
    return fock_states_stat

def main():
    fock_states = exact_bose_samp()
    
    with open("data/exact_dist.json", "w") as f:
        json.dump(fock_states.fock_dict, f)

main()
import numpy as np
import json
import strawberryfields as sf
from src.BosonSamplingArch import FockProb
from src.Architecture import SFArchitecture

def exact_bose_samp():

    n_photos = 3
    modes = 4
    depth = 3
    ver = 0
    theta_num = 5

    arch = SFArchitecture(n_photos, modes, depth, theta_num, ver)
    eng = sf.Engine(backend="fock", backend_options={"cutoff_dim": n_photos+1})

    # tf_theta_list = [np.pi/4 for _ in range(5)]
    tf_theta_list = [5.490799580937497, 6.231214270348368, 0.9528841360440271, 4.193042253237036, 0.04889399082251021]
    args_dict = {}
    for i in range(theta_num):
        args_dict["theta_{}".format(i)] = tf_theta_list[i]

    fock_states_stat = FockProb(eng.run(arch.prog, args=args_dict).state)
    return fock_states_stat

def main():
    fock_states = exact_bose_samp()
    
    with open("data/exact_dist_tf.json", "w") as f:
        json.dump(fock_states.fock_dict, f)

main()
import argparse
import numpy as np
import strawberryfields as sf
from strawberryfields import ops
import joblib as jb
from src.BoseSampSimulation import BoseSampSim
from src.Architecture import SFArchitecture

def naive_uniform_sim(n, m, d, num_params, v, sim_bool, seed):
    np.random.seed(seed)

    arch = SFArchitecture(n, m, d, num_params, v, sim_bool)
    eng = sf.Engine(backend="fock", backend_options={"cutoff_dim": n+1})

    tf_theta_list = [np.pi/4 for _ in range(num_params)]
    args_dict = {}
    for i in range(num_params):
        args_dict["theta_{}".format(i)] = tf_theta_list[i]

    bose_sim = BoseSampSim(programme=arch.prog, engine=eng, params_dict=args_dict)
    bose_sim.two_shot_simulation()
    bose_sim.von_neumann_prot()
    
    return bose_sim.von_neumann_str

def main():

    N = 10**4
    np.random.seed(42)
    seeds = np.random.randint(N, size=N)

    output_strs = jb.Parallel(n_jobs=10, verbose=5)(
        jb.delayed(bose_sampling_sim)(seed) for seed in seeds)

    output_strs = list(filter(lambda i: i != '', output_strs))
    
    np.save("data/output_tf.npy", output_strs)

main()

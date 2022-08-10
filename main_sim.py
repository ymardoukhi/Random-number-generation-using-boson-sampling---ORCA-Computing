import numpy as np
import strawberryfields as sf
from strawberryfields import ops
import joblib as jb
from src.BoseSampSimulation import BoseSampSim

def bose_sampling_sim(seed):
    np.random.seed(seed)
    eng = sf.Engine(backend="fock", backend_options={"cutoff_dim": 4})

    boson_sampling_sim = sf.Program(4)

    with boson_sampling_sim.context as q:

        ops.Fock(1) | q[0]
        ops.Fock(1) | q[1]
        ops.Fock(1) | q[2]
        ops.Fock(0) | q[3]

        ops.BSgate(np.pi/4, 0.0) | (q[0], q[1])
        ops.BSgate(np.pi/4, 0.0) | (q[2], q[3])

        ops.BSgate(np.pi/4, 0.0) | (q[1], q[2])

        ops.BSgate(np.pi/4, 0.0) | (q[0], q[1])
        ops.BSgate(np.pi/4, 0.0) | (q[2], q[3])

        ops.MeasureFock() | q
    
    bose_sim = BoseSampSim(programme=boson_sampling_sim, engine=eng)
    bose_sim.two_shot_simulation()
    bose_sim.von_neumann_prot()
    
    return bose_sim.von_neumann_str

def main():

    N = 10**5
    np.random.seed(42)
    seeds = np.random.randint(N, size=N)

    output_strs = jb.Parallel(n_jobs=10, verbose=5)(
        jb.delayed(bose_sampling_sim)(seed) for seed in seeds)

    output_strs = list(filter(lambda i: i != '', output_strs))
    
    np.save("./output.npy", output_strs)

main()

import xcc

with open("api_key.txt", "r") as f:
    api_key = f.readlines()[0][:-1]

settings = xcc.Settings(REFRESH_TOKEN=api_key)
settings.save()

import numpy as np
import strawberryfields as sf
from strawberryfields.tdm import full_compile, get_mode_indices
from strawberryfields.ops import Sgate, Rgate, BSgate, MeasureFock

eng = sf.RemoteEngine("borealis")
device = eng.device

modes = 4

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

gate_args_list = full_compile(gate_args, device)
vac_modes = sum(delays)

n, N = get_mode_indices(delays)
print(n, N)

prog = sf.TDMProgram(N)

with prog.context(*gate_args_list) as (p, q):
    Sgate(p[0]) | q[n[0]]
    for i in range(len(delays)):
        Rgate(p[2 * i + 1]) | q[n[i]]
        BSgate(p[2 * i + 2], np.pi / 2) | (q[n[i + 1]], q[n[i]])
    MeasureFock() | q[0]

shots = 10000
# results = eng.run(prog, shots=shots, crop=True)
# 
# samples = results.samples
# np.save("borealisoutput.npy", samples)

compile_options = {
    "device": device,
    "realistic_loss": True,
}

run_options = {
    "shots": None,
    "crop": True,
    "space_unroll": True,
}

eng_sim = sf.Engine(backend="gaussian")
prog.space_unroll(shots=1)
results_sim = eng_sim.run(prog, crop=True)#**run_options, compile_options=compile_options)
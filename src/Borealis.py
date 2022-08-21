import numpy as np
import strawberryfields as sf
from strawberryfields import ops
from strawberryfields.tdm import full_compile, get_mode_indices

class Programme:

    def __init__(self, gate_args_dict: dict) -> None:
        self.gate_args_list = self._get_best_matach_params(
            gate_args_dict=gate_args_dict)
        self.delays = [1, 6, 36]
        self.nN = get_mode_indices(self.delays)
        self.prog = self._init_prog()


    def _get_best_matach_params(self, gate_args_dict):
        """
        connects to Xanadu cloud Borealis to get the closest matches
        of the gate parameters
        input:
            gate_args_dict (dict): dictionary of containing the predefined 
                values of the SGates, BSGates and RGates
            return:
                _ (list): a list of the parameter values of the gates 
                    adjusted to the Borealis device
        """
        eng = sf.RemoteEngine("borealis")
        device = eng.device

        gate_args_list = full_compile(gate_args_dict, device)

        return gate_args_list
    
    def _init_prog(self):
        """
        initialise Borealis programme 

        input:
            (None)
        return:
            _ (strawberryfields.program.Program): Borealis Strawberry Fields programme
        """

        n = self.nN[0]
        N = self.nN[1]
    
        prog = sf.TDMProgram(N)

        with prog.context(*self.gate_args_list) as (p, q):
            ops.Sgate(p[0]) | q[n[0]]
            for i in range(len(self.delays)):
                ops.Rgate(p[2 * i + 1]) | q[n[i]]
                ops.BSgate(p[2 * i + 2], np.pi / 2) | (q[n[i + 1]], q[n[i]])
            ops.MeasureFock() | q[0]
        
        return prog


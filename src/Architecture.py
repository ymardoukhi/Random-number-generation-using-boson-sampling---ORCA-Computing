import numpy as np
import strawberryfields as sf
from strawberryfields import ops

class SFArchitecture:

    def __init__(self, n, m, d, bsg_num, v) -> None:
        self.n = n
        self.m = m
        self.d = d
        self.v = v
        self.bsg_num = bsg_num
        self.prog = self._build_arch()
    
    def _build_arch(self, simulation):

        prog = sf.Program(self.m)

        theta_params = ["theta_{}".format(i) for i in range(self.bsg_num)]
        theta_lst = prog.params(*theta_params)

        with prog.context as q:

            ops.Fock(1) | q[0]
            ops.Fock(1) | q[1]
            ops.Fock(1) | q[2]
            ops.Fock(1) | q[3]

            ops.BSgate(theta_lst[0], 0.0) | (q[0], q[1])
            ops.BSgate(theta_lst[1], 0.0) | (q[2], q[3])

            ops.BSgate(theta_lst[2], 0.0) | (q[1], q[2])

            ops.BSgate(theta_lst[3], 0.0) | (q[0], q[1])
            ops.BSgate(theta_lst[4], 0.0) | (q[2], q[3])

            if simulation:
                ops.MeasureFock | q

        return prog
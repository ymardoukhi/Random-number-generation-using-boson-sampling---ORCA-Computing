import strawberryfields as sf
from strawberryfields import ops

class SFArchitecture:
    """
    class to setup the architecture of the interferometer. Currently 
    the archictercture must be changed within the source file. But I 
    aim to compile the architecture via txt files
    """

    def __init__(self, n: int, m: int, d: int, bsg_num: int, v: int, sim_bool: bool=False) -> None:
        """
        initialising the SFArchitecture object
        input:
            n (int): number of the input photos
            m (int): number of modes
            d (int): depth of the circuit
            bsg_num (int): number of beam splitters
            sim_bool (bool): whether the architecture is used for simulation
        """
        self.n = n
        self.m = m
        self.d = d
        self.v = v
        self.bsg_num = bsg_num
        self.prog = self._build_arch(sim_bool)
    
    def _build_arch(self, simulation: bool) -> sf.program.Program:
        """
        function that builds the Strawberry Fields programme

        """

        # initialise the programme by indicating the number of modes
        prog = sf.Program(self.m)

        # create programme parameters for the theta angle of the beam splitters
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
                ops.MeasureFock() | q

        return prog
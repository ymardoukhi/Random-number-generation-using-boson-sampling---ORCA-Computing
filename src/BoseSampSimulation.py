import numpy as np

class BoseSampSim:

    def __init__(self, programme, engine) -> None:
        self.programme = programme
        self.engine = engine
        self.two_shots = None
        self.von_neumann_str = None


    def two_shot_simulation(self):
        res = []
        for i in range(2):
            output = self.engine.run(self.programme).samples[0]
            res.append(self._convert_binary(output))
        
        self.two_shots = res

    def _convert_binary(self, array):
        array[np.where(array > 0)[0]] = 1
        return array

    def von_neumann_prot(self):
        output_res = ''
        for i in range(len(self.two_shots[0])):
            if self.two_shots[0][i] == self.two_shots[1][i]:
                continue
            else:
                digit = abs(self.two_shots[0][i]*(self.two_shots[1][i]-1))
                output_res = output_res + str(digit)
        self.von_neumann_str = output_res

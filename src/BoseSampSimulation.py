import numpy as np
import joblib as jb

class BoseSampSim:

    def __init__(self, programme, engine, params_dict, encoding=None) -> None:
        self.programme = programme
        self.engine = engine
        self.args = params_dict
        self.encoding = encoding
        self.two_shots = None
        self.von_neumann_str = None


    def two_shot_simulation(self):
        res = []
        for i in range(2):
            output = self.engine.run(self.programme).samples[0]
            res.append(self._convert_binary(output))
        
        self.two_shots = res

    def _hufmann_str(self):
        output = self.engine.run(self.programme, args=self.args).samples[0]
        return self.encoding[str(tuple(output))]

    def hufmann_simulation(self, shots):
        two_str = []
        for _ in range(2):
            str_ls = []

            for _ in range(shots):
                str_ls.append(self._hufmann_str())

            two_str.append("".join(str_ls))
        self.two_shots = two_str

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

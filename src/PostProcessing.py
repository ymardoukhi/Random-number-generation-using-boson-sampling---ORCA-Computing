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
        for _ in range(2):
            output = self.engine.run(self.programme, args=self.args).samples[0]
            bin_output = self._convert_binary(output)
            bin_output = "".join(list(map(str, bin_output)))
            res.append(bin_output)

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
        upper_bound = min(len(self.two_shots[0]), len(self.two_shots[1]))
        for i in range(upper_bound):
            if self.two_shots[0][i] == self.two_shots[1][i]:
                continue
            else:
                digit = abs(
                    int(self.two_shots[0][i])*(int(self.two_shots[1][i])-1)
                    )
                output_res = output_res + str(digit)
        self.von_neumann_str = output_res

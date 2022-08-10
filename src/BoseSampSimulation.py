import numpy as np

class BoseSampSim:

    def __init__(self, programme, engine) -> None:
        self.programme = programme
        self.engine = engine


    def two_shot_simulation(self):
        res = []
        for i in range(2):
            output = self.engine.run(self.programme).samples[0]
            res.append(self.convert_binary(output))
        
        return res

    def convert_binary(self, array):
        array[np.where(array > 0)[0]] = 1
        return array

    def von_neumann_prot(input1, input2):
        output_res = ''
        for i in range(len(input1)):
            if input1[i] == input2[i]:
                continue
            else:
                digit = abs(input1[i]*(input2[i]-1))
                output_res = output_res + str(digit)
        return output_res

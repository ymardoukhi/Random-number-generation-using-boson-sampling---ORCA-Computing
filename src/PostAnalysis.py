import numpy as np
import joblib as jb
from collections import Counter

class BinSamples:

    def __init__(self, binary_strs: list) -> None:
        self.binary_strs = binary_strs

    def _zero_one_ratio(self, binary_string: str) -> dict:
        """
        a function that calculates the ration between zeros 
        and ones in a binary string

        input:
            binary_string (str): a given binary string e.g. 010001
    
        return:
            _ (dict): dictionary of the form {'0': 1-ratio, '1': ratio} 
                where ration is the ration between zeros and ones
        """
        # convert the binary strings into an array of zero and 
        # one integers
        binary_arr = np.asarray([*binary_string], dtype=int)
        # sum is the total number of ones
        ratio = np.sum(binary_arr)/binary_arr.shape[0]
        return {'0': 1-ratio, '1': ratio}


    def _distribution(self, binary_strs: list):
        """
        calculate the probability of appearance of a specific 
        binary string in a list of binary strings

        input:
            binar_strs (list): list of binary strings
        return:
            _ (dict): dictionary of the form {'001': 0.12, ...} 
                specifying the probability distribution of binary 
                strings
        """
        # get the length of the list for normalising the probabilities
        N = len(binary_strs)
        # count the number of occurances of the binary strings
        output_strs = Counter(binary_strs)
        # form a list of tuples of binary strings and their associated 
        # appearance probability to sort them in a descending manner
        output_strs = [(key, val) for key, val in output_strs.items()]
        output_strs.sort(key=lambda x: x[1], reverse=True)

        return {el[0]: el[1]/N for el in output_strs}


    def _trunc_stat(self, trunc_index: list):
        """
        calculate the ratio between 0's and 1's bits in a 
        list of binary strings truncated at a specific index

        input:
            trunc_index (int): the index at which the list of binary strings must 
                be truncated
        return:
            _ (dict): a dictionary of the form {"ratio": #1, "dist": #2} where #1 
                is the a dictionary indicating the ration of 0's and 1's and 
                #2 is a dictionary containing the probability distribution of 
                distinct binary strings
        """
        return {
            "ratio": self._zero_one_ratio("".join(self.binary_strs[:trunc_index])),
            "dist": self._distribution(self.binary_strs[:trunc_index])
            }

    def truncated_ensemble(self, trunc_indices):
        """
        function that parallelise the calculation of the 01 ratio and the 
        distribution of the binary strings for a list of truncation indices

        input:
            trunc_indices (list): list of indices
        return:
            _ (dict): a dictionary of the form {ind: {"ratio": , "dist": }} 
        """
        res = jb.Parallel(n_jobs=-2, verbose=5)(
            jb.delayed(self._trunc_stat)(index) for index in trunc_indices
        )

        return {trunc_indices[i]: res[i] for i in range(len(trunc_indices))}



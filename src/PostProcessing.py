import numpy as np

class PostEncoding:
    """
    class that provides a dictionary of the encoding scheme of 
    the output of a Boson Sampler
    """

    def __init__(self, encoding: dict=None) -> None:
        """
        input:
            encoding (dict): is a dictionary of the form {'(n_1, n_2, ..., n_m)': '0101...001'}
                that maps a fock state onto a binary string
        """
        self.encoding = encoding

class Huffman(PostEncoding):
    """
    sub-class of PostEncoding that uses the Huffman encoding scheme
    to encode the fock states into binary strings
    """

    def __init__(self, encoding: dict = None) -> None:
        super().__init__(encoding)
    
    def huffman(self, fock_state: str) -> str:
        """
        function that return the binary string of a fock state 
        according to the Huffman encoding scheme
        
        input:
            fock_state (str): a given fock state given in the form of '(n_1, n_2, ..., n_m)' 
                i.e. string of a tuple
        return:
            _ (str): the Huffman encoding of the input fock state
        """
        return self.encoding[fock_state]

class Permutation(PostEncoding):

    def __init__(self, encoding: dict = None) -> None:
        super().__init__(encoding)

class VonNeumann(PostEncoding):
    """
    class containing methods to perform von Neumann post processing 
    of the fock states of a Boson Sampler
    """

    def __init__(self, encoding: dict = None) -> None:
        super().__init__(encoding)

    def _convert_binary(self, array: np.ndarray) -> str:
        """
        method to convert the numpy array of the output of 
        Strawberryfields engine.run method to a binary 
        string of 01. The strig zero corresponds to no 
        photon detection and the string 1 corresponds to 
        the detection of a photon or multiple photos

        input:
            array (numpy.ndarray): a numpy array of the form [n_1, n_2, ..., n_m]
                where n_m is the number of photos in the m_th mode
        return:
            bin_string (str): binary string of the input fock state
        """
        array[np.where(array > 0)[0]] = 1
        bin_string = "".join(list(map(str, array)))
        return bin_string
    
    def von_neumann_prot(self, shots: list) -> str:
        """
        method that gets two fock states as a list of numpy arrays 
        and returns a binary string according to the von Neumann 
        protocol. the von Neumann protocol is given by the following 
        table
        input_1 | input_2 | output 
        --------|---------|-------
            0   |    0    |   *
            0   |    1    |   0
            1   |    0    |   1
            1   |    1    |   *
        
        where the * means discarded

        input:
            shots (List[numpy.ndarray[int]]): a list of two fock states
        return:
            output_res (str): processed binary string of two fock states 
                according to the von Neumann protocol
        """

        # empty string that records the output of the von Neumann protocol
        output_res = ''

        # convert the fock states to binary strings
        shots = list(map(self._convert_binary, shots))
        str_len = len(shots[0])
        
        # von Neumann protocol
        for i in range(str_len):
            # discard if two bits are the same
            if shots[0][i] == shots[1][i]:
                continue
            else:
                # a trick to avoid nested if conditions
                digit = abs(
                    int(shots[0][i])*(int(shots[1][i])-1)
                    )
                output_res = output_res + str(digit)
        return output_res

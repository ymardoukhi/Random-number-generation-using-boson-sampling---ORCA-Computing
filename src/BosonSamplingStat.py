import numpy as np

class FockProb:
    """
    class to extract information out of the result of a 
    the exact simulation of a Boson Sampler using fock
    backend without measurement gate

    input:
        data (strawberryfields.backends.BaseState): exact state 
            of a Boson sampler using the fock backend
    """

    def __init__(self, data) -> None:
        self.data = data
    
    def fock_states(self):
        """
        function that locates fock states that have non-zero 
        probability of appearance and forms a sorted dictionary  
        of the form {fockstate: probability}

        input:
            None
        return:
            _ (dict): a dictionary of fockstates and their 
                associated probability of appearance
        """
        # find the indices of fock states with non-zero probability
        indices = np.where(self.data.all_fock_probs() > 0.0)
        indices = np.asarray(indices)
        # stupidly, the indices are not of the form of indices but 
        # a list of indices where the length of the list is the dimension 
        # of the original array and in each list the elements are the 
        # indices along that dimension. Anyhow, for a tuple of 
        # (fockstate, probability), such that we would sort them in 
        # a descending manner
        tuple_prob = [
            (str(tuple(indices[:, i])),
            self.data.all_fock_probs()[tuple(indices[:, i])]) for i in range(indices.shape[1])
            ]
        tuple_prob = tuple_prob.sort(key=lambda x: x[1], reverse=True)
        # convert the tuple to dictionary
        return {el[0]: el[1] for el in tuple_prob}
        
    def entropy(self):
        """
        calculates the entropy of the distribution of the fock states
        input:
            None
        return:
            _ (float): the entropy of the distrubition of the fock states
        """
        return np.sum([-i*np.log(i) for i in list(self.fock_dict.values())])
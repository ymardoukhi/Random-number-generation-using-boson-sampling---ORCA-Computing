import numpy as np

class FockProb:

    def __init__(self, data) -> None:
        self.data = data
        self.fock_dict = self._fock_states()
        self.entropy_val = self._entropy()
    
    def _fock_states(self):
        fock_dict = {}
        indices = np.where(self.data.all_fock_probs() > 0.0)
        indices = np.asarray(indices)
        for i in range(indices.shape[1]):
            fock_dict[str(tuple(indices[:, i]))] = self.data.all_fock_probs()[tuple(indices[:, i])]
        
        return fock_dict
    
    def _entropy(self):
        return np.sum([-i*np.log(i) for i in list(self.fock_dict.values())])
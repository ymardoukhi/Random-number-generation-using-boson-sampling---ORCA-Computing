import numpy as np
import networkx as nx

class PostEncoding:
    """
    class that provides a dictionary of the encoding scheme of 
    the output of a Boson Sampler
    """

    def __init__(self) -> None:
        """
        input:
            encoding (dict): is a dictionary of the form {'(n_1, n_2, ..., n_m)': '0101...001'}
                that maps a fock state onto a binary string
        """
        self.encoding = None

class HuffmanEncoding(PostEncoding):
    """
    class to construct Huffman encoding scheme given a probability 
    distribution over a set of symbols (alphabets)
    
    input:
        nodes_dict (dict): a dictionary of symbols with their 
            associated probability of occurance
    """

    def __init__(self, nodes_dict: dict) -> None:
        super().__init__()
        self.nodes_dict = nodes_dict
        self.graph = self._graph()
        self.root = ''
    
    def _graph(self):
        """
        function that initialises a trivial graph (has only nodes) 
        given a set of symbols

        input:
            None
        return:
            G (nx.classes.graph.Graph): a networkx graph which its 
                nodes are the set of symbols
        """
        G = nx.Graph()
        G.add_nodes_from(list(self.nodes_dict.keys()))
        return G
    
    def _huffman_encoding_tree(self):
        """
        implementation of the Huffman encoding scheme. See 
        Introduction to Coding and Information written by Roman 
        Springer Verlag

        This function updates the graph G having only symobls as 
        its nodes and iteratively addes edges between the nodes 
        until a tree is constructed and the nodes are all merged 
        to get the root of the tree

        input:
            None
        return:
            None
        """
        nodes_prob_ls = [ (key, val) for key, val in self.nodes_dict.items() ]

        while len(nodes_prob_ls) > 1:
            left_node = min(nodes_prob_ls, key=lambda el: el[1])
            nodes_prob_ls.remove(left_node)
            right_node = min(nodes_prob_ls, key=lambda el: el[1])
            nodes_prob_ls.remove(right_node)
            new_node = left_node[0] + right_node[0]
            self.graph.add_node(new_node)
            self.graph.add_edge(left_node[0], new_node, label='0')
            self.graph.add_edge(right_node[0], new_node, label='1')
            nodes_prob_ls.append((new_node, left_node[1] + right_node[1]))

        self.root = nodes_prob_ls[0][0]
    
    def _label_extractor(self, path):
        """
        a helper function that extracts the lable of the edges 
        connecting two nodes in a graph G

        input:
            path (list): list of the nodes that indicates a path 
                between two given nodes
        return:
            _ (str): binary string that sequentially shows the 
                label of the edges connecting the two nodes in 
                "path"
        """
        path_list = [ self.graph.get_edge_data(path[i], path[i+1])['label'] for i in range(len(path)-1) ]
        return "".join(path_list)

    def _swapped_encoding(self, bin_str):
        """
        a helper function that swaps a binary string

        input:
            bin_str (str): binary string
        return:
            _ (str): swapped binary string
        """
        swapped_arr = -1*(np.asarray([*bin_str], dtype=int) - 1)
        return "".join(list(map(str, swapped_arr)))

    def huffman_encoding(self):
        """
        function that constructs the binary string encoding of the 
        symbols based on the Huffman encoding

        input:
            None
        return:
            None
        """
        # construct the Huffman encoding tree
        self._huffman_encoding_tree()
        # for each node in the list of symbols 
        # find the shortest path between the root 
        # and the node and the label of the edges 
        # this shortest path is the encoding of that 
        # very node
        node_encoding = {}
        for node in self.nodes_dict.keys():
            path = nx.shortest_path(self.graph, self.root, node)
            code = self._label_extractor(path)
            node_encoding[node] = (code, self._swapped_encoding(code))
        self.encoding = node_encoding

class Permutation(PostEncoding):

    def __init__(self) -> None:
        super().__init__()

class VonNeumann(PostEncoding):
    """
    class containing methods to perform von Neumann post processing 
    of the fock states of a Boson Sampler
    """

    def __init__(self) -> None:
        super().__init__()

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

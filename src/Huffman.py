import networkx as nx

class HuffmanEncoding:
    """
    class to construct Huffman encoding scheme given a probability 
    distribution over a set of symbols (alphabets)
    
    input:
        nodes_dict (dict): a dictionary of symbols with their 
            associated probability of occurance
    """

    def __init__(self, nodes_dict) -> None:
        self.nodes_dict = nodes_dict
        self.graph = self._graph()
        self.root = ''
        self.encoding = None
    
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
            node_encoding[node] = code
        self.encoding = node_encoding
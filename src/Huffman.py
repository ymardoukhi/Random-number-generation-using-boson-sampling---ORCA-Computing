from copy import copy
import networkx as nx

class HuffmanEncoding:

    def __init__(self, nodes_dict) -> None:
        self.nodes_dict = nodes_dict
        self.graph = self._graph()
        self.root = ''
        self.encoding = None
    
    def _graph(self):
        G = nx.Graph()
        G.add_nodes_from(list(self.nodes_dict.keys()))
        return G
    
    def _huffman_encoding_tree(self):
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
        path_list = [ self.graph.get_edge_data(path[i], path[i+1])['label'] for i in range(len(path)-1) ]
        return "".join(path_list)

    def huffman_encoding(self):
        self._huffman_encoding_tree()
        node_encoding = {}
        for node in self.nodes_dict.keys():
            path = nx.shortest_path(self.graph, self.root, node)
            code = self._label_extractor(path)
            node_encoding[node] = code
        self.encoding = node_encoding
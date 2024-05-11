'''
Module containing an implementation of open directed graphs
'''

from modules import node
from modules.open_digraph_mixins.open_digraph_composition_mx import open_digraph_composition_mx
from modules.open_digraph_mixins.open_digraph_factory_mx import open_digraph_factory_mx
from modules.open_digraph_mixins.open_digraph_io_mx import open_digraph_io_mx
from modules.open_digraph_mixins.open_digraph_paths_mx import open_digraph_paths_mx

class open_digraph(open_digraph_composition_mx, open_digraph_factory_mx, open_digraph_io_mx, open_digraph_paths_mx):
    '''
    Open directed graph. Distinguished input nodes (no parents) and output nodes (no children)
    '''


    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self._inputs = inputs
        self._outputs = outputs
        self._nodes = {node.get_id():node for node in nodes} # self.nodes: <int,node> dict


    def get_input_ids(self):
        return self._inputs
    

    def set_inputs(self, inputs):
        self._inputs = inputs


    def add_input_id(self, identity):
        '''
        identity: int;
        Adds the node with the given id a an input to the graph.
        '''
        if identity not in self.get_node_ids():
            raise ValueError("The provided id does not correspond to a node of the graph")
        
        self._inputs.append(identity)


    def get_output_ids(self):
        return self._outputs
    

    def set_outputs(self, outputs):
        self._outputs = outputs


    def add_output_id(self, identity):
        '''
        identity: int;
        Adds the node with the given id as an output to the graph.
        '''
        if identity not in self.get_node_ids():
            raise ValueError("The provided id does not correspond to a node of the graph")
        self._outputs.append(identity)


    def get_node_map(self):
        return self._nodes
    

    def get_nodes(self):
        return list(self._nodes.values())
    

    def get_node_ids(self):
        return list(self._nodes.keys())
    

    def get_node_by_id(self, id):
        return self._nodes[id]
    

    def get_nodes_by_ids(self, id_list):
        return map(self.get_node_by_id, id_list) 
    
    
    def new_id(self):
        '''
        Returns an id that is not currently used in the graph
        '''
        return max([-1] + self.get_node_ids()) + 1

    
    def add_edge(self, src, tgt):
        '''
        src: int; id of the source node
        tgt: int; id of the target node
        Adds an edge between the source and the target
        '''
        if src in self._outputs or tgt in self._inputs:
            raise ValueError("This edge cannot be added while maintaining input and output nodes")
        
        self.get_node_by_id(src).add_child_id(tgt)
        self.get_node_by_id(tgt).add_parent_id(src)


    def add_edges(self, edges):
        '''
        edges: int list list; list of pairs of source and target Nodes
        Vectorised version of add_edge
        '''
        for pair in edges:
            self.add_edge(pair[0], pair[1])

    
    def add_node(self, label="", parents=None, children=None):
        '''
        Adds a node to a graph.
        '''
        if parents == None:
            parents = {}

        if children == None:
            children = {}

        new_id = self.new_id()
        new_node = node.node(new_id, label, parents, children)
        
        self._nodes[new_id] = new_node

        self.add_edges([[parent, new_id] for parent in parents for i in range(parents[parent])])
        self.add_edges([[new_id, child] for child in children for i in range(children[child])])


        return new_node.get_id()


    def remove_edge(self, src, tgt):
        '''
        src: int; id of the source node
        tgt: int; id of the target node
        Removes the edge between the given nodes
        '''
        self._nodes[src].remove_child_once(tgt)
        self._nodes[tgt].remove_parent_once(src)


    def remove_edges(self, edges):
        '''
        edges: int list list; list of pairs of edges
        Removes the specified edges (once) between the given nodes
        '''
        for pair in edges:
            self.remove_edge(pair[0], pair[1])


    def remove_parallel_edges(self, src, tgt):
        '''
        src: int; id of the source node
        tgt: int; id of the target node
        Removes all edges between the given nodes
        '''
        self._nodes[src].remove_child_id(tgt)
        self._nodes[tgt].remove_parent_id(src)


    def remove_several_parallel_edges(self, node_pairs):
        '''
        node_pairs: int list list; list of pairs of edges
        Removes all edges between the given nodes
        '''
        for pair in node_pairs:
            self.remove_parallel_edges(pair[0], pair[1])


    def remove_node_by_id(self, id):
        '''
        id: int; unique id of the node to be removed
        Removes a given node from a graph
        '''
        n = self._nodes[id]
        parents = [p for p in n.get_parents()]
        children = [c for c in n.get_children()]
        for parent in parents:
            self.remove_parallel_edges(parent, id)
        for child in children:
            self.remove_parallel_edges(id, child)

        del self._nodes[id]


    def remove_nodes_by_id(self, id_list):
        '''
        id_list: int list; list of ids of nodes to be removed
        Removes the nodes with the given ids from the graph
        '''
        ids = [id for id in id_list]
        for id in ids:
            self.remove_node_by_id(id)


    def is_cyclic(self):
        '''
        Returns True if the graph is cyclic, False otherwise
        '''
        copied_graph = self.copy()
        while copied_graph.get_nodes() != []:
            cyclic = True
            for n in copied_graph.get_nodes():
                if n.outdegree() == 0:
                    copied_graph.remove_node_by_id(n.get_id())
                    cyclic = False
                    break

            if cyclic:
                return True

        return False


    def is_well_formed(self):
        '''
        Verifies if an Open Directed Graph is well defined.
        - Each input and output node must be in the graph
        - Each input node must have a single child (of multiplicity 1) and no parent
        - Each output node must have a single parent (of multiplicity 1) and no children
        - Each key in nodes corresponds to a node which has the key as id
        - If j has i as a child, with multiplicity m, then i must have j as a parent, 
        with multiplicity m (and viceversa)
        '''
        c1 = all(input_id in self.get_node_ids() for input_id in self._inputs)

        c2 = all(output_id in self.get_node_ids() for output_id in self._outputs)

        c3 = all(len(self._nodes[input_id].get_children()) == 1 and
                len(self._nodes[input_id].get_parents()) == 0 for input_id in self._inputs)
        
        c4 = all(len(self._nodes[output_id].get_children()) == 0 and
                len(self._nodes[output_id].get_parents()) == 1 for output_id in self._outputs)
        
        c5 = all(n.get_id() == id for id, n in self._nodes.items())

        for n in self.get_nodes():
            for parent_id in n.get_parents():
                if not(parent_id in self.get_node_ids()):
                    return False
        
                parent = self._nodes[parent_id]

                if not(n.get_id() in parent.get_children().keys()) or n.get_parents()[parent_id] != parent.get_children()[n.get_id()]:
                    return False
            
            for child_id in n.get_children():
                if not(child_id in self.get_node_ids()):
                    return False
        
                child = self._nodes[child_id]

                if not(n.get_id() in child.get_parents().keys()) or n.get_children()[child_id] != child.get_parents()[n.get_id()]:
                    return False

        return c1 and c2 and c3 and c4 and c5
    

    def adjacency_matrix(self):
        # To be completed. Exercice 9 of 3rd session.
        raise NotImplementedError()

    
    def min_id(self):
        '''
        Returns the minimum id of the graph's nodes
        '''
        return min(self.get_node_ids())
    

    def max_id(self):
        '''
        Returns the maximum id of the graph's nodes
        '''
        return max(self.get_node_ids())
    

    def shift_indices(self, n):
        '''
        n: int; number by which to translate all indices (could be negative)
        Shifts the indices of all nodes inside a graph
        '''
        self._inputs = [inp + n for inp in self._inputs]
        self._outputs = [outp + n for outp in self._outputs]

        for node in self.get_nodes():
            node.set_id(node.get_id() + n)
            node.set_parents({key + n : value for key, value in node.get_parents().items()})
            node.set_children({key + n : value for key, value in node.get_children().items()})

        self._nodes = {node.get_id():node for node in self.get_nodes()}
    

    def merge_nodes(self, node_id1, node_id2):
        '''
        Merges two nodes in the graph.
        
        Args:
            node_id1 (int): The id of the first node to merge.
            node_id2 (int): The id of the second node to merge.

        Returns:
            int: The id of the merged node.
        '''
        node1 = self.get_node_by_id(node_id1)
        node2 = self.get_node_by_id(node_id2)

        new_label = input("Enter the label for the merged node: ")

        merged_parents = {**node1.get_parents(), **node2.get_parents()}
        merged_children = {**node1.get_children(), **node2.get_children()}

        merged_node_id = self.add_node(label=new_label, parents=merged_parents, children=merged_children)

        self.remove_node_by_id(node_id1)
        self.remove_node_by_id(node_id2)

        return merged_node_id
    
    
    def copy(self):
        '''
        Creates a copy of the graph.
        
        Returns:
            open_digraph: A copy of the graph.
        '''
        new_nodes = [node.copy() for node in self.get_nodes()]
        return open_digraph(self._inputs, self._outputs, new_nodes)

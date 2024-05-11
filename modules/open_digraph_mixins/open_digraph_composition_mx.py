'''
Mixin for composition of open directed graphs
'''

class open_digraph_composition_mx:
    def iparallel(self, g):
            '''
            g: open_digraph; graph to be composed in parallel with self
            Modifies the current graph by composing it in parallel with the graph passed as a parameter
            '''
            g = g.copy()
            if self.get_nodes() != [] and g.get_nodes() != []:
                g.shift_indices(self.max_id() - g.min_id() + 1)

            self._inputs.extend(g.get_input_ids())
            self._outputs.extend(g.get_output_ids())

            for id, node in g.get_node_map().items():
                self._nodes[id] = node

    @classmethod
    def parallel(cls, g1, g2):
        '''
        g1: open_digraph; first graph of composition
        g2: open_digraph; second graph of composition
        Returns the parallel composition of the parameter graphs
        Note that the operation is not strictly commutative, but will return isomorphic graphs
        '''
        composition = g1.copy()
        composition.iparallel(g2)
        return composition
    
    
    def icompose(self, f):
        '''
        f: open_digraph; graph to be composed sequentially with self
        Modifies the current graph by composing it (if possible) in sequence with the graph passed as a parameter
        '''
        if len(self.get_input_ids()) != len(f.get_output_ids()):
            raise ValueError("Number of inputs of the first graph does not match the number of outputs of the second graph.")
        
        f = f.copy()

        if self.get_nodes() != [] and f.get_nodes() != []:
            self.shift_indices(f.max_id() - self.min_id() + 1)
        
        for id, node in f.get_node_map().items():
            self._nodes[id] = node.copy()


        prev_inputs = self.get_input_ids()
        self._inputs = f.get_input_ids()
        for input_id, output_id in zip(prev_inputs, f.get_output_ids()):
            self.add_edge(output_id, input_id)


    @classmethod
    def compose(cls, g1, g2):
        '''
        g1: open_digraph; first graph of composition
        g2: open_digraph; second graph of composition
        Returns the composition of the parameter graphs
        Note that the operation is not strictly commutative
        '''
        g1 = g1.copy()
        g1.icompose(g2)
        return g1
    
    @classmethod
    def identity(cls, n):
        '''
        n: int; number of children
        Creates an open_digraph representing the identity over n children.
        '''
        identity_graph = cls.empty()
        for i in range(n):
            node_id = identity_graph.add_node(label=f"Identity_{i}")
            identity_graph.add_edge(node_id, node_id)
        identity_graph.set_inputs(list(range(n)))
        identity_graph.set_outputs(list(range(n)))
        return identity_graph
'''
Mixin containing IO implementation for open directed graphs
'''

class open_digraph_io_mx:
    def save_as_dot_file(self, path, verbose = False):
        '''
        path: str; location of the future .dot file.
        Save a graph as a .dot file
        '''
        res = "digraph G {\n"
        
        if verbose:
            for n in self.get_nodes():
                res += f"v{n.get_id()}[label=\"{n.get_id()}: {n.get_label()}\"];\n"
                
        for n in self.get_nodes():
            for c in self.get_nodes_by_ids(n.get_children()):
                res += f"v{n.get_id()} -> v{c.get_id()};\n"
        res += "}"
        
        with open(path, "w") as f:
            f.write(res)
            

    def from_dot_file(self, path):
        '''
        path: str; location of the .dot file from which to construct graph
        Creates a graph from a .dot file
        '''
        raise NotImplementedError()
    

    def __str__ (self):
        return str([str(node) for node in self._nodes])
    
    
    def __repr__ (self):
        return self.__str__()
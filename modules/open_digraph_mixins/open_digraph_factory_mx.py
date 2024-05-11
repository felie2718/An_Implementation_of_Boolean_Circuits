'''
Factory mixin for open directed graphs
'''

from modules.open_digraph_mixins import adjacency_matrices

class open_digraph_factory_mx:
    @classmethod
    def empty(cls):
        return cls([],[],[])
    

    @classmethod
    def random(cls, n, bound, inputs=0, outpus=0, form="free"):
        '''
        n: int; Number of nodes
        bound: int; Maximum number of connections between nodes
        inputs: int; Number of input nodes
        outpus: int; Number of output nodes
        form : str; Specifies the form of the graph to be constructed.
                    This parameter may take any of the following values
            - free: Generates a free graph
            - DAG: Dyrected acyclic graph
            - oriented: No 2-cycles
            - loop-free: No loops
            - undirected: All connections are bidirectional
            - loop-free undirected: All connections are bidirectiona, no loops
        '''
        if form == "free":
            M = adjacency_matrices.random_matrix(n, bound, null_diag=False)
        elif form == "DAG":
            M = adjacency_matrices.random_dag_int_matrix(n, bound, null_diag=True)
        elif form == "oriented":
            M = adjacency_matrices.random_matrix(n, bound, oriented=True)
        elif form == "loop-free":
            M = adjacency_matrices.random_matrix(n, bound, symmetric=True)
        elif form == "undirected":
            M = adjacency_matrices.random_matrix(n, bound, null_diag=False, symmetric=True)
        elif form == "loop-free undirected":
            M = adjacency_matrices.random_matrix(n, bound)
        else:
            raise ValueError(f"Invalid value {form} for form parameter.")

        g = cls.empty()
        for i in range(n):
            g.add_node(label=f"{i}")
        
        for i in range(n):
            for j in range(n):
                for k in range(M[i][j]):
                    g.add_edge(i, j)

        return g

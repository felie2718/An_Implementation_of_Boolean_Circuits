'''
Mixin for open directed graphs containing methods concerning paths between different nodes
'''

class open_digraph_paths_mx:
    def separate_connected_components(self):
        '''
        Separates the circuit into its connected components.
        Returns a list of open_digraph objects representing the connected components.
        '''
        connected_components = []
        visited = set()

        def dfs(node_id, component):
            if node_id not in visited:
                visited.add(node_id)
                component.append(node_id)
                for child_id in self._nodes[node_id].get_children():
                    dfs(child_id, component)
                for parent_id in self._nodes[node_id].get_parents():
                    dfs(parent_id, component)

        for node_id in self.get_node_ids():
            if node_id not in visited:
                component = []
                dfs(node_id, component)
                connected_components.append(component)

        components_graphs = []
        for component in connected_components:
            component_graph = self.__class__.empty()
            for node_id in component:
                node = self.get_node_by_id(node_id)
                component_graph.add_node(label=node.get_label(), parents=node.get_parents(), children=node.get_children())
            components_graphs.append(component_graph)

        return components_graphs


    def dijkstra(self, src, direction=None):
        def get_neighbours(n):
            if direction == None:
                return list(n.get_children().keys()) + list(n.get_parents().keys())
            if direction == -1:
                return list(n.get_parents().keys())
            if direction == 1:
                return list(n.get_children().keys())

        Q = [src]
        dist = {src: 0}
        prev = {}
        while Q != []:
            u = min(Q, key = lambda q: dist[q])
            Q.remove(u)
            neighbours = self.get_nodes_by_ids(get_neighbours(u))
            for n in neighbours:
                if n not in dist:
                    Q.append(n)
                if n not in dist or dist[n] > dist[u] + 1:
                    dist[n] = dist[u] + 1
                    prev[n] = u
        return dist, prev
    
    
    def common_ancestors(self, n1, n2):
        anc1 = self.dijkstra(n1, direction=-1)[0]
        anc2 = self.dijkstra(n2, direction=-1)[0]
        res = {}
        for key in anc1:
            if key in anc2:
                res[key] = (anc1[key], anc2[key])
        return res
    

    def topological_sort(self):
        '''
        Returns the topological sort of the (acyclic) graph, as a list of sets of node numbers
        '''
        copied_graph = self.copy()
        top_sort = []
        leaves = []

        copied_graph.remove_nodes_by_id(copied_graph.get_input_ids())
        copied_graph.remove_nodes_by_id(copied_graph.get_output_ids())

        while copied_graph.get_nodes() != []:
            for n in copied_graph.get_nodes():
                if n.get_parents() == {}:
                    leaves.append(n.get_id())

            top_sort.append(set(leaves))
            copied_graph.remove_nodes_by_id(leaves)
            leaves = []

        return top_sort


    def node_depth(self, n1):
        '''
        Calculates the depth of a given node in the (acyclic) graph
        n1: int; node whose depth is calculated
        Returns the depth of the node in the graph
        '''
        top_sort = self.topological_sort()
        for i in range(len(top_sort)):
            if n1 in top_sort[i]:
                return i + 1
        
        raise ValueError("Invalid node to calculate depth in graph")
    

    def graph_depth(self):
        '''
        Returns the depth of the acyclic open directed graph
        '''
        return len(self.topological_sort())
    

    def longest_path(self, u, v):
        '''
        Calculates the length of the longest path between two nodes (in an acyclic graph)
        u: int; id of the starting node
        v: int; id of the ending node
        Returns the length of the longest path and the last step in the journey
        '''
        top_sort = self.topological_sort()
        k = self.node_depth(u)
        dist = {u: 0}
        prev = {}
        for i in range(k, self.graph_depth()):
            for w in top_sort[i]:
                dist_parents = [parent for parent in self.get_node_by_id(w).get_parents() if parent in dist]
                if dist_parents != []:
                    prev[w] = max(dist_parents, key=lambda p: dist[p])
                    dist[w] = dist[prev[w]] + 1

                if w == v:
                    if v not in dist:
                        raise ValueError(f"Node {v} is not a descendant of {u}")
                    return dist[v], prev[v]

        raise ValueError("Impossible to calculate the distance between the given nodes")
    
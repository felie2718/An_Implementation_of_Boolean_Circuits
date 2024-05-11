'''
Implementation of nodes for graphs
'''

class node:
    '''
    Node inside of a graph
    Nodes only know local information about the graph. Therefore, methods that modify a node's connections in one 
    direction do not do so for the other direction.
    '''


    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
        self._id = identity
        self._label = label
        self._parents = parents
        self._children = children


    def get_id(self):
        return self._id


    def set_id(self, identity):
        '''
        identity: int;
        Sets a nodes id
        '''
        self._id = identity
        

    def get_label(self):
        return self._label
    

    def set_label(self, label):
        '''
        label: string;
        Sets a name (label) for the node
        '''
        self._label = label
    

    def get_parents(self):
        '''
        Returns a node's parents
        '''
        return self._parents
    

    def set_parents(self, parents):
        '''
        Sets the parents of a node
        '''
        self._parents = parents
    

    def add_parent_id(self, identity):
        '''
        indentity: int; unique identifier of the parent node
        Adds a new parent (with the given id) for the given node
        '''
        if identity not in self._parents:
            self._parents[identity] = 0

        self._parents[identity] += 1
    

    def get_children(self):
        '''
        Returns a node's children
        '''
        return self._children
    

    def set_children(self, children):
        '''
        Sets the children of a node
        '''
        self._children = children


    def add_child_id(self, identity):
        '''
        indentity: int; unique identifier of the child node
        Adds a new child (with the given id) for the given node
        '''
        if identity not in self._children:
            self._children[identity] = 0

        self._children[identity] += 1


    def copy(self):
        '''
        Returns an identical copy of a node
        '''
        return node(self._id, self._label, self._parents.copy(), self._children.copy())


    def _remove_once_helper(self, identity, dic):
        
        if identity not in dic:
            raise ValueError("The given node is not a parent")
        
        if dic[identity] == 1:
            del dic[identity]
        
        else:
            dic[identity] -= 1


    def remove_parent_once(self, identity):
        '''
        identity: int; unique id of the parent to be removed
        Removes one connection with the given parent. Fails if the parent is not valid
        '''
        self._remove_once_helper(identity, self._parents)


    def remove_child_once(self, identity):
        '''
        identity: int; unique id of the child to be removed
        Removes one connection with the given child. Fails if the child is not valid
        '''
        self._remove_once_helper(identity, self._children)


    def remove_parent_id(self, identity):
        '''
        identity: int; unique id of the parent to be removed
        Removes all connections with the given parent (mono-directional)
        '''
        if identity in self._parents:
            del self._parents[identity]


    def remove_child_id(self, identity):
        '''
        identity: int; unique id of the child to be removed
        Removes all connections with the given child (mono-directional)
        '''
        if identity in self._children:
            del self._children[identity]


    def indegree(self):
        '''
        Returns the indegree of the node
        '''
        return sum(list(self._parents.values()))
    

    def outdegree(self):
        '''
        Returns the outegree of the node
        '''
        return sum(list(self._children.values()))
    

    def degree(self):
        '''
        Returns the degree of the node
        '''
        return self.indegree() + self.outdegree()
    

    def __str__(self):
        '''
        Conversion of a node to a string
        '''
        return self._label
    
    
    def __repr__ (self):
        '''
        Representation of a node, used when printing        
        '''
        return self.__str__()

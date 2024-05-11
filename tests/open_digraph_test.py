'''
Unit tests for the open_digraph module
'''

import os
import sys
sys.path.insert(0, '..')

import unittest

from modules.open_digraph import *
from modules.node import *

if not(os.path.exists("tmp")):  # Creates empty tmp directory inside of tests if it doesn't already exist    
    os.mkdir("tmp")

class InitTest(unittest.TestCase):
    def test_init_open_digraph(self):
        n0 = node(0, 'i', {}, {})
        n1 = node(1, 'j', {}, {})
        n2 = node(2, 'k', {}, {})
        n3 = node(3, 'l', {}, {})
        gr = open_digraph([1, 2], [4], [n0, n1, n2, n3])
        
        self.assertEqual(gr._inputs, [1, 2])
        self.assertEqual(gr._outputs, [4])
        self.assertEqual(gr._nodes, {0:n0, 1:n1, 2:n2, 3:n3})
        self.assertIsInstance(gr, open_digraph)
        
        
class CopyTest(unittest.TestCase):
    def test_open_digraph_copy(self):
        n0 = node(0, 'i', {}, {})
        n1 = node(1, 'j', {}, {})
        n2 = node(2, 'k', {}, {})
        n3 = node(3, 'l', {}, {})
        gr = open_digraph([1, 2], [4], [n0, n1, n2, n3])
        gr_copy = gr.copy()
        
        self.assertIsNot(gr, gr_copy)
        self.assertNotEqual(gr.get_node_map(), gr_copy.get_node_map()) # Nodes should be copied
        self.assertEqual(gr.get_input_ids(), gr_copy.get_input_ids())
        self.assertEqual(gr.get_output_ids(), gr_copy.get_output_ids())
        

class WellFormedGraphsTest(unittest.TestCase):
    '''
    Test case for the is_well_formed method of open_digraph.
    '''
    def test_empty_graph_is_well_formed(self):
        gr = open_digraph.empty()
        self.assertTrue(gr.is_well_formed())
    
    def test_no_children_input(self):
        n0 = node(0, 'i', {}, {})
        gr = open_digraph([0], [], [n0])
        self.assertFalse(gr.is_well_formed())
        
    def test_one_child_input(self):
        n_in = node(0, 'in', {}, {1:1})
        n = node(1, 'inner_node', {0:1}, {})
        gr = open_digraph([0], [], [n_in, n])
        self.assertTrue(gr.is_well_formed())
        
    def test_two_children_input(self):
        n_in = node(0, 'in', {}, {1:1, 2:1})
        n1 = node(1, 'inner_node', {0:1}, {})
        n2 = node(2, 'inner_node', {0:1}, {})
        gr = open_digraph([0], [], [n_in, n1, n2])
        self.assertFalse(gr.is_well_formed())
        
    def test_input_with_parent(self):
        n0 = node(0, 'i', {1:1}, {})
        n1 = node(0, 'i', {}, {0:1})
        gr = open_digraph([0], [], [n0, n1])
        self.assertFalse(gr.is_well_formed())
        
    def test_two_outputs_one_parent(self):
        n_out1= node(0, 'out1', {2:1}, {})
        n_out2 = node(1, 'out2', {2:2}, {}) # Double connection
        n = node(2, 'inner', {}, {0:1, 1:2})
        gr = open_digraph([], [0, 1], [n_out1, n_out2, n])
        self.assertTrue(gr.is_well_formed())
        
    def test_one_child_output(self):
        n_out = node(0, 'out', {1:1}, {})
        n = node(1, 'inner_node', {}, {0:1})
        gr = open_digraph([], [0], [n_out, n])
        self.assertTrue(gr.is_well_formed())
    

class DotFileGenerationTest(unittest.TestCase):
    def test_dotfile_created(self):
            
        path = "tmp/temporary_test_graph.dot"
        open_digraph.empty().save_as_dot_file(path, verbose=True)
        result = os.path.exists(path)
        if result:
            os.remove(path)
        self.assertTrue(result)
        
        
class RandomGraphGenerationTest(unittest.TestCase):
    def test_free_is_well_formed(self):
        self.assertTrue(open_digraph.random(5, 3).is_well_formed())
        
    def test_dag_is_well_formed(self):
        self.assertTrue(open_digraph.random(5, 3, form="DAG").is_well_formed())
        
    def test_oriented_is_well_formed(self):
        self.assertTrue(open_digraph.random(5, 3, form="oriented").is_well_formed())
        
    def test_loop_free_is_well_formed(self):
        self.assertTrue(open_digraph.random(5, 6, form="loop-free").is_well_formed())
        
    def test_loop_free_undirected_is_well_formed(self):
        self.assertTrue(open_digraph.random(5, 3, form="loop-free undirected").is_well_formed())
    
    def test_loop_undirected_is_well_formed(self):
        self.assertTrue(open_digraph.random(4, 3, form="undirected").is_well_formed())
        
    def test_invalid_form_fails(self):
        with self.assertRaises(ValueError):
            open_digraph.random(4, 4, form="invalid")



class EdgeRemovalTest(unittest.TestCase):
    '''
    Tests for the removal of edges within open directed graphs
    '''
    def setUp(self):
        n0 = node(0, '1-0', {}, {3:1})
        n1 = node(1, '1-1', {}, {3:1})
        n2 = node(2, '1-2', {}, {4:1})
        n3 = node(3, '1-3', {0:1, 1:1}, {5:1})
        n4 = node(4, '1-4', {2:1}, {5:1, 6:2})
        n5 = node(5, '1-5', {3:1, 4:1}, {})
        n6 = node(6, '1-6', {4:2}, {})
        self.gr = open_digraph([0, 1, 2], [5, 6], [n0, n1, n2, n3, n4, n5, n6])

    def test_remove_edge(self):
        self.gr.remove_edge(4, 5)
        self.assertEqual(self.gr.get_node_by_id(4).get_children(), {6:2})
        self.assertEqual(self.gr.get_node_by_id(5).get_parents(), {3:1})

    def test_remove_parallel_edges(self):
        self.gr.remove_parallel_edges(4, 6)
        self.assertEqual(self.gr.get_node_by_id(4).get_children(), {5:1})
        self.assertEqual(self.gr.get_node_by_id(6).get_parents(), {})

    def test_remove_several_parallel_edges(self):
        self.gr.remove_several_parallel_edges([[4, 6], [1, 3]])
        self.assertEqual(self.gr.get_node_by_id(4).get_children(), {5:1})
        self.assertEqual(self.gr.get_node_by_id(6).get_parents(), {})
        self.assertEqual(self.gr.get_node_by_id(1).get_children(), {})
        self.assertEqual(self.gr.get_node_by_id(3).get_parents(), {0:1})



class NodeRemovalTest(unittest.TestCase):
    '''
    Tests for node removal within open directed graphs
    '''
    def setUp(self):
        n0 = node(0, '1-0', {}, {3:1})
        n1 = node(1, '1-1', {}, {3:1})
        n2 = node(2, '1-2', {}, {4:1})
        n3 = node(3, '1-3', {0:1, 1:1}, {5:1})
        n4 = node(4, '1-4', {2:1}, {5:1, 6:2})
        n5 = node(5, '1-5', {3:1, 4:1}, {})
        n6 = node(6, '1-6', {4:2}, {})
        self.gr = open_digraph([0, 1, 2], [5, 6], [n0, n1, n2, n3, n4, n5, n6])
    
    def test_remove_input(self):
        self.gr.remove_node_by_id(0)
        self.assertEqual(set(self.gr.get_node_ids()), set([1, 2, 3, 4, 5, 6]))
        self.assertEqual(self.gr.get_node_by_id(3).get_parents(), {1:1})

    def test_remove_output(self):
        self.gr.remove_node_by_id(5)
        self.assertEqual(set(self.gr.get_node_ids()), set([1, 2, 3, 4, 0, 6]))
        self.assertEqual(self.gr.get_node_by_id(3).get_children(), {})


    def test_remove_inner_node(self):
        self.gr.remove_node_by_id(3)
        self.assertEqual(set(self.gr.get_node_ids()), set([1, 2, 0, 4, 5, 6]))
        self.assertEqual(self.gr.get_node_by_id(1).get_children(), {})

    def test_remove_multiple_nodes(self):
        self.gr.remove_nodes_by_id([0, 3])
        self.assertEqual(set(self.gr.get_node_ids()), set([1, 2, 4, 5, 6]))
        self.assertEqual(self.gr.get_node_by_id(1).get_children(), {})
        self.assertEqual(self.gr.get_node_by_id(5).get_parents(), {4:1})


class CompositionTest(unittest.TestCase):
    '''
    Barebone for composition tests for both parallel and sequential composition (they require the same setup)
    '''
    def setUp(self):
        '''
        Graphs to be composed in the tests. Realistic examples
        '''
        n0 = node(0, '1-0', {}, {3:1})
        n1 = node(1, '1-1', {}, {3:1})
        n2 = node(2, '1-2', {}, {4:1})
        n3 = node(3, '1-3', {0:1, 1:1}, {5:1})
        n4 = node(4, '1-4', {2:1}, {5:1, 6:2})
        n5 = node(5, '1-5', {3:1, 4:1}, {})
        n6 = node(6, '1-6', {4:2}, {})
        self.gr1 = open_digraph([0, 1, 2], [5, 6], [n0, n1, n2, n3, n4, n5, n6])

        n0 = node(0, '2-0', {}, {2:1, 3:1})
        n1 = node(1, '2-1', {}, {4:1})
        n2 = node(2, '2-2', {0:1}, {})
        n3 = node(3, '2-3', {0:1}, {5:1})
        n4 = node(4, '2-4', {1:1}, {5:1})
        n5 = node(5, '2-5', {3:1, 4:1}, {})
        self.gr2 = open_digraph([0, 1], [5], [n0, n1, n2, n3, n4, n5])


class ParallelCompositionTest(CompositionTest):
    def test_iparallel(self):
        self.gr1.iparallel(self.gr2)
        self.assertTrue(self.gr1.get_input_ids() == [0, 1, 2, 7, 8])
        self.assertTrue(self.gr1.get_output_ids() == [5, 6, 12])
        self.assertTrue(self.gr1.get_node_ids() == [i for i in range(13)])
        self.assertTrue(self.gr1.get_node_by_id(0).get_children() == {3:1})
        self.assertTrue(self.gr1.get_node_by_id(10).get_parents() == {7:1})

        self.assertTrue(self.gr2.get_node_ids() == [0, 1, 2, 3, 4, 5]) # Check that the second graph was not modified
        
    def test_parallel(self):
        composition = open_digraph.parallel(self.gr1, self.gr2)
        self.assertTrue(composition.get_input_ids() == [0, 1, 2, 7, 8])
        self.assertTrue(composition.get_output_ids() == [5, 6, 12])
        self.assertTrue(composition.get_node_by_id(0).get_children() == {3:1})
        self.assertTrue(composition.get_node_by_id(10).get_parents() == {7:1})

        # Check that the original graphs were not modified
        self.assertTrue(self.gr1.get_node_ids() == [0, 1, 2, 3, 4, 5, 6])
        self.assertTrue(self.gr2.get_node_ids() == [0, 1, 2, 3, 4, 5]) 

    def test_iparallel_neutral(self):
        prev_map = self.gr1.get_node_map()
        self.gr1.iparallel(open_digraph.empty())
        self.assertTrue(self.gr1.get_node_map() == prev_map)


class SequentialCompositionTest(CompositionTest):
    def test_icomposition(self):
        self.gr2.icompose(self.gr1)
        self.assertTrue(set(self.gr2.get_node_ids()) == set([i for i in range(13)]))
        self.assertTrue(self.gr2.get_input_ids() == self.gr1.get_input_ids())
        self.assertTrue(self.gr2.get_output_ids() == [12])

        self.assertTrue(self.gr2.get_node_by_id(7).get_parents() == {5:1})
        self.assertTrue(self.gr2.get_node_by_id(8).get_parents() == {6:1})

        self.assertTrue(self.gr2.get_node_by_id(5).get_children() == {7:1})
        self.assertTrue(self.gr2.get_node_by_id(6).get_children() == {8:1})

        # Check that the input graph was not modified
        self.assertTrue(self.gr1.get_node_ids() == [i for i in range(7)]) 
        self.assertTrue(self.gr1.get_node_by_id(5).get_children() == {})

    def test_icomposition_invalid(self):
        with self.assertRaises(ValueError):
            self.gr1.icompose(self.gr1)

        with self.assertRaises(ValueError):
            self.gr2.icompose(open_digraph.empty())

    def test_composition(self):
        prev_input_ids = self.gr1.get_input_ids()
        gr = open_digraph.compose(self.gr2, self.gr1)
        self.assertTrue(set(gr.get_node_ids()) == set([i for i in range(13)]))
        self.assertTrue(gr.get_input_ids() == prev_input_ids)
        self.assertTrue(gr.get_output_ids() == [12])

        self.assertTrue(gr.get_node_by_id(7).get_parents() == {5:1})
        self.assertTrue(gr.get_node_by_id(8).get_parents() == {6:1})

        self.assertTrue(gr.get_node_by_id(5).get_children() == {7:1})
        self.assertTrue(gr.get_node_by_id(6).get_children() == {8:1})

    def test_composition_invalid(self):
        with self.assertRaises(ValueError):
            open_digraph.compose(self.gr1, self.gr1)

        with self.assertRaises(ValueError):
            open_digraph.compose(self.gr2, open_digraph.empty())



class DijkstraTest(unittest.TestCase):
    '''
    Tests for Dijkstra's shortest path algorithm
    '''
    def setUp(self):
        n0 = node(0, '1-0', {}, {3:1})
        n1 = node(1, '1-1', {}, {3:1})
        n2 = node(2, '1-2', {}, {4:1})
        n3 = node(3, '1-3', {0:1, 1:1}, {5:1})
        n4 = node(4, '1-4', {2:1}, {5:1, 6:2})
        n5 = node(5, '1-5', {3:1, 4:1}, {})
        n6 = node(6, '1-6', {4:2}, {})
        self.gr = open_digraph([0, 1, 2], [5, 6], [n0, n1, n2, n3, n4, n5, n6])

    # Helper function to simplify tests
    def _helper(self, exp, exp_prev):
        return ({self.gr.get_node_by_id(id): val for id, val in exp.items()},
                {self.gr.get_node_by_id(id): self.gr.get_node_by_id(val) for id, val in exp_prev.items()})

    def test_dijkstra_full(self):
        result = self.gr.dijkstra(self.gr.get_node_by_id(0))
        expected = self._helper({0: 0, 1: 2, 2: 4, 3: 1, 4: 3,  5: 2, 6: 4}, {1: 3, 2: 4, 3: 0, 4: 5, 5: 3, 6: 4})
        self.assertEqual(result, expected)

    def test_dijkstra_parents(self):
        result = self.gr.dijkstra(self.gr.get_node_by_id(3), direction=-1)
        expected = self._helper({0: 1, 1: 1, 3: 0}, {0: 3, 1: 3})
        self.assertEqual(result, expected)

    def test_dijkstra_children(self):
        result = self.gr.dijkstra(self.gr.get_node_by_id(2), direction=1)
        expected = self._helper({2: 0, 4: 1, 5: 2, 6: 2}, {4: 2, 5: 4, 6: 4})
        self.assertEqual(result, expected)

    def test_common_ancestors(self):
        result = self.gr.common_ancestors(self.gr.get_node_by_id(5), self.gr.get_node_by_id(4))
        expected = {self.gr.get_node_by_id(4): (1, 0), self.gr.get_node_by_id(2): (2, 1)}
        self.assertEqual(result, expected)

    def test_common_ancestors_empty(self):
        result = self.gr.common_ancestors(self.gr.get_node_by_id(6), self.gr.get_node_by_id(3))
        self.assertEqual(result, {})


class TopologicalSortTest(unittest.TestCase):
    '''
    Tests for the topological sort of open directed graphs.
    '''
    def setUp(self):
        n0 = node(0, '1-0', {}, {3:1, 5:1})
        n1 = node(1, '1-1', {}, {3:1})
        n2 = node(2, '1-2', {}, {4:1})
        n3 = node(3, '1-3', {0:1, 1:1}, {5:1})
        n4 = node(4, '1-4', {2:1}, {5:1, 6:2})
        n5 = node(5, '1-5', {3:1, 4:1}, {})
        n6 = node(6, '1-6', {4:2}, {})
        self.gr = open_digraph([1], [6], [n0, n1, n2, n3, n4, n5, n6])

    def test_empty_topological_sort(self):
        self.assertEqual(open_digraph.empty().topological_sort(), [])

    def test_topological_sort(self):
        self.assertEqual(self.gr.topological_sort(), [set([0, 2]), set([3, 4]), set([5])])

    def test_depth_node(self):
        self.assertEqual(self.gr.node_depth(3), 2)
        self.assertEqual(self.gr.node_depth(0), 1)
        self.assertEqual(self.gr.node_depth(5), 3)
        with self.assertRaises(ValueError):
            self.gr.node_depth(1)

    def test_graph_depth(self):
        self.assertEqual(self.gr.graph_depth(), 3)
        self.assertEqual(open_digraph.empty().graph_depth(), 0)

    def test_longest_path(self):
        self.assertEqual(self.gr.longest_path(0, 5), (2, 3))

if __name__ == '__main__': 
    unittest.main() 

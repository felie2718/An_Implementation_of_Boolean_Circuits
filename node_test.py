'''
Unit tests for the node module
'''

import unittest

import sys
sys.path.insert(0, '..')

from modules.node import *

class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0._id, 0)
        self.assertEqual(n0._label, 'i')
        self.assertEqual(n0._parents, {})
        self.assertEqual(n0._children, {1:1})
        self.assertIsInstance(n0, node)

class CopyTest(unittest.TestCase):
    def test_node_copy(self):  
        n0 = node(1, "Test Node", {1: 2}, {6: 2})
        n0_copy = n0.copy()  
        self.assertIsNot(n0, n0_copy)
        self.assertEqual(n0.get_id(), n0_copy.get_id())
        self.assertEqual(n0.get_label(), n0_copy.get_label())
        self.assertEqual(n0.get_children(), n0_copy.get_children())
        self.assertEqual(n0.get_parents(), n0_copy.get_parents())


if __name__ == '__main__': 
    unittest.main() 
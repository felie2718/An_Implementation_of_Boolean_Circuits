'''
Unit tests for boolean circuits
'''

import unittest

import sys
sys.path.insert(0, '..')

from modules.bool_circ import *

class TestBoolCirc(unittest.TestCase):

    def test_well_formedness(self):
        well_formed_circuit = bool_circ()
        self.assertTrue(well_formed_circuit.is_well_formed())

    def test_random_circuit(self):
        random_circuit = bool_circ.random_bool_circ(10, 5)
        self.assertTrue(random_circuit.is_well_formed())

    def test_register(self):
        register_circuit = bool_circ.register(42, 8)
        self.assertTrue(register_circuit.is_well_formed())
        output_values = [node.get_label() for node in register_circuit.get_nodes() if node in register_circuit.get_output_ids()]
        expected_values = list(bin(42)[2:].zfill(8))
        self.assertEqual(output_values, expected_values)
        
    def test_evaluate(self):
        g = bool_circ()
        input1 = g.add_node(label='1')
        input2 = g.add_node(label='1')
        and_gate = g.add_node(label='&')
        output = g.add_node(label='')

        g.add_edge(input1, and_gate)
        g.add_edge(input2, and_gate)
        g.add_edge(and_gate, output)

        g.evaluate()

        expected_output = '1'
        actual_output = g.get_node_by_id(output).get_label()
        self.assertEqual(actual_output, expected_output)
        
    
def test_half_adder(self):
        half_adder = bool_circ()
        input_A = half_adder.add_node(label='1')
        input_B = half_adder.add_node(label='1')
        xor_gate = half_adder.add_node(label='^')
        and_gate = half_adder.add_node(label='&')

        half_adder.add_edge(input_A, xor_gate)
        half_adder.add_edge(input_B, xor_gate)
        half_adder.add_edge(input_A, and_gate)
        half_adder.add_edge(input_B, and_gate)

        half_adder.evaluate()

        output_sum = half_adder.get_node_by_id(xor_gate).get_label()
        output_carry = half_adder.get_node_by_id(and_gate).get_label()
        self.assertTrue(output_sum == 0 and output_carry == 1)



if __name__ == '__main__':
    unittest.main()
import unittest

import sys
sys.path.insert(0, '..')

from modules.bool_circ import *

class TestBoolCirc(unittest.TestCase):

    def test_well_formedness(self):
        well_formed_circuit = bool_circ()
        self.assertTrue(well_formed_circuit.is_well_formed())

    def test_random_circuit(self):
        random_circuit = bool_circ.random_bool_circ(10, 5)
        self.assertTrue(random_circuit.is_well_formed())

    def test_register(self):
        register_circuit = bool_circ.register(42, 8)
        self.assertTrue(register_circuit.is_well_formed())
        output_values = [node.get_label() for node in register_circuit.get_nodes() if node in register_circuit.get_output_ids()]
        expected_values = list(bin(42)[2:].zfill(8))
        self.assertEqual(output_values, expected_values)
        
    def test_evaluate(self):
        adder_circuit = bool_circ.adder(4)
        input_values = ['1', '0', '1', '1']
        input_ids = adder_circuit.get_input_ids()
        for i, value in zip(input_ids, input_values):
            adder_circuit.get_node_by_id(i).set_label(value)
        adder_circuit.evaluate()
        output_ids = adder_circuit.get_output_ids()
        output_values = [adder_circuit.get_node_by_id(node_id).get_label() for node_id in output_ids]
        expected_output_values = ['0', '1', '1', '1', '0']
        self.assertEqual(output_values, expected_output_values)

if __name__ == '__main__':
    unittest.main()

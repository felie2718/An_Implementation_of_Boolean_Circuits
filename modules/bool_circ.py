'''
Boolean circuits, defined as a subclass of open_digraphs
'''

import random

from modules.open_digraph import open_digraph

class bool_circ(open_digraph):
    valid_signs = ['&', '|', ' ', '~', '^', '', '0', '1']

    def __init__(self, g=None):
        if g == None:
            g = open_digraph.empty()
        else:
            g = g.copy()
        self._nodes = g.get_node_map()
        self._inputs = g.get_input_ids()
        self._outputs = g.get_output_ids()
        #if not(self.is_well_formed()):
        #   raise ValueError("The given graph is not a valid boolean circuit")
    
    
    def is_well_formed(self):
        '''
    Checks if the boolean circuit is well-formed.

    Verifies whether the boolean circuit meets the criteria for being well-formed:
    - No cycles exist in the circuit.
    - Each node has a valid label representing a boolean operation, input, output, or space.
    - Each node has the correct number of parents and children according to its label.

    Returns:
        bool: True if the circuit is well-formed, False otherwise.
    '''
        if not(super().is_well_formed()):
            return False
        
        if self.is_cyclic():
            return False
        
        for node in self.get_nodes():
            if node.get_label() == ' ' or node.get_label() != '~':
                if node.indegree() != 1:
                    return False
                
            if node.get_label() not in bool_circ.valid_signs and node.get_label() not in ['0', '1', '^']:
                return False
        
        return True
    
    
    @classmethod
    def parse_formulas(cls, *args):
        '''
    Parses boolean formulas into a boolean circuit.

    Constructs a boolean circuit by parsing one or more boolean formulas provided as arguments.

    Parameters:
        *args (str): One or more boolean formulas to parse into the circuit.

    Returns:
        tuple: A tuple containing the parsed boolean circuit and the variables found in the formulas.
    '''
        g = bool_circ.empty()
        current_node_ids = []
        variables = []

        for formula in args:
            current_node_id = g.add_node(label='')
            s2 = ''
            open_brackets = 0

            for char in formula:
                if char == '(':
                    if open_brackets == 0:
                        if s2.strip() != '':
                            raise ValueError("Invalid formula: unexpected opening bracket")
                        continue
                    else:
                        s2 += char
                    open_brackets += 1
                elif char == ')':
                    if open_brackets == 0:
                        raise ValueError("Invalid formula: unexpected closing bracket")
                    elif open_brackets == 1:
                        if s2.strip() == '':
                            raise ValueError("Invalid formula: empty expression within brackets")
                        g.get_node_by_id(current_node_id).set_label(g.get_node_by_id(current_node_id).get_label() + s2)
                        parent_id = list(g.get_node_by_id(current_node_id).get_parents().keys())[0]
                        current_node_id = parent_id
                        s2 = ''
                    else:
                        s2 += char
                    open_brackets -= 1
                elif char.isalpha():
                    variables.append(char)
                    s2 += ' '
                else:
                    s2 += char
            
            if open_brackets != 0:
                raise ValueError("Invalid formula: unclosed brackets")
            
            g.get_node_by_id(current_node_id).set_label(g.get_node_by_id(current_node_id).get_label() + s2)
            current_node_ids.append(current_node_id)

        output_node_id = g.add_node(label='')
        for node_id in current_node_ids:
            g.add_edge(node_id, output_node_id)

        return bool_circ(g), variables
    

    @classmethod
    def random_bool_circ(cls, n, bound):
        '''
    Generates a random boolean circuit.

    Constructs a random boolean circuit with the specified number of nodes and a given bound for multiplicity.

    Parameters:
        n (int): The number of nodes in the circuit.
        bound (int): The upper bound for the multiplicity of edges.

    Returns:
        bool_circ: A randomly generated boolean circuit.
    '''
        binary_operators = ["&", "|", "^"]
        random_DAG = open_digraph.random(n, bound, 0, 0, form="DAG")
        nodes = [node for node in random_DAG.get_nodes()]

        for node in nodes:
            if node.get_parents() == {}:
                new_in = random_DAG.add_node("", children={node.get_id():1})
                random_DAG.set_inputs(random_DAG.get_input_ids() + [new_in])
            if node.get_children() == {}:
                new_out = random_DAG.add_node("", parents={node.get_id():1})
                random_DAG.set_outputs(random_DAG.get_output_ids() + [new_out])
        
        for node in nodes:
            if node.indegree() == 1 and node.outdegree() == 1:
                node.set_label("~")
            elif node.indegree() == 1 and node.outdegree() > 1:
                node.set_label(" ")
            elif node.outdegree() > 1 and node.indegree() == 1:
                node.set_label(random.choice(binary_operators))
            elif node.outdegree() > 1 and node.indegree() > 1:
                new = random_DAG.add_node(" ", children={nd: ch for nd, ch in node.get_children().items()})
                node.set_children({})
                node.set_label(random.choice(binary_operators))
                random_DAG.add_edge(node.get_id(), new)
            else:
                node.set_label(random.choice(binary_operators))

        return bool_circ(random_DAG)
    

    @classmethod
    def adder(cls, n, half=False):
        '''
    Generates a boolean circuit for binary addition.

    Constructs a boolean circuit representing binary addition with the specified number of bits. Optionally, if `half` is True, it generates a circuit for the upper half of the binary addition.

    Parameters:
        n (int): The number of bits for the binary addition.
        half (bool, optional): If True, generates a circuit for the upper half of the binary addition. Defaults to False.

    Returns:
        bool_circ: A boolean circuit representing the binary addition operation.
    '''
        if n == 0:
            return cls.__adder_basecase(half=half)
        
        prev = cls.adder(n-1, half=half)
        comp = open_digraph.parallel(prev, prev.copy())

        c_in = comp.get_input_ids()[len(comp.get_input_ids()) // 2 - 1]
        c_out = comp.get_output_ids()[len(comp.get_output_ids()) // 2 + 1]

        comp.set_inputs([inp for inp in comp.get_input_ids() if inp != c_in])
        comp.set_outputs([out for out in comp.get_output_ids() if out != c_out])

        comp.add_edge(c_out, c_in) 
        
        size = len(comp.get_input_ids())

        for i in range(size // 4, size // 2):
            inp1 = comp.get_input_ids()[i]
            inp2 = comp.get_input_ids()[size//2 + i]
            inner1 = list(comp.get_node_by_id(inp1).get_children().keys())[0]
            inner2 = list(comp.get_node_by_id(inp2).get_children().keys())[0]
            comp.remove_edge(inp1, inner1)
            comp.add_edge(inp1, inner2)
            comp.remove_edge(inp2, inner2)
            comp.add_edge(inp2, inner1) 

        return bool_circ(comp)


    @classmethod
    def __adder_basecase(cls, half=False):
        '''
    Generates the base case of the binary adder circuit.

    Constructs a boolean circuit representing the base case of binary addition with two input bits and two output bits.

    Parameters:
        half (bool, optional): If True, generates a circuit for the upper half of the binary addition. Defaults to False.

    Returns:
        bool_circ: A boolean circuit representing the base case of binary addition.
    '''
        gr = open_digraph.empty()

        # Inputs
        i1 = gr.add_node('')
        i2 = gr.add_node('')
        carry_input = gr.add_node('')
        if half:
            gr.get_node_by_id(carry_input).set_label('0')
        gr.add_input_id(i1)
        gr.add_input_id(i2)
        gr.add_input_id(carry_input)

        # Inner nodes
        c1 = gr.add_node(' ', parents={i1:1})
        c2 = gr.add_node(' ', parents={i2:1})
        c3 = gr.add_node(' ', parents={carry_input:1})
        
        a1 = gr.add_node('&', parents={c1:1, c2:1})
        x1 = gr.add_node('^', parents={c1:1, c2:1})
        c4 = gr.add_node(' ', parents={x1:1})

        a2 = gr.add_node('&', parents={c3:1, c4:1})
        x2 = gr.add_node('^', parents={c3:1, c4:1})

        o1 = gr.add_node('|', parents={a1:1, a2:1})

        # Outputs
        out1 = gr.add_node('', parents={o1:1})
        out2 = gr.add_node('', parents={x2:1})
        gr.add_output_id(out1)
        gr.add_output_id(out2)

        return bool_circ(gr)



    @classmethod
    def register(cls, integer, size=8):
        '''
    Constructs a boolean circuit to represent a binary register.

    Constructs a boolean circuit to represent a binary register with the specified integer value and size.

    Parameters:
        integer (int): The integer value to be represented by the register.
        size (int, optional): The size of the register in bits. Defaults to 8.

    Returns:
        bool_circ: A boolean circuit representing the binary register with the given integer value.
    '''
        if integer < 0 or integer >= 2**size:
            raise ValueError("Integer value out of range for given register size")

        binary_str = bin(integer)[2:].zfill(size)

        register_circuit = cls(g=open_digraph.empty())

        for i in range(size):
            node_id = register_circuit.add_node(label=binary_str[i])
            if i == 0:
                register_circuit.add_input_id(node_id)
            if i == size - 1:
                register_circuit.add_output_id(node_id)
            if i > 0:
                register_circuit.add_edge(node_id - 1, node_id)

        return register_circuit

    
    def zero(self, node_id):
         '''
    Sets the label of a node to represent a constant zero.

    Sets the label of the specified node in the boolean circuit to represent a constant zero.

    Parameters:
        node_id (int): The ID of the node to set to zero.

    Returns:
        None
    '''
        self.get_node_by_id(node_id).set_label('0')
        self.get_node_by_id(node_id).set_parents({})
        self.get_node_by_id(node_id).set_children({})


    def one(self, node_id):
        '''
    Sets the label of a node to represent a constant one.

    Sets the label of the specified node in the boolean circuit to represent a constant one.

    Parameters:
        node_id (int): The ID of the node to set to one.

    Returns:
        None
    '''
        self.get_node_by_id(node_id).set_label('1')
        self.get_node_by_id(node_id).set_parents({})
        self.get_node_by_id(node_id).set_children({})


    def invert(self, node_id):
        '''
    Inverts the label of a node.

    Changes the label of the specified node in the boolean circuit to its logical negation.

    Parameters:
        node_id (int): The ID of the node to invert.

    Returns:
        None
    '''
        current_label = self.get_node_by_id(node_id).get_label()
        if current_label == '0':
            self.zero(node_id)
        elif current_label == '1':
            self.one(node_id)
        else:
            self.get_node_by_id(node_id).set_label('~' + current_label)


    def input_copy(self, node_id, input_id):
        '''
    Sets the label of a node to represent an input copy.

    Sets the label of the specified node in the boolean circuit to represent a copy of the input with the given ID.

    Parameters:
        node_id (int): The ID of the node to set as an input copy.
        input_id (int): The ID of the input node to copy.

    Returns:
        None
    '''
        self.get_node_by_id(node_id).set_label(str(input_id))
        self.get_node_by_id(node_id).set_parents({input_id: 1})
        self.get_node_by_id(node_id).set_children({})


    def output_copy(self, node_id, output_id):
        '''
    Sets the label of a node to represent an output copy.

    Sets the label of the specified node in the boolean circuit to represent a copy of the output with the given ID.

    Parameters:
        node_id (int): The ID of the node to set as an output copy.
        output_id (int): The ID of the output node to copy.

    Returns:
        None
    '''
        self.get_node_by_id(node_id).set_label(str(output_id))
        self.get_node_by_id(node_id).set_parents({})
        self.get_node_by_id(node_id).set_children({output_id: 1})


    def and_gate(self, node_id, input_id1, input_id2):
        '''
    Sets the label of a node to represent a logical AND gate.

    Sets the label of the specified node in the boolean circuit to represent a logical AND operation between the inputs with the given IDs.

    Parameters:
        node_id (int): The ID of the node to set as an AND gate.
        input_id1 (int): The ID of the first input node.
        input_id2 (int): The ID of the second input node.

    Returns:
        None
    '''
        self.get_node_by_id(node_id).set_label('&')
        self.get_node_by_id(node_id).set_parents({input_id1: 1, input_id2: 1})
        self.get_node_by_id(node_id).set_children({})


    def or_gate(self, node_id, input_id1, input_id2):
        '''
    Sets the label of a node to represent a logical OR gate.

    Sets the label of the specified node in the boolean circuit to represent a logical OR operation between the inputs with the given IDs.

    Parameters:
        node_id (int): The ID of the node to set as an OR gate.
        input_id1 (int): The ID of the first input node.
        input_id2 (int): The ID of the second input node.

    Returns:
        None
    '''
        self.get_node_by_id(node_id).set_label('|')
        self.get_node_by_id(node_id).set_parents({input_id1: 1, input_id2: 1})
        self.get_node_by_id(node_id).set_children({})


    def xor_gate(self, node_id, input_id1, input_id2):
        '''
    Sets the label of a node to represent a logical XOR gate.

    Sets the label of the specified node in the boolean circuit to represent a logical XOR operation between the inputs with the given IDs.

    Parameters:
        node_id (int): The ID of the node to set as an XOR gate.
        input_id1 (int): The ID of the first input node.
        input_id2 (int): The ID of the second input node.

    Returns:
        None
    '''
        self.get_node_by_id(node_id).set_label('^')
        self.get_node_by_id(node_id).set_parents({input_id1: 1, input_id2: 1})
        self.get_node_by_id(node_id).set_children({})


    def fanout(self, node_id, input_id):
        '''
    Sets the label of a node to represent a fanout operation.

    Sets the label of the specified node in the boolean circuit to represent a fanout operation, copying the input with the given ID.

    Parameters:
        node_id (int): The ID of the node to set as a fanout.
        input_id (int): The ID of the input node to copy.

    Returns:
        None
    '''
        self.get_node_by_id(node_id).set_label(' ')
        self.get_node_by_id(node_id).set_parents({input_id: 1})
        self.get_node_by_id(node_id).set_children({input_id: 1})
    
    
    def evaluate(self):
        """
        Evaluates the boolean circuit by updating the labels of each node to reflect the output values based on the inputs.
        """
        while True:
            transformed = False
            for node_id in self.get_nodes():
                if len(self.get_node_by_id(node_id).get_children()) == 0 and len(self.get_node_by_id(node_id).get_parents()) == 1:
                    parent_id = list(self.get_node_by_id(node_id).get_parents().keys())[0]
                    parent_label = self.get_node_by_id(parent_id).get_label()
                    if parent_label == '0':
                        self.zero(node_id)
                    elif parent_label == '1':
                        self.one(node_id)
                    elif parent_label == '~':
                        self.invert(node_id)
                    elif parent_label.isdigit():
                        self.input_copy(node_id, int(parent_label))
                    elif parent_label == ' ':
                        grandparent_id = list(self.get_node_by_id(parent_id).get_parents().keys())[0]
                        grandparent_label = self.get_node_by_id(grandparent_id).get_label()
                        if grandparent_label in ['&', '|', '^']:
                            input_id = list(self.get_node_by_id(parent_id).get_parents().keys())[0]
                            self.get_node_by_id(parent_id).set_label(str(input_id))
                            self.get_node_by_id(parent_id).set_parents({input_id: 1})
                            self.get_node_by_id(parent_id).set_children({})
                        else:
                            continue
                    elif parent_label in ['&', '|', '^']:
                        inputs = list(self.get_node_by_id(parent_id).get_parents().keys())
                        ready = True
                        for input_id in inputs:
                            if input_id not in self.get_node_by_id(parent_id).get_children():
                                ready = False
                                break
                        if ready:
                            if parent_label == '&':
                                self.and_gate(node_id, inputs[0], inputs[1])
                            elif parent_label == '|':
                                self.or_gate(node_id, inputs[0], inputs[1])
                            elif parent_label == '^':
                                self.xor_gate(node_id, inputs[0], inputs[1])
                    else:
                        continue

                    transformed = True

            if not transformed:
                break


    @classmethod
    def hamming_encoder(cls):
        '''
        Produces a hamming encoder for 3 bits
        '''
        gr = open_digraph.empty()
        for i in range(4):
            inp = gr.add_node("")
            ins = gr.get_input_ids()
            ins.append(inp)
            gr.set_inputs(ins)
        
        for i in range(7):
            out = gr.add_node("")
            outs = gr.get_output_ids()
            outs.append(out)
            gr.set_outputs(outs)

        ins = gr.get_input_ids()

        copies = []
        for i in range(4):
            c = gr.add_node(" ", parents={ins[i]:1})
            copies.append(c)
        
        xs = []
        for i in range(3):
            x = gr.add_node("^", parents={c:1 for c in copies})
            xs.append(x)

        gr.add_edges([[xs[0], outs[0]], [xs[1], outs[1]], [copies[0], outs[2]],
                        [xs[2], outs[3]], [copies[1], outs[4]], [copies[2], outs[5]],
                        [copies[3], outs[6]]])

        return bool_circ(g=gr)


    @classmethod
    def decoder(cls):
        '''
        Produces a Hamming decoder for 3 bits
        '''
        gr = open_digraph.empty()
        for i in range(7):
            inp = gr.add_node("")
            ins = gr.get_input_ids()
            ins.append(inp)
            gr.set_inputs(ins)
        
        for i in range(4):
            out = gr.add_node("")
            outs = gr.get_output_ids()
            outs.append(out)
            gr.set_outputs(outs)
        
        ins = gr.get_input_ids()
        outs = gr.get_output_ids()

        c1 = gr.add_node(" ", parents={ins[2]:1})
        c2 = gr.add_node(" ", parents={ins[4]:1})
        c3 = gr.add_node(" ", parents={ins[5]:1})
        c4 = gr.add_node(" ", parents={ins[6]:1})

        x1 = gr.add_node("^", parents={ins[0]:1, c1:1, c2:1, c3:1, c4:1})
        x2 = gr.add_node("^", parents={ins[1]:1, c1:1, c2:1, c3:1, c4:1})
        x3 = gr.add_node("^", parents={ins[3]:1, c1:1, c2:1, c3:1, c4:1})

        cx1 = gr.add_node(" ", parents={x1:1})
        cx2 = gr.add_node(" ", parents={x2:1})
        cx3 = gr.add_node(" ", parents={x3:1})

        n1 = gr.add_node("~", parents={cx3:1})
        n2 = gr.add_node("~", parents={cx2:1})
        n3 = gr.add_node("~", parents={cx1:1})
        
        a1 = gr.add_node("&", parents={cx1:1, cx2:1, n1:1})
        a2 = gr.add_node("&", parents={cx1:1, n2:1, cx3:1})
        a3 = gr.add_node("&", parents={n3:1, cx2:1, cx3:1})
        a4 = gr.add_node("&", parents={cx1:1, cx2:1, cx3:1})

        x4 = gr.add_node("^", parents={a1:1, c1:1})
        x5 = gr.add_node("^", parents={a2:1, c2:1})
        x6 = gr.add_node("^", parents={a3:1, c3:1})
        x7 = gr.add_node("^", parents={a4:1, c4:1})

        gr.add_edges([[x4, outs[0]], [x5, outs[1]], [x6, outs[2]], [x7, outs[3]]])

        return bool_circ(g=gr)

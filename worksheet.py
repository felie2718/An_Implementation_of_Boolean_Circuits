'''
Calculates depth of half-adder and shortest path between input and output
'''

from modules.bool_circ import bool_circ

for n in range(0, 5):
    adder = bool_circ.adder(n)
    
    best_lengths = []
    for inp in adder.get_input_ids():
        dijkstra = adder.dijkstra(adder.get_node_by_id(inp))[0]
        best_lengths.append(min([dijkstra[out] for out in adder.get_nodes_by_ids(adder.get_output_ids())]))
    
    best = min(best_lengths)
    print(f"Lenght of shortest path between input and output {n}-bit adder: {best}")

for n in range(0, 5):
    adder = bool_circ.adder(n)
    print(f"Depth of {n}-bit adder: {adder.topological_sort()}")
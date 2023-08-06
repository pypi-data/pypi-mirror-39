import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import gym
from gym import spaces
a = nx.DiGraph()
network_size = 10
input_nodes = 3
observation_space = spaces.MultiDiscrete(np.full((network_size, network_size), 2))
s = [i for i in range(input_nodes, network_size)]
print(s)
a.add_nodes_from(range(network_size))
a.add_edge(1,3)
a.add_edge(3,9)
v = a.in_degree()
new_edge = [(2,5)]
a.add_edges_from(new_edge)
all_edges = list(a.edges())
a.remove_edges_from(all_edges)
print(nx.algorithms.dag.is_directed_acyclic_graph(a))
y = [node for node, in_degree in v if in_degree>0]
print(y)

print(v)
q = nx.to_numpy_matrix(a).astype(int)
print(q)

plt.subplot(121)
set1 = nx.ancestors(a, network_size - 1)

print(set(range(network_size)))
if set1 == set(range(network_size)):
    print('sup')
else:
    print(set1, set(range(network_size)))

#nx.draw(a, with_labels=True, font_weight='bold')

final_workflow = nx.DiGraph()
final_workflow.add_nodes_from(range(network_size))
i = 0
while nx.ancestors(final_workflow,network_size-1) != set(range(network_size-1)):
    print('ancestors',nx.ancestors(final_workflow,network_size-1), set(range(network_size-1)))
    i += 1
    if i > 100:
        print('generating graph took too long')
        break
    valid_source_nodes = [index for index, in_degree in
                            final_workflow.in_degree() if
                            ((in_degree > 0 or index < input_nodes) and index < (network_size - 1))]
    print(valid_source_nodes)
    valid_to_nodes = [index for index in range(input_nodes, network_size)]
    print(valid_to_nodes)
    new_edge = [(random.choice(valid_source_nodes), random.choice(valid_to_nodes))]
    final_workflow.add_edges_from(new_edge)
    if not nx.algorithms.dag.is_directed_acyclic_graph(final_workflow):
        print('isnt dag')
        final_workflow.remove_edges_from(new_edge)
    observation = nx.to_numpy_matrix(final_workflow).astype(int)
    if not observation_space.contains(observation):
        print('ineligible')
        final_workflow.remove_edges_from(new_edge)
nx.draw(final_workflow, with_labels=True, font_weight='bold')
plt.show()
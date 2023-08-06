import networkx as nx
import matplotlib.pyplot as plt
a = nx.DiGraph()
number_services = 10
input_nodes = 3
s = [i for i in range(input_nodes,number_services)]
print(s)
a.add_nodes_from(range(number_services))
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
set1 = nx.ancestors(a,number_services-1)

print(set(range(number_services)))
if set1 == set(range(number_services)):
    print('sup')
else:
    print(set1,set(range(number_services)))

nx.draw(a, with_labels=True, font_weight='bold')
plt.show()
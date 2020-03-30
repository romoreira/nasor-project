import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms.simple_paths import all_simple_paths

# Grab edge list
edgelist = pd.read_csv("/home/rodrigo/PycharmProjects/EdgeComputingSlice/topology/domain1_links.csv")
#print(edgelist)

# Grab node list data
nodelist = pd.read_csv("/home/rodrigo/PycharmProjects/EdgeComputingSlice/topology/domain1_routers.csv")
#print(nodelist)

# Create empty graph
g = nx.Graph()

# Add edges and edge attributes
for i, elrow in edgelist.iterrows():
    g.add_edge(elrow[0], elrow[1], attr_dict=elrow[2:].to_dict())

# Add node attributes
for i, nlrow in nodelist.iterrows():
    g.node[nlrow['routerID']].update(nlrow[1:].to_dict())

print("\nLinks:")
print(g.edges(data=True))

print("\nRoteadores")
print(g.nodes(data=True))

# Define node positions data structure (dict) for plotting
node_positions = {node[0]: (node[1]['lati'], -node[1]['long']) for node in g.nodes(data=True)}

# Define data structure (list) of edge colors for plotting
for e in g.edges(data=True):
    edge_colors = [e[2]['attr_dict']['color'] for e in g.edges(data=True)]


#plt.figure(figsize=(19, 10))
#plt.xlabel('Domain1-Connectivity')
#nx.draw(g, pos=node_positions, edge_color=edge_colors, node_size=6, node_color='black',with_labels = True, font_family='sans-serif', font_size=30)
#plt.title('Graph Representation of Sleeping Giant Trail Map', size=15)
#plt.show()
#plt.savefig('/home/rodrigo/PycharmProjects/EdgeComputingSlice/topology/Domain1.png')

print("\nAll Paths:")
for path in all_simple_paths(g, 'r1', 'r3'):
    print (path)

print("\nDjikstra")
print(nx.dijkstra_path(g,'r1','r3',weight = lambda u, v, d: d['attr_dict']['network_metric'] ))



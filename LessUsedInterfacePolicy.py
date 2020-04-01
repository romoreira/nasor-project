import requests
from networkx import get_edge_attributes
from networkx.algorithms.simple_paths import all_simple_paths
import json
from networkx.readwrite import json_graph
import networkx as nx
import pandas as pd
import numpy as np

r = requests.get('http://127.0.0.1:5000/v1.0/getTopology')
#print("\n Response: "+str(r.content))
resposta = str(r.text.decode("utf-8"))
#resposta = resposta.replace("\"", "'")
#jsongraph = json.dumps(json.loads(r.content.encode("utf-8")), sort_keys=True)
#jsongraph = str.replace(str(jsongraph),"u'","'")


jsongraph = json.loads(resposta)
jsongraph = json.dumps(jsongraph)
jsongraph = json.loads(jsongraph,'utf-8')
#print(str(jsongraph["nodes"][0]["id"]).decode("utf-8"))


print(jsongraph["nodes"][0])

g = nx.DiGraph()

for key in jsongraph:
    if key == "links":
        links = jsongraph[key]
        for link in links:
            #print(link)
            g.add_edge(link["source"], link["target"], attr_dict=link["attr_dict"])

#print("\nLinks:")
#print(g.edges(data=True))


# Add node attributes
for key in jsongraph:
    if key == "nodes":
        routers = jsongraph[key]
        for router in routers:
            print(router)
            g.node[router['id']].update(router)


print("\nRoteadores")
print(g.nodes(data=True))

print("\nAll Paths:")
for path in all_simple_paths(g, 'r1', 'r3'):
    print (path)
    print("Test if the path bandwidth consumption is lowest")

for node1, node2, data in g.edges(data=True):
    print(data["attr_dict"])


#Path chosen according Djikstra will be the palce where the Slice SID-based will be setted.
print("\nDjikstra")
print(nx.dijkstra_path(g,'r1','r3',weight = lambda u, v, d: d['attr_dict']['network_metric'] ))





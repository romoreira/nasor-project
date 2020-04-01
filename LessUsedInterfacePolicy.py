import requests
from networkx import get_edge_attributes
from networkx.algorithms.simple_paths import all_simple_paths
import json
from networkx.readwrite import json_graph
import networkx as nx
import pandas as pd
import numpy as np

class LUIP():


    def topology_operations(self):

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




        # Add node attributes
        for key in jsongraph:
            if key == "nodes":
                routers = jsongraph[key]
                for router in routers:
                    print(router)
                    g.node[router['id']].update(router)




        print("\nRoteadores")
        print(g.nodes(data=True))
        print("\nLinks:")
        print(g.edges(data=True))



        print("\nAll Paths:")
        for path in all_simple_paths(g, 'r1', 'r3'):

            print("Path a ser consultado: "+str(path))
            #for each in path:
            #    print("Item do Caminho: "+str(each))
            #    for node in g.nodes(data=True):
            #        print("Detalhes do No do Caminho: "+str(node))
            #        if node[1:][0]["type"] == "core":
            #            print(node[1:][0]["management_ip"])
                #print("Cada Item do Caminho: "+str(each))
        for node1, node2, data in g.edges(data=True):
            print("Cada Item do Edges: "+str(data))


        print("\nPos supostamente fazer o update")
        for node1, node2, data in g.edges(data=True):
            color = nx.get_edge_attributes(g, data[1:])
            print("Cor: "+str(color))
            nx.set_edge_attributes(g, data["attr_dict"]["color"],'g')
            print("Cada Item do Edges: "+str(data))


    def choose_path():

        #Path chosen according Djikstra will be the palce where the Slice SID-based will be setted.
        print("\nDjikstra")
        print(nx.dijkstra_path(g,'r1','r3',weight = lambda u, v, d: d['attr_dict']['network_metric'] ))




    def teste():
        print("Ola mundo")

if __name__ == '__main__':
    print('Running by IDE - NANO')
    topo = LUIP()
    topo.topology_operations()
else:
    print('Imported in somewhere place - NANO')
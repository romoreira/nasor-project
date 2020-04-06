from __future__ import division
import requests
import logging
import time
from networkx import get_edge_attributes
from networkx.algorithms.simple_paths import all_simple_paths
import json
import networkx as nx
import socket
import pycos
import PolicySpeaker
import sys
sys.path.insert(1, '/home/rodrigo/PycharmProjects/EdgeComputingSlice/Policies')

message = ""

class LUIP():

    def __init__(self):
        a = ""

    def speaker_proc(host, port, n, task=None):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = pycos.AsyncSocket(sock)
        yield sock.connect((host, int(port)))
        msg = str(message) + '/'
        msg = msg.encode()
        yield sock.sendall(msg)
        sock.close()


    def topology_operations(self):

        r = requests.get('http://127.0.0.1:5000/v1.0/getTopology')
        #print("\n Response: "+str(r.content))
        resposta = str(r.text).encode("utf-8")
        #resposta = resposta.replace("\"", "'")
        #jsongraph = json.dumps(json.loads(r.content.encode("utf-8")), sort_keys=True)
        #jsongraph = str.replace(str(jsongraph),"u'","'")

        print("Resposta: "+str(resposta))

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
            print(path)
            for each in path:
                for router in g.nodes(data=True):
                    if router[0] == each:#A lista de router e igual a algum do caminho
                        #print(router[1]["management_ip"])
                        print(router[1:][0]["management_ip"])

        utilization_path_1 = []

        r = requests.get('http://192.168.0.247:1414/network/statistics?interface=eth0&stamp=8')
        result = r.json()
        utilization_path_1.append(str(result["tx"]["ratestring"]))

        r = requests.get('http://192.168.0.248:1414/network/statistics?interface=eth1&stamp=8')
        result = r.json()
        utilization_path_1.append(str(result["tx"]["ratestring"]))

        r = requests.get('http://192.168.0.249:1414/network/statistics?interface=eth2&stamp=8')
        result = r.json()
        utilization_path_1.append(str(result["tx"]["ratestring"]))

        r = requests.get('http://192.168.0.250:1414/network/statistics?interface=eth0&stamp=8')
        result = r.json()
        utilization_path_1.append(str(result["tx"]["ratestring"]))


        #PATH 2-------------------------------------------------------------

        utilization_path_2 = []

        r = requests.get('http://192.168.0.247:1414/network/statistics?interface=eth1&stamp=8')
        result = r.json()
        utilization_path_2.append(str(result["tx"]["ratestring"]))

        r = requests.get('http://192.168.0.249:1414/network/statistics?interface=eth2&stamp=8')
        result = r.json()
        utilization_path_2.append(str(result["tx"]["ratestring"]))



        print("Capacity Utilization - Path 1 "+str(utilization_path_1))
        print("Capacity Utilization - Path 2 " + str(utilization_path_2))

        # Channal utilization 1---------------------------------------------------------------

        channal_utilization1 = 0

        #Provide a sum of utilization of path 1
        for each in utilization_path_1:
            each = each.split()
            # print("Valor: "+str(each[0]))
            # print("Scala: " + str(each[1]))
            if each[1].startswith("k"):
                #print("start with k")
                channal_utilization1 =  float(channal_utilization1 + (float(each[0])/1000))
                #print("Channel utilization in mbps: "+str(channal_utilization1))
            if each[1].startswith("M"):
                #print("start with m")
                channal_utilization1 = float(float(each[0]) + channal_utilization1)
                #print("Channel utilization in mbps: " + str(channal_utilization1))

        #Channal utilization 2---------------------------------------------------------------

        channal_utilization2 = 0

        print("\nPath utlization PATH 2")
        # Provide a sum of utilization of path 2
        for each in utilization_path_2:
            each = each.split()
            #print("Valor: "+str(each[0]))
            #print("Scala: " + str(each[1]))
            # print(each[2:])
            # print("Soma teste: "+str(int(each[0]) + 1))
            if each[1].startswith("k"):
                print("start with k")
                channal_utilization2 = float(channal_utilization2 + (float(each[0]) / 1000))
                #print("Channel utilization in mbps: " + str(channal_utilization2))
            if each[1].startswith("M"):
                #print("start with M")
                channal_utilization2 = float(float(each[0]) + channal_utilization2)
                #print("Channel utilization in mbps: " + str(channal_utilization2))

        print("Path 1 Utilization in Mbps: "+str(channal_utilization1))
        print("Path 2 Utilization in Mbps: " + str(channal_utilization2))

        if channal_utilization1 > channal_utilization2:
            print("Path escollhido: 2 - Instalar os SIDs")
            return
        elif channal_utilization1 <= channal_utilization2:
            print("Path escollhido: 1 - Instalar os SIDs")
            return



    def choose_path(self):

        #Path chosen according Djikstra will be the palce where the Slice SID-based will be setted.
        print("\nDjikstra")
        print(nx.dijkstra_path(g,'r1','r3',weight = lambda u, v, d: d['attr_dict']['network_metric'] ))



#if __name__ == '__main__':
#    print('Running by IDE - NANO')
#    topo = LUIP()
#    topo.topology_operations()

#else:
#    logging.debug("Imported in somewhere place - Less Used Interfaec Policy")
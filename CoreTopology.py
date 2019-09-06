'''
Author: Rodrigo Moreira
Date: 05/09/2019
'''
#To be defined further
import networkx as nx


G = nx.Graph()


G.add_node(2)
G.nodes[2]['is_border_vnf'] = 'false'
G.nodes[2]['vnf_management_ip'] = '192.168.0.100'
G.nodes[2]['vnf_egress-if_name'] = 'eth1'
G.nodes[2]['vnf_ingress-if_name'] = 'eth2'
G.nodes[2]['vim_management_ip'] = '192.168.0.200'

G.add_node(1)
G.nodes[1]['is_border_vnf'] = 'false'
G.nodes[1]['vnf_management_ip'] = '192.168.0.100'
G.nodes[1]['vnf_egress-if_name'] = 'eth1'
G.nodes[2]['vnf_ingress-if_name'] = 'eth2'
G.nodes[1]['vim_management_ip'] = '192.168.0.200'

G.add_edge(1, 2)


print(str(G.nodes.data()))


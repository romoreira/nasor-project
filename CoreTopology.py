"""
Author: Rodrigo Moreira
Date: 05/09/2019
"""

# To be defined further
import networkx as nx


class CoreTopology:
    G = nx.Graph()

    def is_nodes_connected(self, u, v):
        return u in self.G.neighbors(v)

    def neighborhood_check(self, asns_involved):

        self.G.add_node(2)
        self.G.nodes[2]['asn'] = 16735
        self.G.nodes[2]['is_border_vnf'] = 'false'
        self.G.nodes[2]['vnf_management_ip'] = '192.168.0.100'
        self.G.nodes[2]['vnf_egress-if_name'] = 'eth1'
        self.G.nodes[2]['vnf_ingress-if_name'] = 'eth2'
        self.G.nodes[2]['vim_management_ip'] = '192.168.0.200'

        self.G.add_node(1)
        self.G.nodes[1]['asn'] = 14571
        self.G.nodes[1]['is_border_vnf'] = 'true'
        self.G.nodes[1]['vnf_management_ip'] = '192.168.0.100'
        self.G.nodes[1]['vnf_egress-if_name'] = 'eth1'
        self.G.nodes[1]['vnf_ingress-if_name'] = 'eth2'
        self.G.nodes[1]['vim_management_ip'] = '192.168.0.200'

        self.G.add_edge(1, 2)

        print("Checking neighborhood. Graph Data: " + str(self.G.nodes.data()))

        # Building a Python list - removing first and last charachtere.
        asns_involved = asns_involved[1:-1]
        asns_involved = asns_involved.split(",")
        node_index = []

        # Checkin if given two ASN they are neighbors - save the tuple of Node IDs.
        for n in self.G.nodes:
            if str(self.G.nodes[n]['asn']) in str(asns_involved):
                node_index.append(n)

        print(str(self.is_nodes_connected(node_index[0], node_index[1])) + " - Vizinhança!")

'''
Author: Rodrigo Moreira
Date: 05/09/2019
'''
#To be defined further
import networkx as nx


class CoreTopology:

    G = nx.Graph()

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

        print(str(self.G.nodes.data()))

        for n, nbrs in self.G.adj.items():
            for nbr, eattr in nbrs.items():
                print('(%d, %d)' % (n, nbr))

        for u in self.G.nodes:
            print(str(self.G.nodes[u]['asn']))

        print("FIM: "+str(asns_involved))
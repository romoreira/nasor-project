from networkx.algorithms.simple_paths import all_simple_paths
import logging
import networkx as nx
import pandas as pd
from networkx.readwrite import json_graph
from flask import Flask
from flask import request
import PolicySpeaker
import sys
sys.path.insert(1, '/home/rodrigo/PycharmProjects/EdgeComputingSlice/Policies')

#import sys
#sys.path.insert(1, '/home/rodrigo/PycharmProjects/EdceComputingSlice/segment-routing')
#import grpc_client
import json

SlicePolicyAPI = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

def get_topology():

    # Grab edge list
    edgelist = pd.read_csv("/home/rodrigo/PycharmProjects/EdgeComputingSlice/topology/domain1_links.csv")
    #print(edgelist)

    # Grab node list data
    nodelist = pd.read_csv("/home/rodrigo/PycharmProjects/EdgeComputingSlice/topology/domain1_routers.csv")
    # print(nodelist)

    # Create empty graph
    g = nx.DiGraph()

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

    # plt.figure(figsize=(19, 10))
    # plt.xlabel('Domain1-Connectivity')
    # nx.draw(g, pos=node_positions, edge_color=edge_colors, node_size=6, node_color='black',with_labels = True, font_family='sans-serif', font_size=30)
    # plt.title('Graph Representation of Sleeping Giant Trail Map', size=15)
    # plt.show()
    # plt.savefig('/home/rodrigo/PycharmProjects/EdgeComputingSlice/topology/Domain1.png')

    print("\nAll Paths:")
    for path in all_simple_paths(g, 'r1', 'r3'):
        print (path)

    return json_graph.node_link_data(g)

#@SlicePolicyAPI.route('/v1.0/installRouteR1', methods=['GET'])
#def route_installR1():
#    data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
#    global message
#    json_m = json.loads(data)
#    message = json.dumps(json_m)

#    print("Message: "+str(message))

#    grpc_route_agent = grpc_client.gRPC_Route("192.168.0.247",12345,message)
#    print(grpc_route_agent.main())


@SlicePolicyAPI.route('/v1.0/getTopology', methods=['GET'])
def api_topology():
    return get_topology()

@SlicePolicyAPI.route('/v1.0/applyPolicy', methods=['GET'])
def apply_policy():
    print("Applying Slice Policy")
    args = request.args
    if args["policy_type"] == "bgp":
        print("BGP Policy Chosed")
        PolicySpeaker.experimento_deployment_time1()
        return "Applying BGP-aware"
    elif args["policy_type"] == "networK_aware":
        print("Netowrk Aware chosed")
    else:
        return "Policy Unavailable"

if __name__ == '__main__':
    logging.debug('Running by IDE - SlicePolicyAPI')
    SlicePolicyAPI.run(debug=True)
else:
    logging.debug('Imported in somewhere place - SlicePolicyAPI')
    SlicePolicyAPI.run(debug=True)
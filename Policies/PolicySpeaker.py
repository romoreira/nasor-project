import pycos
import socket
import logging
import json
import sys
sys.path.insert(1, '../segment-routing')
import grpc_client
import grpc_sid_client

message = []

def sr_policy_installR1():
    #data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
    data = """{%ssid_ip%s: %s""" + str("a::2") + """%s, %ssid_behaviour%s: %s""" + str("end") + """%s}"""
    data = str(data % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
    global message
    json_m = json.loads(data)

    message = json_m

    #print("Message SENT: "+str(message))

    sid_installer = grpc_sid_client.gRPC_SID("192.168.0.247", 123456, message)
    print("Policy SID Creation Response: " + str(sid_installer.main()))

def route_installR1():
    data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F3"]}]}]"""
    global message
    json_m = json.loads(data)
    message = json.dumps(json_m)

    #print("Message: "+str(message))

    grpc_route_agent = grpc_client.gRPC_Route("192.168.0.247",12345,message)
    print(grpc_route_agent.main())


#ROUTER 3#____________________________________________________________________________________



def sr_policy_installR3():
    #data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
    #sudo srconf localsid add 2::AD6:F1 end.ad6 ip 2:f1::f1 veth1_2 veth1_2
    data = """{%ssid_ip%s: %s""" + str("2::AD6:F3") + """%s, %ssid_behaviour%s: %s""" + str("end") + """%s}"""
    data = str(data % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
    global message
    json_m = json.loads(data)

    message = json_m

    #print("Message SENT: "+str(message))

    sid_installer = grpc_sid_client.gRPC_SID("192.168.0.249", 123456, message)
    print("Policy SID Creation Response: " + str(sid_installer.main()))

def route_installR3():
    data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
    global message
    json_m = json.loads(data)
    message = json.dumps(json_m)

    #print("Message: "+str(message))

    grpc_route_agent = grpc_client.gRPC_Route("192.168.0.249",12345,message)
    print(grpc_route_agent.main())

if __name__ == "__main__":
    logging.debug('Running by IDE - PolicySpeaker')
    route_installR1()
    #sr_policy_installR1()
    #route_installR3()
    #sr_policy_installR3()

else:
    logging.debug('Running throug import - PolicySpeaker')
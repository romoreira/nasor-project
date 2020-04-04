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
    data = """{%ssid_ip%s: %s""" + str("1::d6") + """%s, %ssid_behaviour%s: %s""" + str("end.dx6") + """%s, %sip_addr%s: %s""" + str("a::2") + """%s, %starget_if%s: %s""" + str("veth1_1") + """%s}"""
    data = str(data % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
    global message
    json_m = json.loads(data)

    message = json_m

    #print("Message SENT: "+str(message))

    sid_installer = grpc_sid_client.gRPC_SID("192.168.0.247", 123456, message)
    print("Policy SID Creation Response: " + str(sid_installer.main()))

def route_installR1():
    data = """[{"paths": [{"via": "2001:470:28:5a1::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::d6","2001::"]}]}]"""
    global message
    json_m = json.loads(data)
    message = json.dumps(json_m)

    #print("Message: "+str(message))

    grpc_route_agent = grpc_client.gRPC_Route("192.168.0.247",12345,message)
    print(grpc_route_agent.main())


#ROUTER 3#____________________________________________________________________________________



def policy_installR3_left_right():
    #data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
    #sudo srconf localsid add 2::AD6:F1 end.ad6 ip 2:f1::f1 veth1_2 veth1_2

    data = """{%ssid_ip%s: %s""" + str("2001::") + """%s, %ssid_behaviour%s: %s""" + str("end") + """%s, %sip_addr%s: %s""" + str("") + """%s, %starget_if%s: %s""" + str("") + """%s}"""
    data = str(data % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))

    global message
    json_m = json.loads(data)

    message = json_m

    #print("Message SENT: "+str(message))

    sid_installer = grpc_sid_client.gRPC_SID("192.168.0.249", 123456, message)
    print("Policy SID Creation Response: " + str(sid_installer.main()))

def policy_installR3_right_left():
    #data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
    #sudo srconf localsid add 2::AD6:F1 end.ad6 ip 2:f1::f1 veth1_2 veth1_2
    data = """{%ssid_ip%s: %s""" + str("2607::") + """%s, %ssid_behaviour%s: %s""" + str("end") + """%s, %sip_addr%s: %s""" + str("") + """%s, %starget_if%s: %s""" + str("") + """%s}"""
    data = str(data % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
    global message
    json_m = json.loads(data)

    message = json_m

    #print("Message SENT: "+str(message))

    sid_installer = grpc_sid_client.gRPC_SID("192.168.0.249", 123456, message)
    print("Policy SID Creation Response: " + str(sid_installer.main()))

def routes_installR3_left_right():
    data = """[{"paths": [{"via": "2607:f0d0:2001::2", "device": "eth2", "destination": "b::/64", "encapmode": "", "segments": ""}]}]"""
    global message
    json_m = json.loads(data)
    message = json.dumps(json_m)

    #print("Message: "+str(message))

    grpc_route_agent = grpc_client.gRPC_Route("192.168.0.249",12345,message)
    print(grpc_route_agent.main())


#ROUTER 4#________________________________________________________________________________


def sr_policy_installR4():
    #data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
    #Base: srconf localsid add 2607:f0d0:2001::2 end.dx6 ip b::2 veth1_3
    data = """{%ssid_ip%s: %s""" + str("3::d6") + """%s, %ssid_behaviour%s: %s""" + str("end.dx6") + """%s, %sip_addr%s: %s""" + str("b::2") + """%s, %starget_if%s: %s""" + str("veth1_3") + """%s}"""
    data = str(data % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
    global message
    json_m = json.loads(data)

    message = json_m

    #print("Message SENT: "+str(message))

    sid_installer = grpc_sid_client.gRPC_SID("192.168.0.250", 123456, message)
    print("Policy SID Creation Response: " + str(sid_installer.main()))


def route_installR4():
    data = """[{"paths": [{"via": "2607:f0d0:2001::1", "device": "eth2", "destination": "a::/64", "encapmode": "encap", "segments": ["1::d6", "2607::"]}]}]"""
    global message
    json_m = json.loads(data)
    message = json.dumps(json_m)

    #print("Message: "+str(message))

    grpc_route_agent = grpc_client.gRPC_Route("192.168.0.250",12345,message)
    print(grpc_route_agent.main())











    #-------------------------------------#Experimento 2 - Canal Alternativo#-------------------------------------------------









def exp2_policy_installR1():
    #data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
    data = """{%ssid_ip%s: %s""" + str("1::d6") + """%s, %ssid_behaviour%s: %s""" + str("end.dx6") + """%s, %sip_addr%s: %s""" + str("a::2") + """%s, %starget_if%s: %s""" + str("veth1_1") + """%s}"""
    data = str(data % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
    global message
    json_m = json.loads(data)

    message = json_m

    #print("Message SENT: "+str(message))

    sid_installer = grpc_sid_client.gRPC_SID("192.168.0.247", 123456, message)
    print("Policy SID Creation Response: " + str(sid_installer.main()))


def exp2_policy_installR2_left_right():
    #data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
    #sudo srconf localsid add 2::AD6:F1 end.ad6 ip 2:f1::f1 veth1_2 veth1_2
    data = """{%ssid_ip%s: %s""" + str("2::") + """%s, %ssid_behaviour%s: %s""" + str("end") + """%s, %sip_addr%s: %s""" + str("") + """%s, %starget_if%s: %s""" + str("") + """%s}"""
    data = str(data % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
    global message
    json_m = json.loads(data)

    message = json_m

    #print("Message SENT: "+str(message))

    sid_installer = grpc_sid_client.gRPC_SID("192.168.0.248", 123456, message)
    print("Policy SID Creation Response: " + str(sid_installer.main()))

def exp2_policy_installR3_left_right():
    #data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
    #sudo srconf localsid add 2::AD6:F1 end.ad6 ip 2:f1::f1 veth1_2 veth1_2
    data = """{%ssid_ip%s: %s""" + str("3::") + """%s, %ssid_behaviour%s: %s""" + str("end") + """%s, %sip_addr%s: %s""" + str("") + """%s, %starget_if%s: %s""" + str("") + """%s}"""
    data = str(data % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
    global message
    json_m = json.loads(data)

    message = json_m

    #print("Message SENT: "+str(message))

    sid_installer = grpc_sid_client.gRPC_SID("192.168.0.249", 123456, message)
    print("Policy SID Creation Response: " + str(sid_installer.main()))


def exp2_policy_installR3_right_left():
    #data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
    #sudo srconf localsid add 2::AD6:F1 end.ad6 ip 2:f1::f1 veth1_2 veth1_2
    data = """{%ssid_ip%s: %s""" + str("5::") + """%s, %ssid_behaviour%s: %s""" + str("end") + """%s, %sip_addr%s: %s""" + str("") + """%s, %starget_if%s: %s""" + str("") + """%s}"""
    data = str(data % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
    global message
    json_m = json.loads(data)

    message = json_m

    #print("Message SENT: "+str(message))

    sid_installer = grpc_sid_client.gRPC_SID("192.168.0.249", 123456, message)
    print("Policy SID Creation Response: " + str(sid_installer.main()))


def exp2_policy_installR2_right_left():
    #data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
    #sudo srconf localsid add 2::AD6:F1 end.ad6 ip 2:f1::f1 veth1_2 veth1_2
    data = """{%ssid_ip%s: %s""" + str("6::") + """%s, %ssid_behaviour%s: %s""" + str("end") + """%s, %sip_addr%s: %s""" + str("") + """%s, %starget_if%s: %s""" + str("") + """%s}"""
    data = str(data % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
    global message
    json_m = json.loads(data)

    message = json_m

    #print("Message SENT: "+str(message))

    sid_installer = grpc_sid_client.gRPC_SID("192.168.0.248", 123456, message)
    print("Policy SID Creation Response: " + str(sid_installer.main()))

def exp2_policy_installR4():
    #data = """[{"paths": [{"via": "1:2::2", "device": "eth1", "destination": "b::/64", "encapmode": "encap", "segments": ["3::D6","2::AD6:F2","2::AD6:F1"]}]}]"""
    data = """{%ssid_ip%s: %s""" + str("4::d6") + """%s, %ssid_behaviour%s: %s""" + str("end.dx6") + """%s, %sip_addr%s: %s""" + str("b::2") + """%s, %starget_if%s: %s""" + str("veth1_3") + """%s}"""
    data = str(data % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
    global message
    json_m = json.loads(data)

    message = json_m

    #print("Message SENT: "+str(message))

    sid_installer = grpc_sid_client.gRPC_SID("192.168.0.250", 123456, message)
    print("Policy SID Creation Response: " + str(sid_installer.main()))


if __name__ == "__main__":

    logging.debug('Running by IDE - PolicySpeaker')

    # Experimento 1-------------------------------------------------------------------

    #route_installR1()
    #sr_policy_installR1()
    #policy_installR3_left_right()
    #policy_installR3_right_left()
    #routes_installR3_left_right()
    #routes_installR3_right_left()
    #route_installR4()
    #sr_policy_installR4()

    #Experimento 2-------------------------------------------------------------------

    #exp2_policy_installR2_left_right()
    #exp2_policy_installR3_left_right()
    #exp2_policy_installR4()

    #exp2_policy_installR3_right_left()
    #exp2_policy_installR2_right_left()
    #exp2_policy_installR1()



else:
    logging.debug('Running throug import - PolicySpeaker')
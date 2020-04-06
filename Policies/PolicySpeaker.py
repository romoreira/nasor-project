import paramiko
import pycos
import socket
import logging
import json
import time
import sys
sys.path.insert(1, '/home/rodrigo/PycharmProjects/EdgeComputingSlice/segment-routing')
import grpc_client
import grpc_sid_client

sys.path.insert(1, '/home/rodrigo/PycharmProjects/EdgeComputingSlice/Policies')
import LessUsedInterfacePolicy

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

def exp2_route_installR1():
    data = """[{"paths": [{"via": "2001:470:28:5a1::2", "device": "eth0", "destination": "b::/64", "encapmode": "encap", "segments": ["4::D6","3::","2::"]}]}]"""
    global message
    json_m = json.loads(data)
    message = json.dumps(json_m)

    #print("Message: "+str(message))

    grpc_route_agent = grpc_client.gRPC_Route("192.168.0.247",12345,message)
    print(grpc_route_agent.main())

def exp2_route_installR4():
    data = """[{"paths": [{"via": "2001:470:28:5a1::2", "device": "eth0", "destination": "a::/64", "encapmode": "encap", "segments": ["1::D6","6::","5::"]}]}]"""
    global message
    json_m = json.loads(data)
    message = json.dumps(json_m)

    #print("Message: "+str(message))

    grpc_route_agent = grpc_client.gRPC_Route("192.168.0.250",12345,message)
    print(grpc_route_agent.main())





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

def experimento_deployment_time2():
    import LessUsedInterfacePolicy
    less_used = LessUsedInterfacePolicy.LUIP()

    start_time = 0

    with open("/home/rodrigo/PycharmProjects/EdgeComputingSlice/benchmark/Experiment_2/Data-DeploymentTime/Round2-Network-aware-8.txt", "a+") as file_object:

        for i in range(50):
            print("Captura Tempo inicial - I == "+str(i))
            start_time = time.time()
            less_used.topology_operations()#Check networks statuses

            exp2_route_installR1()
            exp2_policy_installR2_left_right()
            exp2_policy_installR3_left_right()
            exp2_policy_installR4()

            exp2_route_installR4()
            exp2_policy_installR3_right_left()
            exp2_policy_installR2_right_left()
            exp2_policy_installR1()


            file_object.write(str((time.time() - start_time)) + "\n")
            print("Escreve Tempo Final -- I == "+str(i))

            #Deleting previuous config to the next one Round of Experiments
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("192.168.0.247", username="sr6", password="sr6")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /home/sr6/deployment_time/clear.sh")
            print("Output Router 1: "+str(ssh_stdout.readlines()))
            ssh.close()

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("192.168.0.248", username="sr6", password="sr6")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /home/sr6/deployment_time/clear.sh")
            print("Output Router 2: " + str(ssh_stdout.readlines()))
            ssh.close()

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("192.168.0.249", username="sr6", password="sr6")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /home/sr6/deployment_time/clear.sh")
            print("Output Router 3: " + str(ssh_stdout.readlines()))
            ssh.close()

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("192.168.0.250", username="sr6", password="sr6")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /home/sr6/deployment_time/clear.sh")
            print("Output Router 4: " + str(ssh_stdout.readlines()))
            ssh.close()


def experimento_deployment_time1():
    with open("/home/rodrigo/PycharmProjects/EdgeComputingSlice/benchmark/Experiment_2/Data-DeploymentTime/Round1.txt", "a+") as file_object:

        start_time = time.time()

        route_installR1()
        sr_policy_installR1()
        policy_installR3_left_right()
        policy_installR3_right_left()
        route_installR4()
        sr_policy_installR4()

        file_object.write(str((time.time() - start_time))+"\n")

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

    experimento_deployment_time2()

else:
    logging.debug('Running throug import - PolicySpeaker')



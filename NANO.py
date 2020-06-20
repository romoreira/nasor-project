"""
Author: Rodrigo Moreira
Date: 10/09/2019
"""

# O que imagino para essa Classe: ela recebera um yaml contendo o asn onde devera ser lancado o serviço,
# além disso, no yaml contem o nivel onde ocorrera o deployment. Essa classe devera consultar o
# Apache Geode para procurar nessa base persistente o VIM aonde a VNF esta lancada e por ela fazer o
# mapeamento desde a VNF ate a outra. Empurrando isso de forma inter-dominios.

#Links do multi-domain dataplane:
#https://wiki.gentoo.org/wiki/Quagga
#https://www.brianlinkletter.com/how-to-build-a-network-of-linux-routers-using-quagga/
#https://openmaniak.com/quagga_tutorial.php
#https://blog.codybunch.com/2016/07/12/Getting-started-with-BGP-on-Linux-with-Cumuls-Quagga/
#http://www.occaid.org/tutorial-ipv6bgp.html
import threading
from optparse import OptionParser
import json, logging
import socket

import CoreDomainTopology

import re

import sys
import telnetlib



sys.path.insert(1, './segment-routing')
import grpc_client
import grpc_sid_client


# logger reference
logging.basicConfig(level=logging.DEBUG)

import IOExClient

# Debug option
SERVER_DEBUG = False

from threading import Thread
import ipaddress


class NANO(Thread):

    NSTD = None
    ASes = []
    NANO_HOST = ""
    NANO_PORT = ""
    NANO_ASN = ""

    message = ""


    '''
    Constructor
    '''
    def __init__(self, val, NANO_ASN, NANO_HOST, NANO_PORT):
        super(NANO, self).__init__()
        self.val = val
        self.NANO_ASN = NANO_ASN
        self.NANO_HOST = NANO_HOST
        self.NANO_PORT = NANO_PORT

    def nst_yaml_interpreter(NSTD):
        ct = CoreDomainTopology.CoreTopology()
        return NSTD[0]['asns']
        #return ct.neighborhood_check(str(self.NSTD[0]['asns']))

    def telnet_agent(self, HOST, COMMAND, PORT):

        user = ""
        password = "zebra\r\n"
        command = "show ipv6 bgp\r\n"

        tn = telnetlib.Telnet(HOST, PORT)

        l = tn.read_until("Password: ".encode())
        #print("Primeira tela ao requisitar login: " + str(l))

        tn.write(password.encode())
        l = tn.read_until("border> ".encode())
        #print("Resultado pos entrar com password: " + str(l))

        tn.write(command.encode())
        l = tn.read_until("Total number of prefixes".encode()).decode()
        tn.close()
        return str(l)

    def get_nano_agent_host(self, ASN):
        "Procurar na Base de Orchestradores do IP do Nano dado um ASN"
        if str(ASN) == str(7675):
            return "192.168.0.130"
        elif str(ASN) == str(16735):
            return "192.168.0.130"
        elif str(ASN) == str(26599):
            return "192.168.0.130"

    def get_nano_agent_port(self, ASN):
        "Procurar na Base de Orchestradores a Porta do Nano dado um ASN"
        if str(ASN) == str(7675):
            return "8013"
        elif str(ASN) == str(16735):
            return "8015"
        elif str(ASN) == str(26599):
            return "8011"

    def telnet_agent_get_iface(self, HOST, PORT, COMMAND):
        user = ""
        password = "zebra\r\n"
        command = "show ipv6 bgp\r\n"

        tn = telnetlib.Telnet(HOST, PORT)

        l = tn.read_until("Password: ".encode())
        #print("Primeira tela ao requisitar login: " + str(l))

        tn.write(password.encode())
        l = tn.read_until("border> ".encode())
        #print("Resultado pos entrar com password: " + str(l.decode()))

        tn.write(COMMAND.encode())
        l = tn.read_until("eth0".encode()).decode()
        tn.close()
        return str(l[190:])

    def target_encounter_check(self, NEXT_HOP, ROUTER_IP):
        route_entries = []
        print("Looking in Target something")
        print("TARGET-CHECK NEXT_HOP: "+str(NEXT_HOP))
        print("TARGET-CHECK ROUTER_IP: " + str(ROUTER_IP))
        iface = NANO.telnet_agent_get_iface("",ROUTER_IP,2601,"show ipv6 route\r\n")
        route_entries = iface.splitlines()
        route = []
        print("TARGET-CHECK ROUTE-ENTRIES: "+str(route_entries))
        for item in route_entries:
            route = item.split()
            print("ROUTE: "+str(route))
            if route:
                print("Item Rota Teste: "+str(route[1]))
                print("Next Hop: "+str(NEXT_HOP[0]))
                try:
                    if ipaddress.ip_address(NEXT_HOP[0]) in ipaddress.ip_network(route[1]):
                        print("Return the network interface to Next Hop: "+str(route[5]))
                        return True
                except ValueError:
                    logging.debug("zebra routes * can not be compared with IPv6 to Check network connectivity - get_egress_interface")
        print("Nothing were found check - get_egress_interface()")

    def get_egress_interface(self, NEXT_HOP):
        route_entries = []
        #print("Looking for Egress Interface to install Routes")
        iface = NANO.telnet_agent_get_iface("","192.168.0.203",2601,"show ipv6 route\r\n")
        route_entries = iface.splitlines()
        route = []
        for item in route_entries:
            route = item.split()
            if route:
                #print("Item Rota Teste: "+str(route[1]))
                #print("Next Hop: "+str(NEXT_HOP[0]))
                try:
                    if ipaddress.ip_address(NEXT_HOP[0]) in ipaddress.ip_network(route[1]):
                        #print("Return the network interface to Next Hop: "+str(route[5]))
                        return route[5]
                except ValueError:
                    logging.debug("zebra routes * can not be compared with IPv6 to Check network connectivity - get_egress_interface")
        print("Nothing were found check - get_egress_interface()")

    def get_next_hop(self, ASN):
        #print("Respondendo a Requisicao de Next HOP para o ASN: "+str(ASN))

        #as_path = NANO.telnet_agent("",NANO.get_nano_agent("",ASN))
        as_path = NANO.telnet_agent("", "192.168.0.204", "",2605)

        as_path = as_path[280:]
        #print(as_path)

        char1 = '*>'
        char2 = ' i'
        # print("Teste: "+as_path[as_path.find(char1) + 1: as_path.find(char2)])
        # as_path = as_path[as_path.find(char1) + 1: as_path.find(char2)]
        as_path = as_path.replace(" i", " #")
        # print(as_path)
        as_path = as_path.replace("*>", "#")
        # print("Ultimo: "+str(as_path))
        as_path = as_path.replace("\t", " ")
        # print("Sem Espaco: "+str(as_path))

        char1 = '#'
        char2 = ' #'
        # print("Start with: "+str(as_path.index("#")))
        # print("End with: "+str((as_path.index("#")+1).index("#")))
        rota_a = as_path[as_path.find(char1) + 1: as_path.find(char2)]
        rota_b = as_path[as_path.find(char1) + 1: as_path.find(char2)]

        rib_entries = []
        rib1 = as_path[as_path.index("#"): as_path.find(char2)]
        # print("RIB1: "+str(rib1))
        # print("SEPARA")
        rib1 = rib1.replace("\r", " ")
        # print("RIB1: "+str(rib1.rstrip()))
        # print("Index: "+str(as_path.find(char2)).index("#"))

        rib1 = re.sub(' +', ' ', rib1)
        # print("REGEX: "+rib1)
        rib1 = as_path.replace('\n', ' ').replace('\r', '')
        rib1 = re.sub(' +', ' ', rib1)
        # print("Remover enters: "+rib1)

        # print("Indice do Asterisco: "+str(rib1.index("*")))
        #print("Depois do Asteristo: " + str(rib1[rib1.index("*") + 1:].find("#")))

        rib_list = []

        # print(rib1[44+1:].find("#"))

        rib_entry = ""
        index = 0
        #print("Tamanho da rib1: " + str(len(rib1)))
        while index != len(rib1):
            # print("Index1: "+str(index))

            if rib1[index] == "#":
                # print("Entrou no for com Index1: "+str(index))
                for index2 in range(index + 1, index + rib1[index + 1:].find("#") + 1):
                    rib_entry += rib1[index2]
                    # print("Index2: "+str(index2))
                    from_index = index2
                rib_list.append(rib_entry)
                rib_entry = ""
                # print(rib_list)
                index = from_index + 2
                # print("Indice que vai partir: "+str(index))
            if rib1[index] == "*":
                # print("Faz nada ate encontrar outro #")
                for index2 in range(index + 1, index + 1 + rib1[index + 1:].find("#") + 1):
                    from_index = index2
                index = from_index
            index = index + 1

        #print("RIB_LIST: " + str(rib_list))

        rib_list_aux = []

        for string in rib_list:
            rib_list_aux.append(string.replace(" ", ";"))

        rib_list = rib_list_aux

        # Verifico qual entrada da rib_list possui o as_peer_slice, ou seja o AS do outro dominio que foi descrito no template
        # do slice
        print(rib_list)

        slice_as_path = []
        slice_as_path_aux = []
        next_hop = []

        for entry in rib_list:
            entry = entry.split(";")
            for each in entry:
                if str(each) == str(ASN):
                    print("Encontrou a entrada que contem o AS target: " + str(entry))
                    next_hop = entry[2]

        print("Roteador consultado.")
        return next_hop

    def eDomain_slice_builder(self, DATA, ASN):

        NANO.NANO_ASN = ASN

        ASs = NANO.nst_yaml_interpreter(DATA['details'])
        print("ASs do Slice: "+str(ASs))

        print("AS Corrente: "+str(NANO.NANO_ASN))

        print("DATA: "+str(DATA))
        print("END TO END NEXT HOP: "+str(DATA['end2end_next_hop']))

        if not(NANO.NANO_ASN in ASs):
            print("NANO.NANO_ASN: "+str(NANO.NANO_ASN))
            print("AS nao faz parte do ASs do slice - ele e transito")

            next_hop_transit = DATA['end2end_next_hop']
            print("Transit list: "+str(next_hop_transit))


            print("end2end_next_hop: "+str(DATA['end2end_next_hop'][0]))



            sid_behaviour = "end"
            sid_creation_json_message = """{%ssid_ip%s: %s"""+str(next_hop_transit[0])+"""%s, %ssid_behaviour%s: %s"""+str(sid_behaviour)+"""%s}"""
            sid_creation_json_message = str(sid_creation_json_message % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
            sid_creation_json_message = json.loads(sid_creation_json_message)
            print("JSON CRIADO ANTES DE MANDAR PRO SID CLIENT: "+str(sid_creation_json_message))

            next_hop_transit.pop(0)

            print("Setting SIDs in Router: " + str(NANO.get_nano_agent_host("",NANO.NANO_ASN)))
            nano_sig_agent = grpc_sid_client.gRPC_SID("192.168.0.204", 123456, sid_creation_json_message)
            print("Nano SID Creation Response: "+str(nano_sig_agent.main()))

            for item in ASs:
                if str(item) != str(DATA['source']):
                    print("Encaminhar o Slice Creator para o NANO do AS: " + str(item))
                    next = IOExClient.slice_creation_forwarder(ASN, "CREATE_SLICE", DATA['details'],
                                                               NANO.get_nano_agent_host("", str(item)),
                                                               NANO.get_nano_agent_port("", str(item)), next_hop_transit)

            return




        #edib = eDomainInformationBase.eDomainInformationBase()

        #Check if ASN are neighbor
        #data = json.loads(edib.get_data_from_region("regionA"))
        # print(data['regionA'][0][1]['as_number'])

        #csvfile = open('./data/idomain_information_base.csv', 'r')
        #jsonfile = open('file.json', 'w')
        #fieldnames = ("domain_id","asn_name","asn","topology_agent","router_ingress_mgmt","switch_ingress_mgmt","switch_egress_mgmt","router_ingress_iface","swtich_ingress_iface","mano_entity")
        #reader = csv.DictReader(csvfile, fieldnames)
        #for row in reader:
        #    json.dump(row, jsonfile)
        #    jsonfile.write('\n')


        #for domain in data['regionA'][0]:
        #    # print(self.ASN)
        #    if domain['as_number'] == self.ASN:
        #        peering_interface_address = domain['peering_interface_address']
        #        peering_interface_name = domain['peering_interface_name']
        #        peering_router_ip = domain['peering_router']


        if int(ASN) == 16735:
            with open('data/inter-domain-16735.json') as f:
                intra_domain_data = json.load(f)
                #print(intra_domain_data)

        else:
            with open('data/inter-domain-26599.json') as f:
                intra_domain_data = json.load(f)
                #print(intra_domain_data)


        if NANO.target_encounter_check("",DATA['end2end_next_hop'], intra_domain_data['router_ingress_mgmt']):

            print("Encontrou o AS 16735, instalar as rotas e os SIDs")


            print("NANO.NANO_ASN: "+str(NANO.NANO_ASN))
            print("end2end_next_hop: "+str(DATA['end2end_next_hop']))

            next_hop_target = DATA['end2end_next_hop']

            sid_behaviour = "end"
            sid_creation_json_message = """{%ssid_ip%s: %s"""+str(next_hop_target[0])+"""%s, %ssid_behaviour%s: %s"""+str(sid_behaviour)+"""%s}"""
            sid_creation_json_message = str(sid_creation_json_message % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))
            sid_creation_json_message = json.loads(sid_creation_json_message)
            print("JSON CRIADO ANTES DE MANDAR PRO SID CLIENT: "+str(sid_creation_json_message))

            next_hop_target.pop(0)

            print("Setting SIDs in Router: " + str(NANO.get_nano_agent_host("",NANO.NANO_ASN)))
            nano_sig_agent = grpc_sid_client.gRPC_SID(intra_domain_data['router_ingress_mgmt'], 123456, sid_creation_json_message)
            print("Nano SID Creation Response: "+str(nano_sig_agent.main()))





        #Descobrir o AS_PATH que precisa ser percorrido para estabelecer o slice inter_domain
        #Conecta no router de ingresso do dominio e pesquisa as rotas BGP
        as_path = NANO.telnet_agent("",intra_domain_data['router_ingress_mgmt'],"",2605)

        #Verifico se o router possui rotas para o as path target do slice
        #A lista ASs contem os dois AS do slice, um deles e o da instancia do NANO
        for item in ASs:
            if str(item) != str(NANO.NANO_ASN):
                as_peer_slice = item

        print("AS_PEER_SLICE: "+str(as_peer_slice))

        as_path = as_path[280:]
        print(as_path)

        char1 = '*>'
        char2 = ' i'
        #print("Teste: "+as_path[as_path.find(char1) + 1: as_path.find(char2)])
        #as_path = as_path[as_path.find(char1) + 1: as_path.find(char2)]
        as_path = as_path.replace(" i", " #")
        #print(as_path)
        as_path = as_path.replace("*>", "#")
        #print("Ultimo: "+str(as_path))
        as_path = as_path.replace("\t", " ")
        #print("Sem Espaco: "+str(as_path))


        char1 = '#'
        char2 = ' #'
        #print("Start with: "+str(as_path.index("#")))
        #print("End with: "+str((as_path.index("#")+1).index("#")))
        rota_a = as_path[as_path.find(char1) + 1: as_path.find(char2)]
        rota_b = as_path[as_path.find(char1) + 1: as_path.find(char2)]

        rib_entries = []
        rib1 = as_path[as_path.index("#"): as_path.find(char2)]
        #print("RIB1: "+str(rib1))
        #print("SEPARA")
        rib1 = rib1.replace("\r"," ")
        #print("RIB1: "+str(rib1.rstrip()))
        #print("Index: "+str(as_path.find(char2)).index("#"))

        rib1 = re.sub(' +', ' ', rib1)
        #print("REGEX: "+rib1)
        rib1 = as_path.replace('\n', ' ').replace('\r', '')
        rib1 = re.sub(' +', ' ', rib1)
        #print("Remover enters: "+rib1)

        #print("Indice do Asterisco: "+str(rib1.index("*")))
        #print("Depois do Asteristo: "+str(rib1[rib1.index("*")+1:].find("#")))

        rib_list = []

        print(rib1[44+1:].find("#"))

        rib_entry = ""
        index = 0
        #print("Tamanho da rib1: "+str(len(rib1)))
        while index != len(rib1):
            #print("Index1: "+str(index))

            if rib1[index] == "#":
                #print("Entrou no for com Index1: "+str(index))
                for index2 in range(index+1, index + rib1[index+1:].find("#")+1):
                    rib_entry += rib1[index2]
                    #print("Index2: "+str(index2))
                    from_index = index2
                rib_list.append(rib_entry)
                rib_entry = ""
                #print(rib_list)
                index = from_index+2
                #print("Indice que vai partir: "+str(index))
            if rib1[index] == "*":
                #print("Faz nada ate encontrar outro #")
                for index2 in range(index+1, index+1 + rib1[index+1:].find("#")+1):
                    from_index = index2
                index = from_index
            index = index + 1

        #print("RIB_LIST: "+str(rib_list))

        rib_list_aux = []

        for string in rib_list:
            rib_list_aux.append(string.replace(" ",";"))

        rib_list = rib_list_aux
        print("RIB_LIST: "+str(rib_list))

        #Verifico qual entrada da rib_list possui o as_peer_slice, ou seja o AS do outro dominio que foi descrito no template
        #do slice
        #print(rib_list)
        slice_as_path = []
        slice_as_path_aux = []
        next_hop = []

        exit = 0
        for entry in rib_list:
            entry = entry.split(";")
            print("Entry: "+str(entry))
            for each in entry:
                if str(each) == str(as_peer_slice):
                    print("Encontrou a entrada que contem o AS target: "+str(entry))
                    if str(entry[2]) == str(0):
                        next_hop.append(entry[1])
                        slice_as_path.append(entry[4])
                        print("ENTRY[2]: " + str(entry[1])+ " Slice AS PATH: "+str(slice_as_path))
                        exit = 1
                        break
                    else:
                        slice_as_path = entry[-3:]
                        next_hop.append(entry[2])
                        print("SLICE AS PATH: " + str(slice_as_path) + " and next_hop: "+str(next_hop))
                    for item in slice_as_path:
                        if item != "":
                            slice_as_path_aux.append(item)
                    slice_as_path = slice_as_path_aux

            if exit == 1:
                break

        print("Slice AS_PATH: "+str(slice_as_path) + " Tamanho da lista do SLICE_AS_PATH: "+str(len(slice_as_path)))
        print("Primeiro Next_Hop: "+str(next_hop))

        if len(slice_as_path) > 1:

            for item in slice_as_path:
                if str(item) == str(16735):
                    #print("Entrou no if")
                    break
                print("Consultar o NANO do AS: "+str(item))
                next = IOExClient.next_hop_request("","GET_PATH",str(as_peer_slice),NANO.get_nano_agent_host("",item),8014)
                next_hop.append(next)


            print("Lista de Next Hop: "+str(next_hop))


            #print("Desencadear aqui chamadas ao grpc para instalar as rotas e os SIDs desse dominio")
            #print("ENDERECO INTERFACE DE PEERING: "+peering_interface_address)
            #print("NOME INTERFACE DE PEERING: "+peering_interface_name)
            #print("ROUTER DE PEERING: "+peering_router_ip)
            #print("AS CORRENT: "+str(self.ASN))
            #print("Terminou de configurar os parametros do slice nesse dominio, envia o NSTD para o outro")
            #print("Procure na lista de ASs qual o NANO Agent do outro dominio")
            #for item in self.ASes:
            #    if item != self.ASN:
            #        for domain in data['regionA'][0]:
            #            if domain['as_number'] != self.ASN:
            #                print("ENVIANDO PARA: "+str(domain['nano_agent']))
            #                print("Domain Name: "+str(domain['as_name']))
            #                neighbor_border_segment_id = str(domain['border_segment_id'])
            #                #IOExClient.nstd_nano_exchange("192.168.0.104",self.NSTD,domain['nano_agent'])

            data ="""
          [
            {
              "paths": [
                {
                  "via": "%s",
                  "device": "%s",
                  "destination": "a::/64",
                  "encapmode": "encap",
                  "segments": [
                    "%s", "%s"
                  ]
                }
              ]
            }
          ]
          """
            data = str(data % ("via", NANO.get_egress_interface(self, next_hop), next_hop[1], next_hop[0]))
            print(data)
            grpc_route_agent = grpc_client.gRPC_Route(intra_domain_data['router_ingress_mgmt'],12345,data)
            grpc_route_agent.main()
            print("Egrees Router Config done!")

            for item in slice_as_path:
                # print("ITEM: "+str(item))
                # print("AS_PEER_SLICE: "+str(as_peer_slice))
                if str(item) != str(as_peer_slice):
                    print("Encaminhar o Slice Creator para o NANO do AS: " + str(item))
                    next = IOExClient.slice_creation_forwarder(ASN, "CREATE_SLICE", DATA['details'],
                                                               NANO.get_nano_agent_host("", str(item)),
                                                               NANO.get_nano_agent_port("", str(item)), next_hop)

            return

        else:

            print("next_hop_len igual a 1")

            data = """
                      [
                        {
                          "paths": [
                            {
                              "via": "%s",
                              "device": "%s",
                              "destination": "b::/64",
                              "encapmode": "encap",
                              "segments": [
                                "%s"
                              ]
                            }
                          ]
                        }
                      ]
                      """
            data = str(data % ("via", NANO.get_egress_interface(self, next_hop), next_hop[0]))
            print(data)
            grpc_route_agent = grpc_client.gRPC_Route(intra_domain_data['router_ingress_mgmt'], 12345, data)
            grpc_route_agent.main()
            print("Domain A Config done!")

            print("Encaminhar o Slice Creator para o NANO do AS: " + str(item))
            next = IOExClient.slice_creation_forwarder(ASN, "CREATE_SLICE", DATA['details'],
                                                               NANO.get_nano_agent_host("", str(item)),
                                                               NANO.get_nano_agent_port("", str(item)), next_hop)



            return
        # '''
        # Getting Informations about other partner domain
        # '''
        # print("Configuring Ingress Border Route")
        # domain_partner = json.loads(edib.get_data_from_region("regionA"))
        # for domain in domain_partner['regionA'][0]:
        #     if domain['as_number'] == self.ASN:
        #
        #         data ="""
        #       [
        #         {
        #           "paths": [
        #             {
        #               "via": "%s",
        #               "device": "%s",
        #               "destination": "a::/64",
        #               "encapmode": "encap",
        #               "segments": [
        #                 "%s"
        #               ]
        #             }
        #           ]
        #         }
        #       ]
        #       """
        #         print(str(domain['border_segment_id']))
        #         data = str(data % ("via", "eth1", str(domain['border_segment_id'])))
        #         print(data)
        #         teste2 = grpc_client.gRPC_Route(peering_router_ip, 12345, data)
        #         teste2.main()
        #         print("Ingress Route Config done!")
        #
        #
        # print("Setting SIDs: "+str(peering_router_ip))
        # nano_sig_agent = grpc_sid_client.gRPC_SID(peering_router_ip, 123456,"")
        # nano_sig_agent.main()


    # Parse options
    def parse_options(self):
        global SECURE
        parser = OptionParser()
        parser.add_option("-d", "--debug", action="store_true", help="Activate debug logs")
        parser.add_option("-s", "--secure", action="store_true", help="Activate secure mode")
        # Parse input parameters
        (options, args) = parser.parse_args()
        # Setup properly the logger
        if options.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        # Setup properly the secure mode
        if options.secure:
            SECURE = True
        else:
            SECURE = False
        SERVER_DEBUG = logging.getEffectiveLevel() == logging.DEBUG
        logging.info("SERVER_DEBUG:" + str(SERVER_DEBUG))

    def nano_rib_request_listener(self):
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.bind((self.NANO_HOST, self.NANO_PORT+1))
        serv.listen(5)
        print("RIB Request Listener is Running on Port: "+str(self.NANO_PORT+1))
        while True:
            conn, addr = serv.accept()
            from_client = ''
            while True:
                data = conn.recv(4096)
                if not data: break
                from_client += data.decode()
                from_client = json.loads(from_client)
                print("JSON Cliente: "+str(from_client))
                response = str(self.get_next_hop(from_client['details']))
                print("Pronto para devolver para o 26599: "+str(response))
                conn.send(response.encode())
            conn.close()
            print('client disconnected')

    def run(self):
        print("ASN: " + str(self.NANO_ASN) + " is Ready")
        logging.debug("NANO ASN: " + str(self.NANO_ASN) + " Listenner is running")
        self.nano_rib_request_listener()

    def service_builder_listener(self, NANO_HOST, NANO_PORT):
        import InterOrchestratorExchange
        InterOrchestratorExchange.nano_receier(NANO_HOST, NANO_PORT, NANO_ASN)

#    def slice_policy_listener(self, NANO_HOST, NANO_PORT, NANO_ASN):
#        logging.debug("Policy ASN: " + str(NANO_ASN) + " Listenner is running")
#        SlicePolicyAPI.slice_policy_listener(NANO_HOST, int(NANO_PORT) + 10, NANO_ASN)

if __name__ == '__main__':

    logging.debug('Running by IDE - NANO')

    if int(sys.argv[2]) > 0:
        NANO_ASN = int(sys.argv[2])
    else:
        print("ASN should be a valid number")
    if str(sys.argv[3]) != "":
        NANO_HOST = sys.argv[3]
    else:
        print("NANO IP soud be a valid IP Address")
    if int(sys.argv[4]) != "" and int(sys.argv[4]) > 0:
        NANO_PORT = int(sys.argv[4])
    else:
        print("NANO Port should be a valid Port Number")

    import OpenPolicyInterface

    #slice_policy_listener = threading.Thread(target=NANO.slice_policy_listener, args=(1,NANO_HOST,NANO_PORT, NANO_ASN))
    service_builder_listenner = threading.Thread(target=NANO.service_builder_listener, args=(1,NANO_HOST,NANO_PORT))
    nano_listenner = NANO(4,NANO_ASN, NANO_HOST, NANO_PORT)
    nano_listenner.start()
    service_builder_listenner.start()
    #slice_policy_listener.start()
    nano_listenner.join()


    print("Algo apos o openpolicy import - NANO")
else:
    logging.debug('Imported in somewhere place - NANO')


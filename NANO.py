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
from io import StringIO
from optparse import OptionParser
import json, logging, sys

import read as read

import CoreDomainTopology
import eDomainInformationBase
import iDomainInformationBase

import pandas as pd
import re

import getpass
import sys
import telnetlib
import csv

sys.path.insert(1, './segment-routing')
import grpc_client
import grpc_sid_client

# logger reference
logging.basicConfig(level=logging.DEBUG)

import IOExClient

# Debug option
SERVER_DEBUG = False

from threading import Thread


class NANO(Thread):

    NSTD = None
    ASN = ""
    ASes = []

    '''
    Constructor
    '''
    def __init__(self, val, ASN):
        super(NANO, self).__init__()
        self.val = val
        self.ASN = ASN

    def get_recursive_as_path(self, caller):
        print("TO-DO")


    def nst_yaml_interpreter(NSTD):
        ct = CoreDomainTopology.CoreTopology()
        return NSTD[0]['asns']
        #return ct.neighborhood_check(str(self.NSTD[0]['asns']))

    def telnet_agent(self, HOST):

        user = ""
        password = "zebra\r\n"
        command = "show ipv6 bgp\r\n"

        tn = telnetlib.Telnet(HOST, 2605)

        l = tn.read_until("Password: ".encode())
        #print("Primeira tela ao requisitar login: " + str(l))

        tn.write(password.encode())
        l = tn.read_until("border> ".encode())
        #print("Resultado pos entrar com password: " + str(l))

        tn.write(command.encode())
        l = tn.read_until("Total number of prefixes".encode()).decode()
        tn.close()
        return str(l)

    def get_nano_agent(self, ASN):
        "Procurar na Base de Orchestradores do IP do Nano dado um ASN"
        if str(ASN) == str(7675):
            return "192.168.0.105"
        elif str(ASN) == str(16735):
            return "192.168.0.105"
        elif str(ASN) == str(26599):
            return "192.168.0.105"

    def get_next_hop(self, ASN):
        #Descobrir o AS_PATH que precisa ser percorrido para estabelecer o slice inter_domain
        #Conecta no router de ingresso do dominio e pesquisa as rotas BGP

        #as_path = NANO.telnet_agent("",NANO.get_nano_agent("",ASN))
        as_path = NANO.telnet_agent("", "192.168.0.204")

        as_path = as_path[280:]
        print(as_path)

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
        print("Depois do Asteristo: " + str(rib1[rib1.index("*") + 1:].find("#")))

        rib_list = []

        # print(rib1[44+1:].find("#"))

        rib_entry = ""
        index = 0
        print("Tamanho da rib1: " + str(len(rib1)))
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

        print("RIB_LIST: " + str(rib_list))

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

        return next_hop

    def eDomain_slice_builder(self, NSTD):

        ASs = NANO.nst_yaml_interpreter(NSTD)
        print("ASs do Slice: "+str(ASs))


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


        with open('inter-domain.json') as f:
            intra_domain_data = json.load(f)
            print(intra_domain_data)

        #Descobrir o AS_PATH que precisa ser percorrido para estabelecer o slice inter_domain
        #Conecta no router de ingresso do dominio e pesquisa as rotas BGP
        as_path = NANO.telnet_agent("",intra_domain_data['router_ingress_mgmt'])

        #Verifico se o router possui rotas para o as path target do slice
        #A lista ASs contem os dois AS do slice, um deles e o da instancia do NANO
        for item in ASs:
            if str(item) != "26599":
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
        print("Depois do Asteristo: "+str(rib1[rib1.index("*")+1:].find("#")))

        rib_list = []

        #print(rib1[44+1:].find("#"))

        rib_entry = ""
        index = 0
        print("Tamanho da rib1: "+str(len(rib1)))
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

        print("RIB_LIST: "+str(rib_list))

        rib_list_aux = []

        for string in rib_list:
            rib_list_aux.append(string.replace(" ",";"))

        rib_list = rib_list_aux

        #Verifico qual entrada da rib_list possui o as_peer_slice, ou seja o AS do outro dominio que foi descrito no template
        #do slice
        print(rib_list)
        slice_as_path = []
        slice_as_path_aux = []
        next_hop = []

        for entry in rib_list:
            entry = entry.split(";")
            for each in entry:
                if str(each) == str(as_peer_slice):
                    print("Encontrou a entrada que contem o AS target: "+str(entry))
                    slice_as_path = entry[-3:]
                    next_hop = entry[2]
                    for item in slice_as_path:
                        if item != "":
                            slice_as_path_aux.append(item)
                    slice_as_path = slice_as_path_aux



        print("Slice AS_PATH: "+str(slice_as_path))
        print("Next_Hop: "+str(next_hop))

        for item in slice_as_path:
            print("Consultar o NANO do AS: "+str(item))
            IOExClient.nano_exchange("","GET_PATH",item,"192.168.0.104",8011)

        return
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
        data = str(data % ("via", peering_interface_name, neighbor_border_segment_id))
        print(data)
        teste = grpc_client.gRPC_Route(peering_router_ip,12345,data)
        teste.main()
        print("Egrees Router Config done!")



        '''
        Getting Informations about other partner domain
        '''
        print("Configuring Ingress Border Route")
        domain_partner = json.loads(edib.get_data_from_region("regionA"))
        for domain in domain_partner['regionA'][0]:
            if domain['as_number'] == self.ASN:

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
                        "%s"
                      ]
                    }
                  ]
                }
              ]
              """
                print(str(domain['border_segment_id']))
                data = str(data % ("via", "eth1", str(domain['border_segment_id'])))
                print(data)
                teste2 = grpc_client.gRPC_Route(peering_router_ip, 12345, data)
                teste2.main()
                print("Ingress Route Config done!")


        print("Setting SIDs: "+str(peering_router_ip))
        nano_sig_agent = grpc_sid_client.gRPC_SID(peering_router_ip, 123456,"")
        nano_sig_agent.main()


    def run(self):
        print("NANO ASN: "+str(self.ASN)+" Listenner is running")
        logging.debug("NANO ASN: "+str(self.ASN)+" Listenner is running")
        import InterOrchestratorExchange
        InterOrchestratorExchange.nano_receier("192.168.0.104",8011)

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

if __name__ == '__main__':
    logging.debug('Running by IDE - NANO')
    nano_listenner = NANO(4,26599)
    nano_listenner.setName('NANO Listenner 1')
    nano_listenner.start()
    nano_listenner.join()
else:
    logging.debug('Impomrted in somewhere place - NANO')
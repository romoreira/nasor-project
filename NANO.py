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

from optparse import OptionParser
import json, logging, sys
import CoreDomainTopology
import eDomainInformationBase
import iDomainInformationBase

sys.path.insert(1, './segment-routing')
import grpc_client
import grpc_sid_client

# logger reference
logging.basicConfig(level=logging.DEBUG)

import InterOrchestratorExchange
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
    def __init__(self, val, NSTD, ASN):
        super(NANO, self).__init__()
        self.val = val
        self.NSTD = NSTD
        self.ASN = ASN



    def nst_yaml_interpreter(self, NSTD):
        ct = CoreDomainTopology.CoreTopology()
        self.ASes = self.NSTD[0]['asns']
        return ct.neighborhood_check(str(self.NSTD[0]['asns']))

    def eDomain_slice_builder(self):

        self.nst_yaml_interpreter(self)

        edib = eDomainInformationBase.eDomainInformationBase()

        #Check if ASN are neighbor
        if self.nst_yaml_interpreter(self.NSTD):
            data = json.loads(edib.get_data_from_region("regionA"))
            #print(data['regionA'][0][1]['as_number'])
            for domain in data['regionA'][0]:
                #print(self.ASN)
                if domain['as_number'] == self.ASN:
                    peering_interface_address = domain['peering_interface_address']
                    peering_interface_name = domain['peering_interface_name']
                    peering_router_ip = domain['peering_router']

        print("Desencadear aqui chamadas ao grpc para instalar as rotas e os SIDs desse dominio")
        print("ENDERECO INTERFACE DE PEERING: "+peering_interface_address)
        print("NOME INTERFACE DE PEERING: "+peering_interface_name)
        print("ROUTER DE PEERING: "+peering_router_ip)
        print("AS CORRENT: "+str(self.ASN))
        print("Terminou de configurar os parametros do slice nesse dominio, envia o NSTD para o outro")
        print("Procure na lista de ASs qual o NANO Agent do outro dominio")
        for item in self.ASes:
            if item != self.ASN:
                for domain in data['regionA'][0]:
                    if domain['as_number'] != self.ASN:
                        print("ENVIANDO PARA: "+str(domain['nano_agent']))
                        print("Domain Name: "+str(domain['as_name']))
                        neighbor_border_segment_id = str(domain['border_segment_id'])
                        #IOExClient.nstd_nano_exchange("192.168.0.104",self.NSTD,domain['nano_agent'])

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
        logging.info("NANO ASN: "+str(self.ASN)+" Listenner is running")
        InterOrchestratorExchange.nano_slice_receier()

    # Parse options
    def parse_options():
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
        SERVER_DEBUG = logger.getEffectiveLevel() == logging.DEBUG
        logger.info("SERVER_DEBUG:" + str(SERVER_DEBUG))

if __name__ == '__main__':
    logging.debug('Running by IDE - NANO')
    nano_listenner = NANO(4,NANO.NSTD,16735)
    nano_listenner.setName('NANO Listenner 1')
    nano_listenner.start()
    nano_listenner.join()
else:
    logging.debug('Impomrted in somewhere place - NANO')
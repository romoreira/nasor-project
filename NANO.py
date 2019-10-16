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

import json, logging, time, socket, sys, pycos
import CoreDomainTopology
import eDomainInformationBase
import iDomainInformationBase

import InterOrchestratorExchange
import IOExClient

from threading import Thread
from random import randint

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

        #Check if ASN are neighbor
        if self.nst_yaml_interpreter(self.NSTD):
            edib = eDomainInformationBase.eDomainInformationBase()
            data = json.loads(edib.get_data_from_region("regionA"))
            #print(data['regionA'][0][1]['as_number'])
            for domain in data['regionA'][0]:
                #print(self.ASN)
                if domain['as_number'] == self.ASN:
                    peering_interface_address = domain['peering_interface_address']
                    peering_interface_name = domain['peering_interface_name']
                    peering_router = domain['peering_router']

        print("Desencadear aqui chamadas ao grpc para instalar as rotas e os SIDs desse dominio")
        print("ENDERECO INTERFACE DE PEERING: "+peering_interface_address)
        print("NOME INTERFACE DE PEERING: "+peering_interface_name)
        print("ROUTER DE PEERING: "+peering_router)
        print("AS CORRENT: "+str(self.ASN))
        print("Terminou de configurar os parametros do slice nesse dominio, envia o NSTD para o outro")
        print("Procure na lista de ASs qual o NANO Agent do outro dominio")
        for item in self.ASes:
            if item != self.ASN:
                for domain in data['regionA'][0]:
                    if domain['as_number'] != self.ASN:
                        print("ENVIANDO PARA: "+str(domain['nano_agent']))
                        print("Domain NAME: "+str(domain['as_name']))
                        IOExClient.nstd_nano_exchange("192.168.0.103",self.NSTD,domain['nano_agent'])


    def run(self):
        print("NANO ASN: "+str(self.ASN)+" Listenner is running")
        logging.info("NANO ASN: "+str(self.ASN)+" Listenner is running")
        InterOrchestratorExchange.nano_slice_receier()

if __name__ == '__main__':

    nano_listenner = NANO(4,NANO.NSTD,16735)
    nano_listenner.setName('NANO Listenner 1')
    nano_listenner.start()
    nano_listenner.join()
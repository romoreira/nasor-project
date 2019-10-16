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

import json
import CoreDomainTopology
import eDomainInformationBase
import iDomainInformationBase

class NANO:
    NSTD = None
    ASes = []

    def __init__(self, NSTD):
        self.NSTD = NSTD
        self.ASes = []

    def nst_yaml_interpreter(self, NSTD):
        ct = CoreDomainTopology.CoreTopology()
        self.ASes = self.NSTD[0]['asns']
        return ct.neighborhood_check(str(self.NSTD[0]['asns']))

    def eDomain_slice_builder(self):

        #Check if ASN are neighbor
        if self.nst_yaml_interpreter(self.NSTD):
            edib = eDomainInformationBase.eDomainInformationBase()
            data = json.loads(edib.get_data_from_region("regionA"))
            print(data['regionA'][0][1]['as_number'])
            for item in self.ASes:
                for domain in data['regionA'][0]:
                    if domain['as_number'] == item:
                        print(domain['peering_interface_name'])

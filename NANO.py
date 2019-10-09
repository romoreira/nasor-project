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


import CoreDomainTopology

class NANO:
    NSTD = None

    def __init__(self, NSTD):
        self.NSTD = NSTD

    def nst_yaml_interpreter(self, NSTD):
        self.NSDT = NSTD

        ct = CoreDomainTopology.CoreTopology()
        ct.neighborhood_check(str(self.NSTD[0]['asns']))

    def interDomain_slice_builder(self):
        print("Construir o Slice!")
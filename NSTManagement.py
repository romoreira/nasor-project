'''
Author: Rodrigo Moreira
Date: 06/09/2019
'''

import yaml

# 1 - Uma vez que recebeu o NST e necessario verificar dois casos - se os asn sao vizinhos ou nao:
# 2 - Se forem vizinhos, instanciar a VNF e fazer uma chamada a entidade de cada dominio para mapear a VNF ate a borda
# 3 - Se nao forem vizinhos, instanciar SR para garantir o by-pass nesse dominio neutro

import CoreTopology

class NSTManagement:

    NSD = None

    def __init__(self, NSD):
        self.NSD = NSD

    def nst_yaml_interpreter(self):
        print(str(self.NSD['asn-involved']))
        ct = CoreTopology.CoreTopology()
        ct.neighborhood_check(str(self.NSD['asn-involved']))




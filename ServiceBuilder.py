'''
Author: Rodrigo Moreira
Date: 06/09/2019
'''

#Each Service Builder in each Domain is able to receibe NSD to proced with service deployment

import yaml

class ServiceBuilder:
    NSD = None

    def read_nsd(self):
        with open("./vnf-descriptor/cirros_vnf/cirros_vnfd.yaml", 'r') as stream:
            NSD = yaml.safe_load(stream)
        self.NSD = NSD

    def nmano_call(self):
        print("Call here nmano")


if __name__ == "__main__":
    sb = ServiceBuilder()
    sb.read_nsd()
    sb.nmano_call()
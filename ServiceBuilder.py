'''
Author: Rodrigo Moreira
Date: 06/09/2019
'''

#Each Service Builder in each Domain is able to receibe NSD to proced with service deployment

import yaml
import NSTManagement
import MANO

class ServiceBuilder:
    NSD = None
    VNFD = None

    def read_nsd(self):
        with open("./vnf-descriptor/cirros_2vnf_ns/cirros_2vnf_nsd.yaml", 'r') as stream:
            NSD = yaml.safe_load(stream)

        self.NSD = NSD['nstd:nstd-details']
        self.VNFD = NSD['nsd:nsd-catalog']

    def network_slice_template(self):
        nmano = NSTManagement.NSTManagement(self.NSD)
        nmano.nst_yaml_interpreter()

    def virtual_network_function_description(self):
        mano = MANO.MANO(self.VNFD)
        mano.vnfd_yaml_interpreter()

if __name__ == "__main__":
    sb = ServiceBuilder()
    sb.read_nsd()

    #Splitting YAML service descriptor to OSM and Netowrk mine Network Slice Builder
    sb.network_slice_template()
    sb.virtual_network_function_description()
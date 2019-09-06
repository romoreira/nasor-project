'''
Author: Rodrigo Moreira
Date: 06/09/2019
'''

import yaml

with open("./vnf-descriptor/cirros_vnf/cirros_vnfd.yaml", 'r') as stream:
    print(yaml.safe_load(stream))
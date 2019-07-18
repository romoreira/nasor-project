'''
Author: Rodrigo Moreira
'''

from socket import AF_INET
from pyroute2 import IPRoute
from yaml import *

# get access to the netlink socket
ip = IPRoute()

# no monitoring here -- thus no bind()

# print interfaces
print(ip.get_default_routes())




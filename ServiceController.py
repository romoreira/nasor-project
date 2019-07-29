'''
Author: Rodrigo Moreira
'''

import logging
from geopy.geocoders import Nominatim


'''
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
logging.basicConfig(level=logging.DEBUG)
logging.debug('This will get logged')
'''

logging.basicConfig(level=logging.INFO)
logging.debug('This will get logged')

class Service:

    def __init__(self, device_id, device_latitude, device_longitude, in_port,
                 container_tos, spi, si, sff_next_hop, nsh_to_sf, transport):
        self.device_id = device_id
        self.device_latitude = device_latitude
        self.device_longitude = device_longitude
        self.in_port = in_port
        self.container_tos = container_tos
        self.spi = spi
        self.si = si
        self.sff_next_hop = sff_next_hop
        self.nsh_to_sf = nsh_to_sf
        self.transport = transport


#service_map = {'in_port' : 2, 'container_tos':'cdn',  'spi': 10, 'si': 3, 'sff_next_hop': '192.168.0.1', 'nsh_to_sf': 'sf2', 'transport': 'vxlan'}


#geolocator = Nominatim(user_agent="EdgeSlicer")
#location = geolocator.reverse("-19.4605259,-45.5948382")
#print(location.address)




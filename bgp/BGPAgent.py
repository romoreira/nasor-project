"""
Author: Rodrigo Moreira
Date: 04/11/2019
"""
import time
from _socket import AF_INET
from pyroute2 import IPRoute
from threading import Thread
import logging
import hashlib
import pycos
import socket
import json

logging.basicConfig(level=logging.DEBUG)

class BGPAgent(Thread):

    global router_domain
    global router_id
    routes_state = ""

    def __init__(self, ROUTER_ID, ROUTER_DOMAIN):
        Thread.__init__(self)
        self.router_id = ROUTER_ID
        self.router_domain = ROUTER_DOMAIN
        self.routes_state = self.hash_route_string(str(self.list_routes()))


    def hash_route_string(self, routes):
        hash_object = hashlib.sha256(routes.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def list_routes(self):

        with IPRoute() as ipr:
            # this request returns one match
            routes = ipr.get_routes(family=AF_INET)
            return routes

    def get_routes_state(self):
        return self.routes_state

    def set_routes_state(self, routes_state):
        self.routes_state = routes_state

    def speaker_proc(host, port, n, task=None):
        # Create a TCP Socket over port 8011 - we may change it further - with pycos we can create more than one socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = pycos.AsyncSocket(sock)
        yield sock.connect((host, port))
        msg = str(BGPAgent.list_routes("")) + '/'
        msg = msg.encode()
        yield sock.sendall(msg)
        sock.close()

    def speaker_proc_register_in_bgp_server(host, port, n, task=None):
        # Create a TCP Socket over port 8011 - we may change it further - with pycos we can create more than one socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = pycos.AsyncSocket(sock)
        yield sock.connect((host, port))

        print(router_domain)
        json_msg = """{ "router-id": %s, "asn": %s }"""
        json_msg = str(json_msg % (BGPAgent.router_id, BGPAgent.router_domain))
        print(str(json_msg))
        return

        msg = str("ROUTER_IP: 192.168.0.202;ASN: 16735") + '/'
        msg = msg.encode()
        yield sock.sendall(msg)
        sock.close()

    def register_to_bgp_server(self):
        logging.debug("Registering on DomainBGP Server - after it will able to reach the router")
        for n in range(1, 2):
            teste = pycos.Task(BGPAgent.speaker_proc_register_in_bgp_server, "192.168.0.104", 8012, n)

    def run(self):
        self.register_to_bgp_server()
        # while True:
        #     if self.get_routes_state() != str(self.hash_route_string(str(self.list_routes()))):
        #         logging.debug("The routes were changed - Sent it to BGPServer")
        #         self.set_routes_state(self.hash_route_string(str(self.list_routes())))
        #         for n in range(1, 2):
        #             teste = pycos.Task(BGPAgent.speaker_proc, "192.168.0.105", 8011, n)
        #     else:
        #         logging.info("As rotas nao mudaram - nada a fazer - dormir por tres segundos")
        #
        #     # Sleep for random time between 1 ~ 3 second
        #     secondsToSleep = 3
        #     time.sleep(secondsToSleep)

if __name__ == '__main__':
    logging.debug('Running by IDE - BGPAgent')

    routeListener = BGPAgent("192.168.0.202", "16735")
    routeListener.setName('Router-Name')

    logging.debug("Antes de Executar a Thread o estado das rotas e: "+routeListener.get_routes_state())

    routeListener.start()

else:
    logging.debug('Imported in somewhere place - BGPAgent')

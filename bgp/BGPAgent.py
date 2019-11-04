"""
Author: Rodrigo Moreira
Date: 04/11/2019
"""
import time
from _socket import AF_INET
from array import array
from random import randint
from pyroute2 import IPRoute
from threading import Thread
import logging
import hashlib

logging.basicConfig(level=logging.DEBUG)

class BGPAgent(Thread):

    router_id = ""
    routes_state = ""

    def __init__(self, ROUTER_ID):
        Thread.__init__(self)
        self.router_id = ROUTER_ID
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

    def run(self):
        while True:
            if self.get_routes_state() != str(self.hash_route_string(str(self.list_routes()))):
                print("As rotas mudaram fazer algo")
                self.set_routes_state(self.hash_route_string(str(self.list_routes())))
            else:
                print("As rotas nao mudaram - nada a fazer - dormir por tres segundos")

            # Sleep for random time between 1 ~ 3 second
            secondsToSleep = 3
            time.sleep(secondsToSleep)

if __name__ == '__main__':
    logging.debug('me executou pelo terminal - MANO')


    routeListener = BGPAgent("192.168.0.105")
    routeListener.setName('Thread-Router-192.168.0.10')

    print("Antes de Executar a Thread o estado das rotas e: "+routeListener.get_routes_state())

    routeListener.start()




else:
    print('me executou como um módulo - Importado em algum lugar')

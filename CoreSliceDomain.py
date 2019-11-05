"""
Author: Rodrigo Moreira
Date: 04/11/2019
"""

from threading import Thread
import logging
import time
import hashlib

logging.basicConfig(level=logging.DEBUG)

class CoreSliceDomain(Thread):

    slice_list = []


    def __init__(self, DOMAIN_ID):
        Thread.__init__(self)
        self.slice_list = []

    def run(self):
        while True:
            print("Doing something when CoreSliceDomain receives a message from a switch abroad")

            # Sleep for random time between 1 ~ 3 second
            secondsToSleep = 3
            time.sleep(secondsToSleep)

if __name__ == '__main__':
    logging.debug('me executou pelo terminal - MANO')

    routeListener = CoreSliceDomain("16735")
    routeListener.setName('Thread-Domain-16735')

    routeListener.start()

else:
    print('me executou como um módulo - Importado em algum lugar')
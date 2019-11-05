"""
Author: Rodrigo Moreira
Date: 04/11/2019
"""

from threading import Thread
import logging
import time
import RouterCommunication

logging.basicConfig(level=logging.DEBUG)

class CoreSliceDomain(Thread):

    slice_list = []


    def __init__(self, DOMAIN_ID):
        Thread.__init__(self)
        self.slice_list = []

    def run(self):
        while True:
            logging.debug("Doing something BGP Server - RouterCommunication is Running as module")

            # Sleep for random time between 1 ~ 3 second
            secondsToSleep = 3
            time.sleep(secondsToSleep)

if __name__ == '__main__':
    logging.debug('Running by IDE - BGPServer')

    routeListener = CoreSliceDomain("16735")
    routeListener.setName('Thread-Domain-16735')

    routeListener.start()


else:
    logging.debug("Imported in somwehere place - BGPServer")
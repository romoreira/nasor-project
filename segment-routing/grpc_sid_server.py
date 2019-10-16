"""
Author: Rodrigo Moreira
Date: 15/10/2019
"""


import grpc
import time
import hashlib
import sid_management_pb2
import sid_management_pb2_grpc
from concurrent import futures
from concurrent import futures
from optparse import OptionParser
from pyroute2 import IPRoute
from google.protobuf import json_format

import os
import logging
import time
import json
import grpc


# Global variables definition

# Server reference
grpc_server = None
# Netlink socket
ip_route = None
# Cache of the resolved interfaces
interfaces = ['enp2s0']
idxs = {}
# logger reference
logger = logging.getLogger(__name__)
# Server ip and port
GRPC_IP = "::"
GRPC_PORT = 12345
# Debug option
SERVER_DEBUG = False
# Secure option
SECURE = False
# Server certificate
CERTIFICATE = "cert_server.pem"
# Server key
KEY = "key_server.pem"


class SIDManagement(sid_management_pb2_grpc.SIDManagementServicer):
    """
    gRPC server for Digestor Service
    """

    def __init__(self, *args, **kwargs):
        self.server_port = 46001

    def AddSID(self, request, context):
        logger.debug("SID Config received:\n%s", request)


        for sid in request.sid:
            # Base: sudo srconf localsid add 2::AD6:F1 end.ad6 ip 2:f1::f1 veth1_2 veth1_2
            command = 'sudo srconf localsid add ' + str(sid.SID)+' '+str(sid.SID_BEHAVIOR)+' ip '+str(sid.IP_ADDR)+' '+str(sid.TARGET_IF)+' '+str(sid.SOURCE_IF)

            p = os.popen(command).read()

            logging.info("SID Added - "+str(command)+ " Command Output: "+str(p))


        return sid_management_pb2.SIDMessageReply(message="SID Created")

    def DelSID(self, request, context):
        print("Hello World DEL")
        return sid_management_pb2.SIDMessageReply(message="SID Deleted")

    # Start gRPC server
    def start_server(self):
        # Configure gRPC server listener and ip route
        global grpc_server, ip_route
        # Setup gRPC server
        if grpc_server is not None:
            logger.error("gRPC Server is already up and running")
        else:
            # Create the server and add the handler
            grpc_server = grpc.server(futures.ThreadPoolExecutor())
            sid_management_pb2_grpc.add_SIDManagementServicer_to_server(SIDManagement(), grpc_server)
            # If secure we need to create a secure endpoint
            if SECURE:
                # Read key and certificate
                with open(KEY) as f:
                    key = f.read()
                with open(CERTIFICATE) as f:
                    certificate = f.read()
                # Create server ssl credentials
                grpc_server_credentials = grpc.ssl_server_credentials(((key, certificate,),))
                # Create a secure endpoint
                grpc_server.add_secure_port("[%s]:%s" % (GRPC_IP, GRPC_PORT), grpc_server_credentials)
            else:
                # Create an insecure endpoint
                grpc_server.add_insecure_port("[%s]:%s" % (GRPC_IP, GRPC_PORT))

        # Start the loop for gRPC
        logger.info("Listening gRPC on Port: "+str(GRPC_PORT))
        grpc_server.start()
        while True:
            time.sleep(5)

    # Parse options
    def parse_options(self):
        global SECURE
        parser = OptionParser()
        parser.add_option("-d", "--debug", action="store_true", help="Activate debug logs")
        parser.add_option("-s", "--secure", action="store_true", help="Activate secure mode")
        # Parse input parameters
        (options, args) = parser.parse_args()
        # Setup properly the logger
        if options.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        # Setup properly the secure mode
        if options.secure:
            SECURE = True
        else:
            SECURE = False
        SERVER_DEBUG = logger.getEffectiveLevel() == logging.DEBUG
        logger.info("SERVER_DEBUG:" + str(SERVER_DEBUG))

if __name__ == "__main__":
    sid_management = SIDManagement()
    sid_management.parse_options()
    sid_management.start_server()
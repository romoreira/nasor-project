"""
Author: Rodrigo Moreira
Date: 15/10/2019
"""

import grpc

import sid_management_pb2_grpc
import sid_management_pb2

import logging
logging.basicConfig(level=logging.DEBUG)

# Define wheter to use SSL or not
SECURE = False
# SSL cerificate for server validation
CERTIFICATE = 'cert_client.pem'

class gRPC_SID():

  REMOTE_SERVER_IP = ""
  REMOTE_SERVER_PORT = ""
  data = ""

  def __init__(self, server, port, data):
    self.REMOTE_SERVER_IP = server
    self.REMOTE_SERVER_PORT = port
    self.data = data


  # Build a grpc stub
  def get_grpc_session(self, ip_address, port, secure):
    # If secure we need to establish a channel with the secure endpoint
    if secure:
      # Open the certificate file
      with open(CERTIFICATE) as f:
        certificate = f.read()
      # Then create the SSL credentials and establish the channel
      grpc_client_credentials = grpc.ssl_channel_credentials(certificate)
      channel = grpc.secure_channel("%s:%s" %(ip_address, port), grpc_client_credentials)
    else:
      channel = grpc.insecure_channel("%s:%s" %(ip_address, port))
    return sid_management_pb2_grpc.SIDManagementStub(channel), channel

  def main(self):
    print("Main - Dados vindo do construtor: "+str(self.data['sid_ip']))
    print("Main - Dados vindo do construtor: " + str(self.data['sid_behaviour']))
    # Get the reference of the stub
    sid_stub,channel = self.get_grpc_session(self.REMOTE_SERVER_IP, self.REMOTE_SERVER_PORT, SECURE)
    sid_request = sid_management_pb2.SIDMessage()
    sid = sid_request.sid.add()
    sid.SID = str(self.data['sid_ip'])
    sid.SID_BEHAVIOR  = str(self.data['sid_behaviour'])
    sid.IP_ADDR = ""
    sid.TARGET_IF = ""
    #sid.IP_ADDR  = str(self.data['ip_addr'])#For Experiments 2, uncoment it
    #sid.TARGET_IF  = str(self.data['target_if'])#For Experiments 2, uncoment it
    sid.SOURCE_IF  = ""

    response = sid_stub.AddSID(sid_request)
    channel.close()
    return str(response)


if __name__ == '__main__':
    logging.debug('Imported by IDE - grpc_sid_client')
    print("Passou pela main sid_client")
    sid_agent = gRPC_SID("192.168.0.202",123456, "")
    sid_agent.main()
else:
    logging.debug('Imported in somewhereplace - grpc_sid_client')
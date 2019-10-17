"""
Author: Rodrigo Moreira
Date: 15/10/2019
"""

import grpc

import sid_management_pb2_grpc
import sid_management_pb2

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
    # Get the reference of the stub
    sid_stub,channel = self.get_grpc_session(self.REMOTE_SERVER_IP, self.REMOTE_SERVER_PORT, SECURE)
    sid_request = sid_management_pb2.SIDMessage()
    sid = sid_request.sid.add()
    sid.SID = "1::d6"
    sid.SID_BEHAVIOR  = "end.dx6"
    sid.IP_ADDR  = "2:f3::f3"
    sid.TARGET_IF  = "eth1"
    sid.SOURCE_IF  = "eth0"


    response = sid_stub.AddSID(sid_request)
    print(str(response))
    channel.close()


if __name__ == '__main__':
    print('me executou pelo terminal')
    sid_agent = gRPC_SID("192.168.0.103",12345, "")
    sid_agent.data = """
      [
        {
          "paths": [
            {
              "via": "1:2::2",
              "device": "eth2",
              "destination": "b::/64",
              "encapmode": "encap",
              "segments": [
                "2::AD6:F1"
              ]
            }
          ]
        }
      ]
      """
    sid_agent.main()
else:
    print('me executou como um módulo')
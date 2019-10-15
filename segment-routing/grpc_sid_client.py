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

# Build a grpc stub
def get_grpc_session(ip_address, port, secure):
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

# Get the reference of the stub
sid_stub,channel = get_grpc_session("192.168.0.201", 12345, SECURE)
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
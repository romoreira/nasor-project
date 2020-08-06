# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import random
import logging

import grpc

import slice_create_pb2_grpc
import slice_create_pb2

def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = slice_create_pb2_grpc.SliceManagerStub(channel)
  response = stub.CreateSlice(slice_create_pb2.CreateRequest(name='you'))
  print("Creation - Client Received: " + response.message)
  response = stub.DeleteSlice(slice_create_pb2.DeleteRequest(name='you'))
  print("Deletion - Client Received: : " + response.message)



if __name__ == '__main__':
    logging.basicConfig()
    run()

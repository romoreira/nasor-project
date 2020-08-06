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
"""The Python implementation of the gRPC route guide server."""

from concurrent import futures
import time
import math
import logging

import grpc

import slice_create_pb2
import slice_create_pb2_grpc

class SliceManager(slice_create_pb2_grpc.SliceManagerServicer):

    def CreateSlice(self, request, context):
        print("Criar uma entrada na tabela SID")
        return slice_create_pb2.CreationReply(message='Creation Message, %s!' % request.name)

    def DeleteSlice(self, request, context):
        print("Deletar uma entrada da tabela SID")
        return slice_create_pb2.DeletionReply(message='Deletion Message, %s!' % request.name)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    slice_create_pb2_grpc.add_SliceManagerServicer_to_server(SliceManager(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

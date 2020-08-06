from concurrent import futures
import os
import logging
import grpc
import slice_create_pb2
import slice_create_pb2_grpc

class SliceManager(slice_create_pb2_grpc.SliceManagerServicer):

    def CreateSlice(self, request, context):
        command = "srconf localsid add "+str(request.SID)+" end"
        #print("Comando a ser executado: "+str(command))
        # os.system(command)
        return slice_create_pb2.CreationReply(message='Creation Message, %s' % request.SID)

    def DeleteSlice(self, request, context):
        command = "srconf localsid del "+str(request.SID)
        #print("Comando a ser executado: "+str(command))
        #os.system(command)
        return slice_create_pb2.DeletionReply(message='Deletion Message, %s' % request.SID)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    slice_create_pb2_grpc.add_SliceManagerServicer_to_server(SliceManager(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

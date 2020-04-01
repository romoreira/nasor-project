
import socket
import pycos
from threading import Thread
import logging
import json
import sys

logging.basicConfig(level=logging.DEBUG)

class SlicePolicyAPI(Thread):

    NANO_HOST = ""
    NANO_PORT = ""
    NANO_ASN = ""

    message = ""


    '''
    Constructor
    '''
def __init__(self, NANO_ASN, NANO_HOST, NANO_PORT):
    super(SlicePolicyAPI, self).__init__()
    self.NANO_ASN = NANO_ASN
    self.NANO_HOST = NANO_HOST
    self.NANO_PORT = NANO_PORT




def listener(conn, task=None):

    data = ''
    while True:
        data += (yield conn.recv(128)).decode('utf-8')
        if data[-1] == '/':
            break
    conn.close()
    # print("7675 Received: "+str(data))
    data = str(data[:-1])
    data = json.loads(data)

    if data['method'] == "CREATE_SLICE":
        print("\n***RECEBEU O PEDIDO DE APLICACAO DE POLITICA***\n")


def listener_proc(host, port, AS, task=None):

    global ASN
    ASN = AS

    task.set_daemon()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = pycos.AsyncSocket(sock)
    sock.bind((host, port))
    sock.listen(8)

    while True:
        conn, addr = yield sock.accept()
        pycos.Task(listener, conn)


def slice_policy_listener(NANO_HOST, NANO_PORT, NANO_ASN):

    print("SlicePolicy Receiver is Running on Port: " + str(NANO_PORT))

    pycos.Task(listener_proc, NANO_HOST, NANO_PORT, NANO_ASN)
    while True:
        cmd = sys.stdin.readline().strip().lower()
        if cmd == 'exit' or cmd == 'quit':
             break

def get_topology():
    print("Pronto para retornar a topologia")


if __name__ == '__main__':
    logging.debug('Running by IDE - SlicePolicyAPI')
else:
    logging.debug('Imported in somewhere place - SlicePolicyAPI')
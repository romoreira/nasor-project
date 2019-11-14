'''
Author: Rodrigo Moreira
Date: 27/08/2019
'''
#Important Links: https://github.com/Exa-Networks/exabgp/wiki/Other-OSS-BGP-implementations
#https://github.com/BytemarkHosting/bgpfeeder
#https://github.com/Exa-Networks/exabgp
#LINK Rest API Apache Geode: https://geode.apache.org/docs/guide/11/rest_apps/develop_rest_apps.html

import socket, sys, pycos, csv, logging,json, threading

from NANO import NANO

logging.basicConfig(level=logging.DEBUG)


ASN = ""


def oib_loader():
    with open('./data/edomain_information_base.csv') as OIB:
        OIB = csv.DictReader(OIB, delimiter=';')
        for row in OIB:
            print(row)

def listener(conn, task=None):

    data = ''
    while True:
        data += (yield conn.recv(128)).decode('utf-8')
        if data[-1] == '/':
           break
    conn.close()
    print("7675 Received: "+str(data))
    data = str(data[:-1])
    data = json.loads(data)

    if data['method'] == "CREATE_SLICE":
        print("RECEBEU O PEDIDO DE CRIACAO DE UM SLICE:")
        NANO.eDomain_slice_builder("", data, ASN)

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

def nano_receier(NANO_HOST, NANO_PORT, NANO_ASN):

    print("NANO Receiver is Running on Port: " +str(NANO_PORT))

    pycos.Task(listener_proc, NANO_HOST, NANO_PORT, NANO_ASN)
    while True:
        cmd = sys.stdin.readline().strip().lower()
        if cmd == 'exit' or cmd == 'quit':
            break

if __name__ == '__main__':
    logging.debug('Running by IDE - InterOrchestratorExchange')
    oib_loader()
    nano_receier()

else:
    #print("InterOrchestratorExchange is Running on Port: "+str(NANO.NANO_PORT))
    #nano_receier(NANO.NANO_HOST, NANO.NANO_PORT)
    logging.debug('Imported in somewhere place - InterOrchestratorExchange')
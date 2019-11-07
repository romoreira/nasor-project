'''
Author: Rodrigo Moreira
Date: 27/08/2019
'''
#Important Links: https://github.com/Exa-Networks/exabgp/wiki/Other-OSS-BGP-implementations
#https://github.com/BytemarkHosting/bgpfeeder
#https://github.com/Exa-Networks/exabgp
#LINK Rest API Apache Geode: https://geode.apache.org/docs/guide/11/rest_apps/develop_rest_apps.html

import socket, sys, pycos, csv, logging

logging.basicConfig(level=logging.DEBUG)

OIB = ''

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
    print('Received: %s' % data)
    print("NANO RECEBEU UM NSTD - DEVE CRIAR O SLICE NO SEU DOMINIO")

def listener_proc(host, port, task=None):
    task.set_daemon()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = pycos.AsyncSocket(sock)
    sock.bind((host, port))
    sock.listen(8)

    while True:
        conn, addr = yield sock.accept()
        pycos.Task(listener, conn)

def nano_slice_receier():

    pycos.Task(listener_proc, '192.168.0.105', 8010)
    while True:
        cmd = sys.stdin.readline().strip().lower()
        if cmd == 'exit' or cmd == 'quit':
            break

if __name__ == '__main__':
    logging.debug('Running by IDE - InterOrchestratorExchange')
    oib_loader()
    nano_slice_receier()

else:
    logging.debug('Imported in somewhere place - InterOrchestratorExchange')
'''
Author: Rodrigo Moreira
Date: 27/08/2019
'''
#Important Links: https://github.com/Exa-Networks/exabgp/wiki/Other-OSS-BGP-implementations
#https://github.com/BytemarkHosting/bgpfeeder
#https://github.com/Exa-Networks/exabgp

import socket, sys, pycos, csv, yaml

OIB = ''

def oib_loader():
    with open('./data/inter-orchestrator_information_base.csv') as OIB:
        OIB = csv.DictReader(OIB, delimiter=';')
        for row in OIB:
            print(row)
        print(yaml.dump(yaml.load(OIB), default_flow_style=False))


def listenner(conn, task=None):
    data = ''
    while True:
        data += (yield conn.recv(128)).decode('utf-8')
        if data[-1] == '/':
           break
    conn.close()
    print('Received: %s' % data)

def listenner_proc(host, port, task=None):
    task.set_daemon()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = pycos.AsyncSocket(sock)
    sock.bind((host, port))
    sock.listen(8)

    while True:
        conn, addr = yield sock.accept()
        pycos.Task(listenner, conn)

def oib_receier():

    pycos.Task(listenner_proc, '127.0.0.1', 8010)
    while True:
        cmd = sys.stdin.readline().strip().lower()
        if cmd == 'exit' or cmd == 'quit':
            break


if __name__ == "__main__":
    oib_loader()
    oib_receier()
'''
Author: Rodrigo Moreira
Date: 27/08/2019
'''
#Important Links: https://github.com/Exa-Networks/exabgp/wiki/Other-OSS-BGP-implementations
#https://github.com/BytemarkHosting/bgpfeeder
#https://github.com/Exa-Networks/exabgp

import socket, sys, pycos, csv

OIB = ''

def oib_loader():
    with open('orchestrator_information_base.csv') as OIB:
        OIB = csv.DictReader(OIB, delimiter=';')
        for row in OIB:
            print(row)
def process(conn, task=None):
    data = ''
    while True:
        data += (yield conn.recv(128)).decode('utf-8')
        if data[-1] == '/':
           break
    conn.close()
    print('received: %s' % data)

def server_proc(host, port, task=None):
    task.set_daemon()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = pycos.AsyncSocket(sock)
    sock.bind((host, port))
    sock.listen(128)

    while True:
        conn, addr = yield sock.accept()
        pycos.Task(process, conn)

# pycos.Task(server_proc, '127.0.0.1', 8010)
# while True:
#     cmd = sys.stdin.readline().strip().lower()
#     if cmd == 'exit' or cmd == 'quit':
#         oib_loader()
#         break

if __name__ == "__main__":
    oib_loader()
'''
Author: Rodrigo Moreira
Date: 27/08/2019
'''
#Important Links: https://github.com/Exa-Networks/exabgp/wiki/Other-OSS-BGP-implementations
#https://github.com/BytemarkHosting/bgpfeeder

import socket, sys, pycos, csv

OIB = ''

def fib_loader():
    with open('orchestrator_information_base.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for row in readCSV:
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

pycos.Task(server_proc, '127.0.0.1', 8010)
while True:
    cmd = sys.stdin.readline().strip().lower()
    if cmd == 'exit' or cmd == 'quit':
        fib_loader()
        break

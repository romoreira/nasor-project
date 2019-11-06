"""
Author: Rodrigo Moreira
Date: 05/11/2019
"""

import sys, pycos, logging, socket

logging.basicConfig(level=logging.DEBUG)

def listener(conn, task=None):
    data = ''
    while True:
        data += (yield conn.recv(128)).decode('utf-8')
        if data[-1] == '/':
           break
    conn.close()
    logging.debug("Received from BGPAgent: "+str(data))

def listener_proc(host, port, task=None):
    task.set_daemon()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = pycos.AsyncSocket(sock)
    sock.bind((host, port))
    sock.listen(8)

    while True:
        conn, addr = yield sock.accept()
        pycos.Task(listener, conn)

def routes_modification_listener():

    pycos.Task(listener_proc, '192.168.0.105', 8011)
    while True:
        cmd = sys.stdin.readline().strip().lower()
        if cmd == 'exit' or cmd == 'quit':
            break

if __name__ == '__main__':
    logging.debug('Running by IDE - RouterCommunication')
    routes_modification_listener()

else:
    logging.debug('Imported in somewhere place - RouterCommunication')
    routes_modification_listener()

"""
Author: Rodrigo Moreira
Date: 04/11/2019
"""

from threading import Thread
import logging
import pycos
import socket
import sys



logging.basicConfig(level=logging.DEBUG)

class BGPServer(Thread):

    routers_domain_list = []


    def __init__(self, DOMAIN_ID):
        Thread.__init__(self)
        self.routers_domain_list = []

    def listener(conn, task=None):
        data = ''
        while True:
            data += (yield conn.recv(128)).decode('utf-8')
            if data[-1] == '/':
                break
        conn.close()
        logging.debug("Received from Router: " + str(data))

    def listener_proc(host, port, task=None):
        task.set_daemon()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = pycos.AsyncSocket(sock)
        sock.bind((host, port))
        sock.listen(8)

        while True:
            conn, addr = yield sock.accept()
            pycos.Task(BGPServer.listener, conn)

    def run(self):
        logging.debug("BGPServer is waiting for new Router Register Request")
        pycos.Task(BGPServer.listener_proc, '192.168.0.102', 8012)
        while True:
            cmd = sys.stdin.readline().strip().lower()
            if cmd == 'exit' or cmd == 'quit':
                break

if __name__ == '__main__':
    logging.debug('Running by IDE - BGPServer')

    routeListener = BGPServer("16735")
    routeListener.setName('Thread-Domain-16735')

    routeListener.start()
    import RouterCommunication

else:
    logging.debug("Imported in somwehere place - BGPServer")
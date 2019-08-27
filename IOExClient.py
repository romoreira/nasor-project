import socket, sys, pycos, random

def client_proc(host, port, n, task=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = pycos.AsyncSocket(sock)
    yield sock.connect((host, port))
    msg = '%d: ' % n + '-' * random.randint(100,300) + '/'
    msg = msg.encode()
    yield sock.sendall(msg)
    sock.close()

for n in range(1, 10):
    pycos.Task(client_proc, '127.0.0.1', 8010, n)
print("Terminou")

import socket, pycos, yaml, sys

yaml_message = yaml.load("- Teste1" +
                         "- Teste2" +
                         "- Teste3")

######################################-Sender-#######################################
def speaker_proc(host, port, n, task=None):
    #Create a TCP Socket over port 8010 - we may change it further - with pycos we can create more than one socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = pycos.AsyncSocket(sock)
    yield sock.connect((host, port))
    msg = str(yaml_message) + '/'
    msg = msg.encode()
    yield sock.sendall(msg)
    sock.close()


def oib_sender():
    for n in range(1, 2):
        pycos.Task(speaker_proc, '127.0.0.1', 8010, n)
    print("Terminou")

######################################-Sender-#######################################

######################################-Receiver-#######################################
def listenner(conn, task=None):
    data = ''
    while True:
        data += (yield conn.recv(128)).decode('utf-8')
        if data[-1] == '/':
           break
    conn.close()
    print('received: %s' % data)

def listenner_proc(host, port, task=None):
    task.set_daemon()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = pycos.AsyncSocket(sock)
    sock.bind((host, port))
    sock.listen(128)

    while True:
        conn, addr = yield sock.accept()
        pycos.Task(listenner, conn)

def oib_receier():

    pycos.Task(listenner_proc, '127.0.0.1', 8010)
    while True:
        cmd = sys.stdin.readline().strip().lower()
        if cmd == 'exit' or cmd == 'quit':
            break
######################################-Receiver-#######################################

if __name__ == "__main__":
    oib_sender()
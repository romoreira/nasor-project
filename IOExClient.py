import socket, pycos, yaml, sys, logging

# yaml_message = yaml.load("- Teste1" +
#                          "- Teste2" +
#                          "- Teste3")

message = ""

RECEIVED_FROM = []

######################################-Sender-#######################################

def client_recv(sock, task=None):
    while True:
        try:
            msg = yield sock.recv_msg()
        except:
            break
        if not msg:
            break
        print('Resposta:  %s' % msg.decode())
        exit(0)

def client_send(sock, task=None):
    # since readline is synchronous (blocking) call, use async thread;
    # alternately, input can be read in 'main' and sent to this task (with
    # message passing)
    thread_pool = pycos.AsyncThreadPool(1)
    if sys.version_info.major > 2:
        read_input = input
    else:
        read_input = raw_input
    while True:
        try:
            line = yield thread_pool.async_task(read_input)
            line = line.strip()
            if line in ('quit', 'exit'):
                break
            yield sock.send_msg(line.encode())
        except:
            break

def speaker_proc(host, port, n, task=None):
    #Create a TCP Socket over port 8010 - we may change it further - with pycos we can create more than one socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = pycos.AsyncSocket(sock)
    yield sock.connect((host, port))
    msg = str(message) + '/'
    msg = msg.encode()
    yield sock.sendall(msg)
    sock.close()

def nano_exchange(SOURCE, METHOD, MESSAGE, NANO_TARGET_HOST, NANO_TARGET_PORT):
    print("Dentro do PYCOS Client")

    print("Message: "+str(MESSAGE))
    print("NANO HOST: "+str(NANO_TARGET_HOST))
    print("NANO PORT: "+str(NANO_TARGET_PORT))

    global message


    json_message = """{%smethod%s: %s""" + str(METHOD) + """%s, %sdetails%s: """ + MESSAGE + """}"""
    json_message = str(json_message % ("\"", "\"", "\"", "\"", "\"", "\""))

    message = json_message

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((NANO_TARGET_HOST, NANO_TARGET_PORT))
    sock = pycos.AsyncSocket(sock)
    sender = pycos.Task(client_send, sock)
    recvr = pycos.Task(client_recv, sock)
    sender.value()
    recvr.terminate()


    #for n in range(1, 2):
    #        response = pycos.Task(speaker_proc, NANO_TARGET_HSOT, NANO_TARGET_PORT, n)



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

    pycos.Task(listenner_proc, '192.168.0.104', 8011)
    while True:
        cmd = sys.stdin.readline().strip().lower()
        if cmd == 'exit' or cmd == 'quit':
            break
######################################-Receiver-#######################################

if __name__ == "__main__":
    #nano_exchange("SOURCE","NSTD","","192.168.0.105",8011)
    #logging.debug("Runninb by using IDE")

    if __name__ == '__main__':
        # optional arg 1 is host IP address and arg 2 is port to use
        host, port = "192.168.0.105", 8011
        if len(sys.argv) > 1:
            host = sys.argv[1]
        if len(sys.argv) > 2:
            port = int(sys.argv[2])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # in other programs socket is converted to asynchronous and 'connect' is
        # used with 'yield' for async I/O. Here, for illustration, socket is first
        # connected synchronously (since 'yield' can not be used in 'main') and then
        # it is setup for asynchronous I/O
        sock.connect((host, port))
        sock = pycos.AsyncSocket(sock)
        sender = pycos.Task(client_send, sock)
        recvr = pycos.Task(client_recv, sock)
        sender.value()
        recvr.terminate()

else:
    logging.debug('Impomrted in somewhere place - IOExClient')
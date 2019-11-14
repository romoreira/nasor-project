import socket, pycos, json, sys, logging

# yaml_message = yaml.load("- Teste1" +
#                          "- Teste2" +
#                          "- Teste3")

message = ""

RECEIVED_FROM = []

######################################-Sender-#######################################


def speaker_proc(host, port, n, task=None):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = pycos.AsyncSocket(sock)
    yield sock.connect((host, int(port)))
    msg = str(message) + '/'
    msg = msg.encode()
    yield sock.sendall(msg)
    sock.close()

def create_forwarder(METHOD, MESSAGE, ASN):
    print("Ola mundo Create Slice Forwarder")

def next_hop_request(SOURCE, METHOD, MESSAGE, NANO_TARGET_HOST, NANO_TARGET_PORT):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((NANO_TARGET_HOST, NANO_TARGET_PORT))

    json_message = """{%smethod%s: %s""" + str(METHOD) + """%s, %sdetails%s: """ + MESSAGE + """}"""
    json_message = str(json_message % ("\"", "\"", "\"", "\"", "\"", "\""))

    message = json_message

    client.send(message.encode())
    from_server = client.recv(4096)
    print("Client Received: "+str(from_server.decode()))
    client.close()
    return from_server.decode()

def slice_creation_forwarder(SOURCE, METHOD, MESSAGE, NANO_TARGET_HOST, NANO_TARGET_PORT, NEXT_HOP_LIST):
    print("Dentro do PYCOS Client")

    print("SOURCE: "+str(SOURCE))
    print("METHOD: "+str(METHOD))
    print("Message: "+str(MESSAGE))
    print("NANO HOST: "+str(NANO_TARGET_HOST))
    print("NANO PORT: "+str(NANO_TARGET_PORT))
    print("NEXT_HOP_LIST: "+str(NEXT_HOP_LIST))

    global message

    message = json.dumps(MESSAGE)
    NEXT_HOP_LIST = json.dumps(NEXT_HOP_LIST)

    json_message = """{%smethod%s: %s""" + str(METHOD) + """%s, %sdetails%s: """ + str(message) + """, %send2end_next_hop%s: """+str(NEXT_HOP_LIST)+"""}"""
    json_message = str(json_message % ("\"", "\"", "\"", "\"", "\"", "\"", "\"", "\""))

    message = json_message

    print(message)

    for n in range(1, 2):
            response = pycos.Task(speaker_proc, NANO_TARGET_HOST, NANO_TARGET_PORT, n)



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
    rib_request("","GET_PATH","16735","192.168.0.104",8010)

else:
    logging.debug('Impomrted in somewhere place - IOExClient')
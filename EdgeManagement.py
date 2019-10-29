"""
Author: Rodrigo Moreira
Date: 29/10/2019
"""

#Here we need SSH passwordless to reach LXD and Docker containers across edge networks



import paramiko, sys, logging
logging.basicConfig(level=logging.DEBUG)

class EdgeManagement:

    EDGE_MANAGEMENT_IP = ""
    VNFD = ""

    def __init__(self, VNFD):
        self.VNFD = VNFD

    def edge_deployment(self, host, user, password, command):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=password)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)

        logging.debug("Command output: "+str(ssh_stdout.read()))

        ssh.close()

if __name__ == '__main__':
    logging.info('me executou pelo terminal - Edge Management')
    print("Running python 2.7 - Did not work with 3.7")

    edge_management = EdgeManagement("")
    host = str(sys.argv[1])
    user = str(sys.argv[2])
    password = str(sys.argv[3])
    command = str(sys.argv[4])
    edge_management = EdgeManagement("")
    edge_management.edge_deployment(host, user, password, command)
else:
    print("me executou como um modulo - Edge Management")
    host = str(sys.argv[1])
    user = str(sys.argv[2])
    password = str(sys.argv[3])
    command = str(sys.argv[4])
    edge_management = EdgeManagement("")
    edge_management.edge_deployment(host, user, password, command)
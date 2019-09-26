"""
Autor: Rodrigo Moreira
Date: 06/09/2019
"""

#https://opendev.org/x/microstack

import yaml, requests, json, logging, glob, os

#logging.debug('This is a debug message')
#logging.info('This is an info message')
#logging.warning('This is a warning message')
#logging.error('This is an error message')
#logging.critical('This is a critical message')
#logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class MANO:

    NST = ""
    NSD = ""
    OSM_TOKEN_ID = ""



    def __init__(self, NST):
        self.NST = NST

    def read_nsd(self, nsd_dir_name):
        os.chdir(nsd_dir_name)
        nsd_file_name = ""
        for nsd in glob.glob("*.yaml"):
            nsd_file_name = str(nsd)

        nsd_full_path = nsd_dir_name + str("\\") + nsd_file_name

        with open(nsd_full_path, 'r') as stream:
            NSD = yaml.safe_load(stream)
            self.NSD = NSD

            with open('result.yaml', 'w') as yaml_file:
                yaml.dump(self.NSD, yaml_file, default_flow_style=False)

        print(self.NSD)

    def get_tokenid(self, osm_response):
        data = osm_response.text.splitlines()
        id = data[4].split("id: ",1)[1]
        self.OSM_TOKEN_ID = id
        if id == None:
            logging.error('Getting Token ID from OSM')
            return None
        return id

    def osm_connector(self):

        print("Here we will use OSM Rest API to Lauch VNF Instances")
        try:
            osm_host = "10.8.0.1"
            osm_port = "9999"
            url = "https://"+osm_host+":"+osm_port+"/osm/admin/v1/tokens"
            data = {"username": "admin", "password": "admin"}
            headers = {"Content-type": "application/json", "Accept": "text/plain"}
            r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)

            logging.debug('Authentication OSM: '+str(osm_host) + ' status code: '+str(r.status_code))

            if int(r.status_code) != 200 and int(r.status_code) != 201:
                logging.error("OSM Authentication Fail")
                return
        except:
            logging.error("OSM "+osm_host+" Unreacheable")
            return

        """
        Getting Token ID
        """
        print(str(self.get_tokenid(r)))

if __name__ == "__main__":
    mano_worker = MANO()
    #mano_worker.read_nsd_temporary()
    #mano_worker.osm_connector()
    #mano_worker.vnfd_untar()
    #print(str(mano_worker.nsd_untar()))
    mano_worker.read_nsd(r"C:\Users\morei\PycharmProjects\InterOIB\ns\cirros_2vnf_ns")
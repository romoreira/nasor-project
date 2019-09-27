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

    NSD = ""
    VNFD = ""
    OSM_TOKEN_ID = ""



    def __init__(self, NSD, VNFD):
        self.NSD = ""
        self.VNFD = ""

    def post_nsd(self, OSM_IP, REQUEST_ID):
        osm_host = "10.8.0.1"
        osm_port = "9999"
        url = "https://" + osm_host + ":" + osm_port + "/osm/nsd/v1/ns_descriptors_content"
        headers = {"Content-type": "application/gzip", "Accept": "text/plain",
                   'Authorization': 'Bearer {}'.format(self.OSM_TOKEN_ID)}
        try:
            with open('./ns/cirros_2vnf_ns.tar.gz', 'rb') as data:
                r = requests.post(url, data=data, headers=headers, verify=False)
                logging.debug('Posting NSD to OSM: ' + str(osm_host) + ' status code: ' + str(r.status_code))
        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + '\nFailed to Upload NSD to OSM - Connection Timeout:' + str(osm_host))
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + '\nFailed to upload NSD to OSM' + str(osm_host))

        return

    def post_vnfd(self, OSM_IP, REQUEST_ID):
        osm_host = "10.8.0.1"
        osm_port = "9999"
        url = "https://" + osm_host + ":" + osm_port + "/osm/vnfpkgm/v1/vnf_packages_content"
        headers = {"Content-type": "application/gzip", "Accept": "text/plain", 'Authorization': 'Bearer {}'.format(self.OSM_TOKEN_ID)}
        try:
            with open('./ns/cirros_vnf.tar.gz', 'rb') as data:
                r = requests.post(url, data=data, headers=headers, verify=False)
                logging.debug('Posting VNFD to OSM: '+str(osm_host) + ' status code: '+str(r.status_code))
        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + '\nFailed to Upload VNFD to OSM - Connection Timeout:' + str(osm_host))
        except requests.exceptions.RequestException as re:
            logging.error(str(re)+'\nFailed to upload VNFD to OSM'+str(osm_host))

        return

    def get_tokenid(self, osm_response):
        data = osm_response.text.splitlines()
        id = data[4].split("id: ",1)[1]
        self.OSM_TOKEN_ID = id
        if id == None:
            logging.error('Getting Token ID from OSM')
            return None
        return id

    def osm_connector(self):
        logging.debug("OSM_CONNECTOR: Here we will use OSM Rest API to Lauch VNF Instances")
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
            else:
                return str(self.get_tokenid(r))
        except:
            logging.error("OSM "+osm_host+" Unreacheable")
            return

if __name__ == "__main__":
    mano_worker = MANO("","")
    #mano_worker.read_nsd_temporary()
    #mano_worker.osm_connector()
    #mano_worker.vnfd_untar()
    #print(str(mano_worker.nsd_untar()))
    mano_worker.osm_connector()
    mano_worker.post_vnfd("","")
    mano_worker.post_nsd("", "")
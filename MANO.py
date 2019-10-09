"""
Autor: Rodrigo Moreira
Date: 06/09/2019
"""

#https://opendev.org/x/microstack

import yaml, requests, json, logging, glob, os
yaml.warnings({'YAMLLoadWarning': False})

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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

    def get_vim_id(self, VIM_NAME):
        osm_host = "10.8.0.1"
        osm_port = "9999"
        url = "https://" + osm_host + ":" + osm_port + "/osm/admin/v1/vim_accounts"
        headers = {"Content-type": "application/json", "Accept": "text/plain",
                   'Authorization': 'Bearer {}'.format(self.OSM_TOKEN_ID)}
        try:
            r = requests.get(url, headers=headers, verify=False)
            vim_id = yaml.load(r.text)
            if str(vim_id[0]['name']) == VIM_NAME:
                vim_id = vim_id[0]['_id']
            else:
                logging.error('\Failed to retrieve VIM_ID from OSM:' + str(osm_host) + " VIM_NAME: "+str(VIM_NAME))
                return

            logging.debug('Getting VIM_ID: ' + str(vim_id) + ' from OSM:'+str(osm_host)+" status code: " + str(r.status_code))
            return vim_id
        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + '\nFailed to GET VIM_ID from OSM - Connection Timeout:' + str(osm_host))
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + '\nFailed to GET VIM_ID from OSM' + str(osm_host))

        return

    def get_ns_id(self, NS_NAME, REQUEST_ID):

        osm_host = "10.8.0.1"
        osm_port = "9999"
        url = "https://" + osm_host + ":" + osm_port + "/osm/nslcm/v1/ns_instances"
        headers = {"Content-type": "application/json", "Accept": "text/plain",
                   'Authorization': 'Bearer {}'.format(self.OSM_TOKEN_ID)}
        try:

            r = requests.get(url, headers=headers, verify=False)
            ns_id = yaml.load(r.text)

            if str(ns_id[0]['name']) == str(NS_NAME):
                ns_id = str(ns_id[0]['_id'])

            logging.debug('Getting NS_ID: ' + str(osm_host) + ' status code: ' + str(r.status_code))

            return ns_id

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + '\nFailed to GET NS_ID from OSM - Connection Timeout:' + str(osm_host))
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + '\nFailed to GET NS_ID from OSM' + str(osm_host))

        return

    def get_nsd_id(self, NSD_NAME):

        osm_host = "10.8.0.1"
        osm_port = "9999"
        url = "https://" + osm_host + ":" + osm_port + "/osm/nsd/v1/ns_descriptors_content"
        headers = {"Content-type": "application/json", "Accept": "text/plain",
                   'Authorization': 'Bearer {}'.format(self.OSM_TOKEN_ID)}
        try:
            r = requests.get(url, headers=headers, verify=False)
            nsd_id = yaml.load(r.text)

            if str(nsd_id[0]['name']) == str(NSD_NAME):
                nsd_id = str(nsd_id[0]['_id'])

            logging.debug('Getting NSD_ID: ' + str(osm_host) + ' status code: ' + str(r.status_code))

            return nsd_id

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + '\nFailed to GET NSD_ID from OSM - Connection Timeout:' + str(osm_host))
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + '\nFailed to GET NSD_ID from OSM' + str(osm_host))

        return

    """
    Delete NS
    """
    def delete_ns(self, NS_NAME, REQUEST_ID):

        ns_id = self.get_ns_id(NS_NAME, REQUEST_ID)

        osm_host = "10.8.0.1"
        osm_port = "9999"
        url = "https://" + osm_host + ":" + osm_port + "/osm/nslcm/v1/ns_instances_content/"+str(ns_id)
        headers = {"Content-type": "application/yaml", "Accept": "text/plain",
                   'Authorization': 'Bearer {}'.format(self.OSM_TOKEN_ID)}
        try:

            r = requests.delete(url, data="", headers=headers, verify=False)

            terminated_ns_id = yaml.load(r.text)

            if int(r.status_code) >= 400:
                logging.error(' NS Delete Failed - OSM ' + str(osm_host)+" status: "+str(terminated_ns_id['status']))
                return
            elif int(r.status_code) == 200 or int(r.status_code) == 201 or  int(r.status_code) == 202:
                logging.debug('Deleted NS: ' + str(terminated_ns_id['_id']) + ' performed on OSM' + osm_host + ' status code: ' + str(r.status_code))
                return "NS: '"+NS_NAME+"' Deleted! - Request ID: "+REQUEST_ID

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + '\nDelete NS Failed - Connection Timeout:' + str(osm_host))
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + '\nDelete NS Failed' + str(osm_host))

        return


    """
    Terminate NS
    """
    def terminate_ns(self, NS_NAME, REQUEST_ID):

        ns_id = self.get_ns_id(NS_NAME, REQUEST_ID)

        osm_host = "10.8.0.1"
        osm_port = "9999"
        url = "https://" + osm_host + ":" + osm_port + "/osm/nslcm/v1/ns_instances/"+str(ns_id)+"/terminate"
        headers = {"Content-type": "application/yaml", "Accept": "text/plain",
                   'Authorization': 'Bearer {}'.format(self.OSM_TOKEN_ID)}
        try:

            r = requests.post(url, data="", headers=headers, verify=False)
            terminated_ns_id = yaml.load(r.text)

            if int(r.status_code) >= 400:
                logging.error(' NS Terminate Failed - OSM ' + str(osm_host)+" status: "+str(terminated_ns_id['status']))
                return
            elif int(r.status_code) == 200 or int(r.status_code) == 201:
                logging.debug('Terminate NS: ' + str(terminated_ns_id['id']) + ' performed on OSM' + osm_host + ' status code: ' + str(r.status_code))
                return terminated_ns_id['id']

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + '\nTerminate NS Failed - Connection Timeout:' + str(osm_host))
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + '\nTerminate NS Failed' + str(osm_host))

        return


    """
    Create and Instantiate NS
    """
    def create_instantiate_ns(self, NS_NAME, NSD_NAME, REQUEST_ID):
        nsd_id = self.get_nsd_id(NSD_NAME)
        vim_id = self.get_vim_id("VIM-Name")

        data = """
                nsName: %s            # mandatory
                nsdId: %s  # mandatory
                vimAccountId: %s   # mandatory
                wimAccountId: %s
                additionalParamsForNs:  {}
                additionalParamsForVnf: []
                ssh_keys: []
                vnf: [ {member-vnf-index: "1", vimAccountId: vim-uuid, internal-vld: [], vdu: [] } ]
                vld: [ {name: vld-name, ip-profile: {}, vnfd-connection-point-ref: [{}] }]
                """

        data = str(data%(NS_NAME, nsd_id, vim_id, "False"))

        osm_host = "10.8.0.1"
        osm_port = "9999"
        url = "https://" + osm_host + ":" + osm_port + "/osm/nslcm/v1/ns_instances_content"
        headers = {"Content-type": "application/yaml", "Accept": "text/plain",
                   'Authorization': 'Bearer {}'.format(self.OSM_TOKEN_ID)}
        try:

            r = requests.post(url, data=data, headers=headers, verify=False)

            create_instantiate_code = yaml.load(r.text)

            if int(create_instantiate_code['status']) >= 400:
                logging.error(' NS Create and Instantiate Failed - OSM ' + str(osm_host)+" code error: "+str(create_instantiate_code['status']))
                return
            elif create_instantiate_code['status'] == 200:
                logging.debug('NS Created on OSM' +osm_host+' status code: ' + str((create_instantiate_code['status'])))
                return

            created_ns_id = yaml.load(r.text)
            created_ns_id = created_ns_id['id']

            logging.debug('Create and Instantiate NS: ' + str(created_ns_id) + ' performed on OSM' + osm_host + ' status code: ' + str(r.status_code))

            return created_ns_id

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + '\nNS Create and Instantiate Failed - Connection Timeout:' + str(osm_host))
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + '\nNS Create and Instantiate Failed' + str(osm_host))

        return

    """
    Create a NS but not instantiate
    """
    def crete_ns(self, NS_NAME, NSD_NAME, REQUEST_ID):

        nsd_id = self.get_nsd_id(NSD_NAME)
        vim_id = self.get_vim_id("VIM-Name")

        data = """
                nsName: %s            # mandatory
                nsdId: %s  # mandatory
                vimAccountId: %s  # mandatory
                wimAccountId: %s
                additionalParamsForNs:  {}
                additionalParamsForVnf: []"""

        data = str(data%(NS_NAME, nsd_id, vim_id, "False"))

        osm_host = "10.8.0.1"
        osm_port = "9999"
        url = "https://" + osm_host + ":" + osm_port + "/osm/nslcm/v1/ns_instances"
        headers = {"Content-type": "application/yaml", "Accept": "text/plain",
                   'Authorization': 'Bearer {}'.format(self.OSM_TOKEN_ID)}
        try:

            r = requests.post(url, data=data, headers=headers, verify=False)
            created_ns_id = yaml.load(r.text)

            logging.debug('NS: ' + str(created_ns_id) + ' Created on OSM' +osm_host+', but not instantiated - status code: ' + str(r.status_code))

            return created_ns_id['id']

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + '\nNS Create Failed - Connection Timeout:' + str(osm_host))
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + '\nNS Create Failed' + str(osm_host))

        return

    def instantiate_ns(self, NS_ID, REQUEST_ID):

        vim_id = self.get_vim_id("VIM-Name")

        data = """
                vimAccountId: %s   # mandatory
                wimAccountId: %s
                ssh_keys: []
                vnf: [ {member-vnf-index: "1", vimAccountId: vim-uuid, internal-vld: [], vdu: [] } ]
                vld: [ {name: vld-name, ip-profile: {}, vnfd-connection-point-ref: [{}] }]"""

        data = str(data%(vim_id, "False"))

        osm_host = "10.8.0.1"
        osm_port = "9999"
        url = "https://" + osm_host + ":" + osm_port + "/osm/nslcm/v1/ns_instances/"+str(NS_ID)+"/instantiate"
        headers = {"Content-type": "application/yaml", "Accept": "text/plain",
                   'Authorization': 'Bearer {}'.format(self.OSM_TOKEN_ID)}
        try:

            r = requests.post(url, data=data, headers=headers, verify=False)
            instantiate_ns_response = yaml.load(r.text)

            if int(instantiate_ns_response['status']) >= 400:
                logging.error(' NS Instantiate Failed - OSM ' + str(osm_host)+" code error: "+str(instantiate_ns_response['status']))
                return
            elif int(instantiate_ns_response['status']) == 200:
                logging.debug('NS Instantiate on OSM' +osm_host+' status code: ' + str((instantiate_ns_response['status'])))
                return

            created_ns_id = yaml.load(r.text)
            created_ns_id = created_ns_id['id']

            logging.debug('NS: ' + str(created_ns_id) + ' Instantiated on OSM' +osm_host+' status code: ' + str(r.status_code))

            return created_ns_id

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + '\nNS Instantiate Failed - Connection Timeout:' + str(osm_host))
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + '\nNS Instantiate Failed' + str(osm_host))

        return


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
    #mano_worker.post_vnfd("","")
    #mano_worker.post_nsd("", "")
    #mano_worker.ns_get_id("cirros_2vnf_ns")
    #mano_worker.vim_get_id("")
    #ns_id = mano_worker.crete_ns("Network Service Test","cirros_2vnf_ns","")
    #mano_worker.instantiate_ns(ns_id,"")
    #mano_worker.create_instantiate_ns("teste","cirros_2vnf_ns","")
    #mano_worker.get_ns_id("teste","")
    #print(mano_worker.terminate_ns("teste",""))
    #print(mano_worker.delete_ns("teste",""))
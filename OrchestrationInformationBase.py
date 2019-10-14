"""
Author: Rodrigo Moreira
Date: 14/10/2019
"""
import requests, logging, json


class OrchestrationInformationBase:

    def get_region_servers(self, region):
        geode_host = "10.8.0.1"
        geode_port = "8080"
        url = "http://" + geode_host + ":" + geode_port + "/geode/v1/servers"
        headers = {"Content-Type": "application/json", "accept": "application/json"}
        try:

            r = requests.get(url, headers=headers, verify=False)

            if r.status_code != 200:
                logging.error("ApagheGeode - Any data were found in given region: "+str(region))
            else:
                data = r.text

            print(data)

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + "Getting region data Definir")
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + "Getting region data Definir")

        return

    def get_region_keys(self, region):
        geode_host = "10.8.0.1"
        geode_port = "8080"
        url = "http://" + geode_host + ":" + geode_port + "/geode/v1/"+str(region)+"/keys"
        headers = {"Content-Type": "application/json", "accept": "application/json"}
        try:

            r = requests.get(url, headers=headers, verify=False)

            if r.status_code != 200:
                logging.error("ApagheGeode - Any data were found in given region: "+str(region))
            else:
                data = r.text

            print(data)

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + "Getting region data Definir")
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + "Getting region data Definir")

        return

    def get_data_from_region(self, region):

        geode_host = "10.8.0.1"
        geode_port = "8080"
        url = "http://" + geode_host + ":" + geode_port + "/geode/v1/"+str(region)
        headers = {"Content-Type": "application/json", "accept": "application/json"}
        try:

            r = requests.get(url, headers=headers, verify=False)

            if r.status_code != 200:
                logging.error("ApagheGeode - Any data were found in given region: "+str(region))
            else:
                data = r.text

            print(data)

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + "Getting region data Definir")
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + "Getting region data Definir")

        return

    def initialize_oib_geode(self, region, key):

        data = """[string: %s]"""

        data = str(data%("teste"))

        data = json.dumps(data)

        geode_host = "10.8.0.1"
        geode_port = "8080"
        url = "http://" + geode_host + ":" + geode_port + "/geode/v1/"+str(region)+"/"+str(key)+"?op=PUT"

        headers = {"Content-Type": "application/json", "accept": "application/json"}
        try:

            r = requests.put(url, data=data, headers=headers, verify=False)

            print(str(r.text))

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + "Definir")
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + "Definir")

        return

if __name__ == "__main__":
    oib = OrchestrationInformationBase()
    oib.initialize_oib_geode("regionA",1)
    #oib.get_data_from_region("regionA")
    #oib.get_region_keys("regionA")
    #oib.get_region_servers("")

"""
Author: Rodrigo Moreira
Date: 15/10/2019
"""

import json, os, logging, requests, time
import pandas as pd

class iDomainInformationBase:

    def geode_syncronization(self):

        csv_file = pd.DataFrame(pd.read_csv("./data/idomain_information_base.csv", sep=",", header=0, index_col=False))
        csv_file.to_json("idib-file.json", orient="records", date_format="epoch", double_precision=10,
                         force_ascii=True, date_unit="ms", default_handler=None)

        with open('idib-file.json') as f:
            data = json.load(f)

        try:
            os.remove('idib-file.json')
        except:
            logging.error("Apache Geode - iDomainInformationBase - CSV to JSON Parsing Error - Deleting temporary file error")
            return None

        if data == "" or data == None:
            logging.info("Apache Geode - iDomainInformationBase - CSV to JSON parsing error - JSON file is empty")
            return

        return data

    def insert_datakey_into_region(self, region, key):

        data = self.geode_syncronization()
        if data == "" or data == None:
            logging.error("Apache Geode - iDomainInformationBase - Error to Insert data to Repository - Data Empty")
            return

        geode_host = "10.9.0.1"
        geode_port = "8080"
        url = "http://" + geode_host + ":" + geode_port + "/geode/v1/"+str(region)+"/"+str(key)+"?op=PUT"

        headers = {"Content-Type": "application/json", "accept": "application/json"}
        try:

            r = requests.put(url, data=json.dumps(data), headers=headers, verify=False)


            if r.status_code != 200 and r.status_code != 201:
                logging.error("Apache Geode - iDomainInformationBase - Inserting data on Repository Error - JSON")
            else:
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                print(str("Data Updated on Apache Geode - iDomainInformationBase"))
                logging.info("Data Inserted on Apache Geode - iDomainInformationBase - IP: "+str(geode_host) + " Data: "+current_time)

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + "Apache Geode - iDomainInformationBase - Inserting data on Repository - Timeout")
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + "Apache Geode - iDomainInformationBase - Inserting data on Repository - Request Error")

        return

    def get_data_from_region(self, region):

        geode_host = "10.9.0.1"
        geode_port = "8080"
        url = "http://" + geode_host + ":" + geode_port + "/geode/v1/"+str(region)
        headers = {"Content-Type": "application/json", "accept": "application/json"}
        try:

            r = requests.get(url, headers=headers, verify=False)

            if r.status_code != 200:
                logging.error("ApagheGeode - iDomainInformationBase - Any data were found in given region: "+str(region))
            else:
                data = r.text

            print(data)

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + "Getting Region Data - iDomainInformationBase")
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + "Getting Region Data - iDomainInformationBase")

        return data


    def get_region_keys(self, region):
        geode_host = "10.9.0.1"
        geode_port = "8080"
        url = "http://" + geode_host + ":" + geode_port + "/geode/v1/"+str(region)+"/keys"
        headers = {"Content-Type": "application/json", "accept": "application/json"}
        try:

            r = requests.get(url, headers=headers, verify=False)

            if r.status_code != 200:
                logging.error("ApagheGeode - iDomainInformationBase - Any data were found in given region: "+str(region))
            else:
                data = r.text

            print(data)

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + "Getting Region Keys - iDomainInformationBase")
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + "Getting region Keys - iDomainInformationBase -")

        return


    def get_region_servers(self, region):

        geode_host = "10.9.0.1"
        geode_port = "8080"
        url = "http://" + geode_host + ":" + geode_port + "/geode/v1/servers"
        headers = {"Content-Type": "application/json", "accept": "application/json"}
        try:

            r = requests.get(url, headers=headers, verify=False)

            if r.status_code != 200:
                logging.error("ApagheGeode - iDomainInformationBase - Any data were found in given region: "+str(region))
            else:
                data = r.text

            print(data)

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + "Getting Region Servers - iDomainInformationBase -")
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + "Getting Region Servers - - iDomainInformationBase -")

        return

    def delete_data_from_region(self, region, key):
        geode_host = "10.9.0.1"
        geode_port = "8080"
        url = "http://" + geode_host + ":" + geode_port + "/geode/v1/"+str(region)+"/"+str(key)
        headers = {"Content-Type": "application/json", "accept": "application/json"}
        try:

            r = requests.delete(url, headers=headers, verify=False)

            if r.status_code != 200:
                logging.error("ApagheGeode - iDomainInformationBase - Any data were found in given region: "+str(region))
                return
            else:
                data = r.text

            print(data)

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + "Deleting Region Data - iDomainInformationBase -")
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + "Deleting Region Data - iDomainInformationBase -")

        return

if __name__ == "__main__":
    ioib = iOrchestrationInformationBase()
    #ioib.geode_syncronization()
    ioib.insert_datakey_into_region("regionA", 1)
"""
Author: Rodrigo Moreira
Date: 14/10/2019
"""
import requests, logging, json, time, os
import pandas as pd


class eDomainInformationBase:

    def delete_data_from_region(self, region, key):
        geode_host = "10.8.0.1"
        geode_port = "8080"
        url = "http://" + geode_host + ":" + geode_port + "/geode/v1/"+str(region)+"/"+str(key)
        headers = {"Content-Type": "application/json", "accept": "application/json"}
        try:

            r = requests.delete(url, headers=headers, verify=False)

            if r.status_code != 200:
                logging.error("ApagheGeode - Any data were found in given region: "+str(region))
                return
            else:
                data = r.text

            print(data)

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + "Deleting region data Definir")
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + "Deleting region data Definir")

        return


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

            #print(data)

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + "Getting region data Definir")
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + "Getting region data Definir")

        return data

    def geode_syncronization(self):

        csv_file = pd.DataFrame(pd.read_csv("./data/edomain_information_base.csv", sep=",", header=0, index_col=False))
        csv_file.to_json("edib-file.json", orient="records", date_format="epoch", double_precision=10,
                         force_ascii=True, date_unit="ms", default_handler=None)


        with open('edib-file.json') as f:
            data = json.load(f)

        try:
            os.remove('edib-file.json')
        except:
            logging.error("Apache Geode - CSV to JSON Parsing Error - Deleting temporary file error")
            return None

        if data == "" or data == None:
            logging.info("Apache Geode - CSV to JSON parsing error - JSON file is empty")
            return

        return data

    def insert_datakey_into_region(self, region, key):
        data = self.geode_syncronization()
        if data == "" or data == None:
            logging.error("Apache Geode - Error to Insert data to Repository - Data Empty")
            return

        geode_host = "10.8.0.1"
        geode_port = "8080"
        url = "http://" + geode_host + ":" + geode_port + "/geode/v1/"+str(region)+"/"+str(key)+"?op=PUT"

        headers = {"Content-Type": "application/json", "accept": "application/json"}
        try:

            r = requests.put(url, data=json.dumps(data), headers=headers, verify=False)


            if r.status_code != 200 and r.status_code != 201:
                logging.error("Apache Geode - Inserting data on Repository Error - JSON")
            else:
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                print(str("Data Updated on Apache Geode"))
                logging.info("Data Inserted on Apache Geode. IP: "+str(geode_host) + " Data: "+current_time)

        except requests.exceptions.Timeout as ct:
            logging.error(str(ct) + "Apache Geode - Inserting data on Repository - Timeout")
        except requests.exceptions.RequestException as re:
            logging.error(str(re) + "Apache Geode - Inserting data on Repository - Request Error")

        return

if __name__ == "__main__":
    eoib = eDomainInformationBase()
    #oib.geode_syncronization()
    eoib.insert_datakey_into_region("regionA",1)
    #oib.get_data_from_region("regionA")
    #oib.get_region_keys("regionA")
    #oib.get_region_servers("")
    #oib.delete_data_from_region("regionA", 1)

if __name__ == '__main__':
    logging.debug('Running by IDE - eDomainInformationBase')
    eoib = eDomainInformationBase()
    #oib.geode_syncronization()
    eoib.insert_datakey_into_region("regionA",1)
    #oib.get_data_from_region("regionA")
    #oib.get_region_keys("regionA")
    #oib.get_region_servers("")
    #oib.delete_data_from_region("regionA", 1)

else:
    logging.debug('Imported in somewhere place - eDomainInformationBase')

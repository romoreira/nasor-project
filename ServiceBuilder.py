'''
Author: Rodrigo Moreira
Date: 06/09/2019
'''


#https://osm-download.etsi.org/ftp/osm-6.0-six/7th-hackfest/presentations/
# Each Service Builder in each Domain is able to receive NST to proced with Service Deployment

import requests, json, logging, glob, os
import yaml
import NANO
import MANO




class ServiceBuilder:
    NSD = None
    VNFD = None
    NSTD = None

    """
    Receives a tar.gz NSD and returns a directory name of extracted files
    """
    def nsd_untar(self):
        dir = os.path.dirname("./ns/cirros_2vnf_ns.tar.gz")  # get directory where file is stored
        dir_extract = os.path.dirname("./ns/")
        filename = os.path.basename("./ns/cirros_2vnf_ns.tar.gz")  # get filename
        file_tar, file_tar_ext = os.path.splitext("./ns/cirros_2vnf_ns.tar.gz")  # split into file.tar and .gz
        file_untar, file_untar_ext = os.path.splitext(file_tar)  # split into file and .tar
        os.chdir(dir)
        if file_tar_ext == ".gz" and file_untar_ext == ".tar":  # check if file had format .tar.gz
            import tarfile
            tar = tarfile.open(filename)
            tar.extractall(path=dir_extract)  # untar file into same directory
            tar.close()
            os.chdir(
                file_untar)  # This fails if file.tar.gz has different name compared to the untarred folder e.g.. file1 instead of file

            logging.debug("Uncompressed NSD " + str(filename) + " on " + str(file_untar))

            # Dir name of extracted files
            return file_untar

    """
    Receives a tar.gz VNFD and returns a directory name of extracted files
    """
    def vnfd_untar(self):
        dir = os.path.dirname("./ns/cirros_vnf.tar.gz")  # get directory where file is stored
        dir_extract = os.path.dirname("./ns/")
        filename = os.path.basename("./ns/cirros_vnf.tar.gz")  # get filename
        file_tar, file_tar_ext = os.path.splitext("./ns/cirros_vnf.tar.gz")  # split into file.tar and .gz
        file_untar, file_untar_ext = os.path.splitext(file_tar)  # split into file and .tar
        os.chdir(dir)
        if file_tar_ext == ".gz" and file_untar_ext == ".tar":  # check if file had format .tar.gz
            import tarfile
            tar = tarfile.open(filename)
            tar.extractall(path=dir_extract)  # untar file into same directory
            tar.close()
            os.chdir(file_untar)  # This fails if file.tar.gz has different name compared to the untarred folder e.g.. file1 instead of file

            logging.debug("Uncompressed VNFD " + str(filename) + " on " + str(file_untar))

            # Dir name of extracted files
            return file_untar

    """
    Search for yaml in extracted directory
    """
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


    def read_nstd(self):
        with open("./ns/cirros_nstd.yaml", 'r') as stream:
            NSTD = yaml.safe_load(stream)

        self.NSTD = NSTD['nst']


    def read_nsd(self):
        with open("./ns/cirros_2vnf_ns/cirros_2vnf_nsd.yaml", 'r') as stream:
            NSD = yaml.safe_load(stream)

        self.VNFD = NSD['nsd:nsd-catalog']

    def network_slice_template(self):
        nano = NANO.NANO(1,self.NSTD,16735)
        nano.eDomain_slice_builder()

    def virtual_network_function_description(self):
        mano = MANO.MANO(self.VNFD)
        mano.vnfd_yaml_interpreter()


if __name__ == "__main__":
    sb = ServiceBuilder()
    #sb.read_nsd()

    """
    Splitting YAML service descriptor to OSM and NANO to provide Network Slice Builder
    """

    sb.read_nstd()
    sb.network_slice_template()


    #sb.virtual_network_function_description()
    #sb.vnfd_untar()
    #sb.nsd_untar()

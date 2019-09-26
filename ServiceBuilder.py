'''
Author: Rodrigo Moreira
Date: 06/09/2019
'''

# Each Service Builder in each Domain is able to receive NST to proced with Service Deployment

import requests, json, logging, glob, os
import yaml
import NANO
import MANO


class ServiceBuilder:
    NSD = None
    VNFD = None

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

    def read_nsd(self):
        with open("./ns/cirros_2vnf_ns/cirros_2vnf_nsd.yaml", 'r') as stream:
            NSD = yaml.safe_load(stream)

        self.NSD = NSD['nstd:nstd-details']
        self.VNFD = NSD['nsd:nsd-catalog']

    def network_slice_template(self):
        nmano = NANO.NANO(self.NSD)
        nmano.nst_yaml_interpreter()

    def virtual_network_function_description(self):
        print(self.VNFD)
        return
        mano = MANO.MANO(self.VNFD)
        mano.vnfd_yaml_interpreter()


if __name__ == "__main__":
    sb = ServiceBuilder()
    #sb.read_nsd()

    """
    Splitting YAML service descriptor to OSM and NANO to provide Network Slice Builder
    """
    #sb.network_slice_template()
    #sb.virtual_network_function_description()
    #sb.vnfd_untar()
    sb.nsd_untar()

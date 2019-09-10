"""
Author: Rodrigo Moreira
Date: 10/09/2019
"""

import CoreTopology

class NANO:
    NST = None

    def __init__(self, NST):
        self.NST = NST

    def nst_yaml_interpreter(self):
        print("Here we will use NANO to launch Slice Instance")

        ct = CoreTopology.CoreTopology()
        ct.neighborhood_check(str(self.NST['asn-involved']))
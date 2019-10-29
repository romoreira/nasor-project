"""
Author: Rodrigo Moreira
Date: 29/10/2019
"""

import pyone

one = pyone.OneServer("http://one:2633/RPC2", session="oneadmin:onepass")

vm_template = one.templatepool.info(-1, -1, -1).VMTEMPLATE[0]
print(vm_template.get_ID())
vm_template_id = int(vm_template.get_ID())
vm_template.get_NAME()

one.template.instantiate(vm_template_id, "my_VM")
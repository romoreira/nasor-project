import ipaddress

print("Ola mundo")

print([ipaddr for ipaddr in ipaddress.summarize_address_range(ipaddress.IPv6Address('1::'), ipaddress.IPv6Address('2000::'))])

print([ipaddr for ipaddr in ipaddress.summarize_address_range(ipaddress.IPv4Address('192.0.2.0'), ipaddress.IPv4Address('192.0.2.130'))])

print(ipaddress.ip_network("1::/16").hosts())

print("\n".join([str(x) for x in ipaddress.ip_network("1::/128").hosts()]))

save = 0

import random
M = 16**4
for i in range(100000):
   print("2000:" + ":".join(("%x" % random.randint(0, M) for i in range(7))))
   save = i + 1

print("Resultado: "+str(save))


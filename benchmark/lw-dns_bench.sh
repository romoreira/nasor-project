#!/bin/bash
while true; do dig www.google.com | grep time; sleep 1; done

#sudo apt-get install namebench - maybe i can use that
#http://www.damagehead.com/blog/2015/04/28/deploying-a-dns-server-using-docker/
#https://blog.webernetz.net/benchmarking-dns-namebench-dnseval/
#github.com/sameersbn/docker-bind
#https://github.com/mastermindg/rpi-dns

#Linux Commands:

# 1981  sudo apt-get install namebench
# 1982  1
# 1983  namebench --no_gui --input=alexa --query_count=2000 --only 8.8.8.8 10.0.0.10
# 1984  mv /tmp/namebench_2019-11-22_1049.csv /home/rodrigo/Documents/SRv6-Traces/lw-dns-1.csv
# 1985  namebench --no_gui --input=alexa --query_count=2000 --only 8.8.8.8 10.0.0.10 208.67.222.222
# 1986  mv /tmp/namebench_2019-11-22_1112.csv /home/rodrigo/Documents//lw-dns-2.csv
# 1987  namebench --no_gui --input=alexa --query_count=2000 --only 8.8.8.8 10.0.0.10 208.67.220.220
# 1988  mv /tmp/namebench_2019-11-22_1138.csv /home/rodrigo/Documents/lw-dns-3.csv
# 1989  namebench --no_gui --input=alexa --query_count=2000 --only 10.0.0.10 208.67.220.220
# 1990  mv /tmp/namebench_2019-11-22_1211.csv /home/rodrigo/Documents/SRv6-Traces/lw-dns-4.csv
# 1991  namebench --no_gui --input=alexa --query_count=2000 --only 8.8.8.8 10.0.0.10 208.67.220.220 8.8.8.8
# 1992  mv /tmp/namebench_2019-11-22_1244.csv /home/rodrigo/Documents/SRv6-Traces/lw-dns-5.csv
# 1993  namebench --no_gui --input=alexa --query_count=2000 --only 8.8.8.8 10.0.0.10 208.67.222.222 8.8.8.8
# 1994  mv /tmp/namebench_2019-11-22_1303.csv /home/rodrigo/Documents/SRv6-Traces/lw-dns-6.csv
# 1995  namebench --no_gui --input=cachehit --query_count=2000 --only 8.8.8.8 10.0.0.10 208.67.222.222
# 1996  mv /tmp/namebench_2019-11-22_1306.csv /home/rodrigo/Documents/SRv6-Traces/lw-dns-7.csv
# 1997  namebench --no_gui --input=cachemiss --query_count=2000 --only 8.8.8.8 10.0.0.10 208.67.222.222
# 1998  mv /tmp/namebench_2019-11-22_1316.csv /home/rodrigo/Documents/SRv6-Traces/lw-dns-8.csv

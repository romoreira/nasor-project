#!/bin/bash
while true; do dig www.google.com | grep time; sleep 1; done

#sudo apt-get install namebench - maybe i can use that
#http://www.damagehead.com/blog/2015/04/28/deploying-a-dns-server-using-docker/
#https://blog.webernetz.net/benchmarking-dns-namebench-dnseval/
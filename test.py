#! /usr/bin/python3

import nmap

nma = nmap.PortScanner()
def callback_result(host, scan_result):
	print('------------------')
	print(host, scan_result)

nma.scan(hosts='192.168.2.0/24', arguments='-T5 -Pn -PA -PS')

print(nma.all_hosts())

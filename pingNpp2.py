#! /usr/bin/python3

import ipaddress
import nmap
from pyfiglet import Figlet
import sys

bannertext2 = Figlet(font='epic')
print(bannertext2.renderText('PINGING'))
print("By: Joshua Smith (aka: killbit -- https://twitter.com/Josh2all)\n\n")


if len(sys.argv)==1:
    print('USAGE: ./sweepNverify.py [TARGET_RANGE_LIST_FILE_NAME]\n\n\n')

converted_list_of_ranges=[]
listOfUpHosts=[]
unalteredRanges=[]
converted_list_of_uphosts=[]

def convertUpHostsList(uphosts):
    for line in uphosts:
        converted_list_of_uphosts.append(ipaddress.ip_address(line.rstrip("\n")))

def nmap_port_ping(ip_ranges):
    nm = nmap.PortScanner()
    count = len(ip_ranges)
    while count > 0:
        nm.scan(hosts=ip_ranges[count-1], arguments='-T5 -sP -PE -PA --top-ports 100')
        print('PINGED\t-->\t', ip_ranges[count-1], '-->\t\tReachable Endpoints:\t',len(nm.all_hosts()))
        outfile = open('josh-done-did-yo-pingz.log', 'a+')
        outfile.write("Successfully ICMP Pinged Hosts in %s:\n%s\nSuccessfully Port-Pinged:\n%s\n" % (ip_ranges[count-1],nm.all_hosts(),nm.csv()))
        count = count-1
        host_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        for eachHost, eachState in host_list:
            if eachState == 'up':
                up_hosts.append(eachHost)
    outfile.close()
    return host_list

def convertRangeListFile():
    f = open(sys.argv[1], 'r')
    for line in f:
        unalteredRanges.append(line.rstrip("\n"))
        converted_list_of_ranges.append(ipaddress.ip_network(line.rstrip("\n")))
    f.close()

# Fills list named 'converted_list_of_ranges'
convertRangeListFile()

up_hosts=[]


#Scan all given ranges from input file
host_list= nmap_port_ping(unalteredRanges)

'''
for each_range in unalteredRanges:
    print("PORT-PINGING Range -->\t", each_range)
    host_list = nmap_port_ping(each_range)
    for eachHost,eachState in host_list:
        if eachState == 'up':
            up_hosts.append(eachHost)
'''
#Convert UpHosts to ipaddress format for comparisons
convertUpHostsList(up_hosts)


masterListYes=[]
masterListNo=[]
for eachRange in converted_list_of_ranges:
    for eachHost in converted_list_of_uphosts:
        if eachHost in eachRange.hosts():
            masterListYes.append(eachRange)
        else:
            masterListNo.append(eachRange)

print("\n[---The following ranges contained NO reachable hosts---]\n" )
for eachNo in set(masterListNo):
    print(eachNo)

print("\n[---The following ranges contained SUCCESSFULLY reached hosts---]\n")
for eachYes in set(masterListYes):
    print(eachYes, "\n\n")

print("Detailed Log File Generated >> josh-done-did-yo-pingz.log")
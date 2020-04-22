#! /usr/bin/python3 

import ipaddress
import sys
import subprocess
import nmap
from pyfiglet import Figlet
from tabulate import tabulate
import pandas as pd

bannertext2 = Figlet(font='epic')
print(bannertext2.renderText('PINGING'))
print("By: Joshua Smith (aka: killbit -- https://twitter.com/Josh2all)\n\n")


if len(sys.argv)==1:
    print('USAGE: ./sweepNverify.py [TARGET_RANGE_LIST_FILE_NAME]\n\n\n')

final_dict={'127.0.0.1':{'PINGABLE':'','STATE':'','PORTS':[]}}
full_probe_dict={}
ping_response={}
converted_list_of_ranges=[]
listOfUpHosts=[]
unalteredRanges=[]
converted_list_of_uphosts=[]

def convertUpHostsList(uphosts):
    for line in uphosts:
        converted_list_of_uphosts.append(ipaddress.ip_address(line.rstrip("\n")))

def pingsweep(ip_range):
    scan = subprocess.run(['/usr/bin/fping','-a','-s','-q','-g',ip_range],text=True,capture_output=True)
    stats = scan.stderr
    statList=stats.split()
    shortStatList=statList[0:6]
    subShortList1=shortStatList[::2]
    subShortList2=shortStatList[1::2]
    correctStats=dict(zip(subShortList2, subShortList1))
    print("PingSweeping --> ",ip_range,' ---->\t[','SCANNED:', correctStats['targets'],'\tALIVE:',correctStats['alive'],'\tUnreachable:',correctStats['unreachable'],']')
    s = scan.stdout
    uphosts=''.join(s).split()
    for eachResponse in uphosts:
        ping_response[eachResponse] = 'up'
    return(uphosts)


def nmap_port_ping(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-T5 -Pn -PS -PA --top-ports 100')
    for host in nm.all_hosts():
        if 'tcp' in nm[host].all_protocols():
            full_probe_dict[host] = nm[host]
    return

def convertRangeListFile():
    f = open(sys.argv[1], 'r')
    for line in f:
        if line == '' or line == ' ':
            skip
        else:
            unalteredRanges.append(line.rstrip("\n"))
            converted_list_of_ranges.append(ipaddress.ip_network(line.rstrip("\n")))
    f.close()

    

def nmap_port_ping(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-T5 -Pn -PS -PA --top-ports 100')
    for host in nm.all_hosts():
        if 'tcp' in nm[host].all_protocols():
            full_probe_dict[host] = nm[host]
    return 

convertRangeListFile()
up_hosts = []
for each_range in unalteredRanges:
    nmap_port_ping(each_range)
    pp = pingsweep(each_range)
    for each in pp:
         up_hosts.append(each)

         
convertUpHostsList(up_hosts)


masterListYes=[]
masterListNo=[]
for eachRange in converted_list_of_ranges:
    for eachHost in converted_list_of_uphosts:
        if eachHost in eachRange.hosts():
            masterListYes.append(eachRange)
        else:
            masterListNo.append(eachRange)


dedup_masterListYes=[]
dedup_masterListNo=[]
for i in masterListYes:
    if i not in dedup_masterListYes:
        dedup_masterListYes.append(i)


for x in masterListNo:
    if x not in dedup_masterListNo:
        dedup_masterListNo.append(x)


print("\n[---The following ranges contained NO reachable hosts---]\n" )
for eachNo in dedup_masterListNo:
    print(eachNo)

print("\n[---The following ranges contained SUCCESSFULLY reached hosts---]\n")
for eachYes in dedup_masterListYes:
    print(eachYes, "\n\n")


outfile = open('josh-done-did-yo-pingsweep.out','w+')
for each in up_hosts:
    it = each.rstrip('\n')
    outfile.write("%s\n" % it)

outfile.close()
print("OUTFILE: josh-done-did-yo-pingsweep.out")

print(full_probe_dict)

print("---Port Pings (ACK, and SYN) initalizing---")
for k,v in ping_response.items():
    if ( k not in full_probe_dict.keys()) and (v == 'up'):
        print("Uphost: ",k,"\tFping Response: YES\tNmap Response: NO")
    elif ('tcp' in full_probe_dict[k].keys()) and (v == 'up'):
        print("Uphost: ",k,"\tFping Response: YES\tNmap Response: YES", "\tListening on: ", list(full_probe_dict[k]['tcp'].keys()))
    elif ('tcp' in full_probe_dict[k].keys()) and (v != 'up'):
        print("Uphost: ",k,"\tFping Response: NO\tNmap Response: YES", "\tListening on: ", list(full_probe_dict[k]['tcp'].keys()))
    else:
        print("FPING: NO RESPONSE \tNMAP: NO RESPONSE")
  
#Building FINAL DICTIONARY
# somedict[key is IP Address]={PINGABLE:'yes/no',STATE:'up','PORTS_PINGABLE':[LIST OF OPEN PORTS]}

#Iterate over dict1 then iterate over dict2 to make sure all keys are accounted 
for k,v in  ping_response.items():
    if k not in final_dict.keys():
        final_dict[k] = {'PINGABLE':'yes', 'STATE':'up'}

for k,v in full_probe_dict.items():
    if k not in final_dict.keys():
        final_dict[k] = {'PINGABLE':'no','STATE':'up','PORTS':full_probe_dict[k]['tcp'].keys()}
    elif k in final_dict.keys():
        final_dict[k] = {'PINGABLE':'yes','STATE':'up','PORTS':full_probe_dict[k]['tcp'].keys()}


df = pd.DataFrame(final_dict.values(),index=final_dict.keys())
print(tabulate(df.sort_index(),headers='keys',tablefmt="grid"))
'''
# TO DO LIST
1. Need to confirm each reached RANGE from nmap scan results
'''

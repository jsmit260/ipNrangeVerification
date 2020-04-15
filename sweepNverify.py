#! /usr/bin/python3 
import ipaddress
import sys
import subprocess
from pyfiglet import Figlet

bannertext = Figlet(font='banner')
print(bannertext.renderText('Pow Pow'))

bannertext2 = Figlet(font='epic')
print(bannertext2.renderText('Bang Boogi'))
print("By: Joshua Smith (aka: killbit -- https://twitter.com/Josh2all)\n\n")


if len(sys.argv)==1:
    print('USAGE: ./sweeNverify.py [TARGET_RANGE_LIST_FILE_NAME]\n\n\n')

converted_list_of_ranges=[]
listOfUpHosts=[]
unalteredRanges=[]
converted_list_of_uphosts=[]

def convertRangeListFile():
    f = open(sys.argv[1], 'r')
    for line in f:
        if line == '' or line == ' ':
            skip
        else:
            unalteredRanges.append(line.rstrip("\n"))
            converted_list_of_ranges.append(ipaddress.ip_network(line.rstrip("\n")))
    f.close()

def convertUpHostsList(uphosts):
    for line in uphosts:
        converted_list_of_uphosts.append(ipaddress.ip_address(line.rstrip("\n")))

countingdown=len(unalteredRanges)
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
    return(uphosts)


convertRangeListFile()
up_hosts = []
for each_range in unalteredRanges:
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

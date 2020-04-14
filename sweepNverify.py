#! /usr/bin/python3 
import ipaddress
import sys
import subprocess

'''
THIS IS VERSION 2 and includes the ping sweep done for you:

USE ADVICE AT YOUR OWN RISK, I AM IN NO WAY RESPONSIBLE FOR THE MISUSE OF THESE INSTRUCTIONS NO THE TOOL ITSELF
This tool was created by killbit follow me on twitter @josh2all (https://twitter.com/Josh2all).
Feel free to use this not so awesome code, just give me credit for my work. Thank you.

Are you tired of having to test if you have access IP addresses within a long list of IP ranges pointing at an excel doc with one hand and your fping out file with the other?

USAGE:
1. Create line seperated list of IP ranges 
2. ./sweepNverify.py [YOUR_LIST_FILE]

'''

#if len(sys.argv[1])==0 or len(sys.argv[2])==0 :
#    print("Usage:> ./ipNrangeVerification.py [FILE_OF_RANGES] [FILE_OF_UPHOSTS_FROM_FPING.OUT]")

converted_list_of_ranges=[]
listOfUpHosts=[]
unalteredRanges=[]
converted_list_of_uphosts=[]

def convertRangeListFile():
    f = open(sys.argv[1], 'r')
    for line in f:
        unalteredRanges.append(line.rstrip("\n"))
        converted_list_of_ranges.append(ipaddress.ip_network(line.rstrip("\n")))
    f.close()

def convertUpHostsList(uphosts):
    for line in uphosts:
        converted_list_of_uphosts.append(ipaddress.ip_address(line.rstrip("\n")))

countingdown=len(unalteredRanges)
def pingsweep(ip_range):
    print("Pingsweeping --> ",ip_range) 
    scan = subprocess.run(['/usr/bin/fping','-a','-q','-g',ip_range],text=True,capture_output=True)
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
    outfile.write("%s\n" % each)

outfile.close()
print("Outfile named, 'josh-done-did-yo-pingsweep.out' created in same directory as script was run!")

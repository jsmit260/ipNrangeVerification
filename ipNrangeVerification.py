#! /usr/bin/python3 
import ipaddress
import sys

'''
USE ADVICE AT YOUR OWN RISK, I AM IN NO WAY RESPONSIBLE FOR THE MISUSE OF THESE INSTRUCTIONS NO THE TOOL ITSELF
This tool was created by killbit follow me on twitter @josh2all (https://twitter.com/Josh2all).
Feel free to use this not so awesome code, just give me credit for my work. Thank you.

Are you tired of having to test if you have access IP addresses within a long list of IP ranges pointing at an excel doc with one hand and your fping out file with the other?

ipNrangeVerication solves this problem simply:
1. Create line seperated list of IP ranges 
2. Run fping command> for each in $(cat targets.list);do fping -a -r 1 -g $each 2>/dev/null >> fping.out; done
3. ./ipNrangeVerification.py [FILE_OF_RANGES] [FILE_OF_UPHOSTS_FROM_FPING.OUT]

'''

#if len(sys.argv[1])==0 or len(sys.argv[2])==0 :
#    print("Usage:> ./ipNrangeVerification.py [FILE_OF_RANGES] [FILE_OF_UPHOSTS_FROM_FPING.OUT]")

listOfRanges=[]
listOfUpHosts=[]
def convertRangeListFile():
    f = open(sys.argv[1], 'r')
    for line in f:
        listOfRanges.append(ipaddress.ip_network(line.rstrip("\n")))
    f.close()


def convertUpHostListFile():
    f= open(sys.argv[2], 'r')
    for line in f:
        listOfUpHosts.append(ipaddress.ip_address(line.rstrip("\n")))
    f.close()


convertRangeListFile()
convertUpHostListFile()

masterListYes=[]
masterListNo=[]
for eachRange in listOfRanges:
    for eachHost in listOfUpHosts:
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


print("[---The following list was NOT reachable---]\n" )
for eachNo in dedup_masterListNo:
    print(eachNo)

print("\n[---The following list were SUCCESSFULLY reached---]\n")
for eachYes in dedup_masterListYes:
    print(eachYes)


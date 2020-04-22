import nmap

 
nma = nmap.PortScannerAsync() 


def nmap_out():
    hosts_list = [(x, nma[x]['status']['state']) for x in nma.all_hosts()]
    for host, status in hosts_list:
        print ('{0}:{1}'.host)
nma.scan(hosts='192.168.2.1', arguments='-T5 -Pn -PS -PA --top-ports 100')
nmap_out()

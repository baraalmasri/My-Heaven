#!/usr/bin/env python
import scapy.all as scapy
import optparse

# code explaning :
#**def get_arguments()
#getting parameters from terminal ex: program.py -`prameter name` `prameter value`
#this ex : simple_network_scanner.py --target or -t  `our ip`**

    # for listing the parameter of ARP() method we can use
    # this > scapy.ls(scapy.ARP()) this method show as how to throgh parameter
    # summary() func. asks for the given ip as this `ARP who has 0.0.0.0`

    # to throw our ip must pdst ipFiled = ip
    # we can do like this `arp_requset.pdst=ip`
    # or wirte it like this arp_requset=scapy.ARP(pdst=ip)
#for asking about mac address we need to send it to broadcast
    #broadcast will ask all ip`s about the wanted mac address so
    # let's ask for ff:ff:ff:ff:ff:ff: virtual mac address
#output >> this our device address 22:44:66:77:89:1f > ff:ff:ff:ff:ff:ff: (0x9000)
#for more detials we can use show() function for ever of arp and ether and arpBroadcast too
#----------------------------------------
    # srp func. meaning `send or receive packet` so this will send a packet and waite for response
    #we need to send this to broadcast and waiting response as macAddress of ip owner
    #srp return to value (packet sent,answer) and unanswered packet
    #timeout is the time value of waiting response,
    # #if we did not set the value this make program wait for lifeTime so 2 second enough
# we can throw unansweredList and use just 1 variable by wirting :
# answered_response_list = scapy.srp(arp_requset_broadcast,timeout=1)[0] because the variables are list
#note need to give program a permission to group `chmod 707 scanner.py`
    #for printing the ip and mac address without any other not used info
#every one element is packet and have to value (request,response )
        #so we listing answered list that meaning we have responses so element[1] is the responses
        #and in the responses there's many don't needed info we need ip and mac only so we`ll use
        #psrc: ip of source device  and hwsrc : mac of source device
        #print(element[1].psrc)
        #print(element[1].hwsrc)

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
    options, arguments = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n-------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)


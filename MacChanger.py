import subprocess
import re
import optparse

#this func. for geting parameters from user on the terminal as > mac_changer.py -i eth0 -m 22:33:56:7...
def get_parameters_from_terminal():
    parser = optparse.OptionParser()

    parser.add_option("-m", "--macaddress", dest="mac", help="device physical address ")
    parser.add_option("-i", "--interface", dest="interface", help="interface ,as eth0 ,wlan0 ,l0 ...etc")
    (values, parameters) = parser.parse_args()

    return values.mac ,values.interface

#this func.execute this command that changing the mac from terminal . so you can change it by write these cmds
def mac_changer(TheInterface,New_Mac):
    subprocess.call("ifconfig eth0 down", shell=True)
    subprocess.call("ifconfig "+TheInterface+" hw ether " + New_Mac, shell=True)
    subprocess.call("ifconfig "+TheInterface+" up", shell=True)
    print("[+] mac deresiniz degistirildi")

#this func. get your old or previous mac form `ifconfig` command output ,powered by re module 
#this module need https://pythex.org to detect your regular grammer exm:mac address reg. is \w\w: 
#so w is maybe one charcter or digit  
def get_macAddress_from_terminal_output(someInterface):
    if (someInterface =="eth0"):
        terminal_output = subprocess.check_output(["ifconfig","eth0" ])
    elif (someInterface=="wlan0"):
        terminal_output = subprocess.check_output(["ifconfig", "wlan0"])
    else:
        print("[-] there is no interface like this  !!")
        return
    old_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(terminal_output))
    return old_mac.group(0)

#--------------------------------------------------------------------------------
New_Mac,TheInterface= get_parameters_from_terminal()

the_old_mac= get_macAddress_from_terminal_output(TheInterface)

if(the_old_mac == New_Mac):
    print("The mac address you added is the same as the old mac! ")
else:
    mac_changer(TheInterface,New_Mac)
    print("[+] previous mac address :"+ str(the_old_mac))
    print("[+] your new mac address :"+ str(New_Mac))





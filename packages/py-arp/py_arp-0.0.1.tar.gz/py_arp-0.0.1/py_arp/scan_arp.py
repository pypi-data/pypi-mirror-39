from sys import argv
from time import sleep
from datetime import datetime
from json import dump

from pprint import pprint
from scapy.all import srp, Ether, ARP, conf, arping
from requests import get

from Target import Target
from utils import make_subnets, target_to_json
#from py_slack.post_hook import send_hook_msg


def make_target(ip):
    ans, unans = arping(ip)
    conf.verb = 0
    for snd,rcv in ans:
        ipv4 = ip
        mac = rcv[Ether].src
        manu = find_vendor(mac)
        return Target(ipv4, mac, manu)

def arp_scan(net_iface):
    subnets = make_subnets()
    for net in subnets:
        if '\n' in net:
            net = net.strip('\n')
        conf.verb = 0
        ans, unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=net),timeout=2, iface=net_iface, inter=0.1)
        targets = []

        for snd,rcv in ans:
            ipv4 = r cv.sprintf(r'%ARP.psrc%')
            mac = rcv.sprintf(r'%Ether.src%')
            manu = find_vendor(mac)

            T = Target(ipv4, mac, manu)
            t_data = [T.ipv4, T.mac, T.manu]
            #send_hook_msg(t_data, hook_url)
            targets.append(T)
            pprint(t_data)

    return targets

def find_vendor(mac):
    #source: https://macvendors.co/api/python
    req = get('http://macvendors.co/api/%s' % mac)
    manu_data = req.json()
    return manu_data

def write_arp_file(target_arr, fname='arpscan.null'):
    ftype = fname.split('.')[1]

    if ftype == '.csv':
        for T in target_arr:
            text =  str(T.ip) + ',' + str(T.mac) + ',' + str(T.ts) + '\n'
            with open(fname, 'a+') as f:
                f.write(text)

    elif ftype == 'json':
        json_name = 'targets_' + target_arr[0].ipv4
        data = {}
        data[json_name] = []

        for T in target_arr:
            target_info = target_to_json(T)
            data[json_name].append(target_info)

        with open(fname, 'a+') as f:
            dump(data,f)
    else:
        return

    return

if __name__ == '__main__':
    try:
        n_args = len(argv)
        if n_args == 3:
            argv[1] = network_interface
            argv[2] = outfile
            write_arp_file(arp_scan(network_interface), outfile)
        elif n_args == 2:
            arp_scan(network_interface)
    except

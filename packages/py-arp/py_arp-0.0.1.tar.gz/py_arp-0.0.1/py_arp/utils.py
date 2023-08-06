#!/usr/bin/env python3
from subprocess import check_output


def make_subnets():
    
    subnets = []
    ip_addr = check_output('hostname -I',shell=True).decode('utf-8')
    addrs = ip_addr.split(' ')
    
    for addr in addrs:
        if addr[:2].isdigit() == False:
            continue
        subnets.append(addr.rsplit('.',1)[0] + '.0/24\n')
    return subnets

def get_gateway():
    cmd = 'ip route|cut -d " " -f 3'
    gateway = check_output(cmd, shell=True).decode('utf-8')
    return gateway.split('\n')[0]

def target_to_json(T):
    return {'ts':str(T.ts), 'ipv4':T.ipv4, 'mac':T.mac, 'manu':T.manu}


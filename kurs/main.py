#!/usr/bin/env python
# -*- coding: utf_8 -*-
__author__ = 'issahar'
import scan_threads

host0 = '127.0.0.1'
host1 = '192.168.1.1'
host2 = '192.168.1.3'
host3 = '192.168.1.5'
host4 = '192.168.1.7'
host5 = '192.168.1.8'
load_hosts = [host0, host1, host2, host3, host4, host5]
load_ports = [21, 23, 53, 67, 69, 80, 443, 445]
open_tcp_ports = {}
open_udp_ports = {}

# opens = {'host1': [1, 2, 3, 4, 5], 'host2': [231, 23, 543, 521]}

if __name__ == '__main__':
    a, b = scan_threads.loading_data(load_hosts, load_ports, 2)
    print a,' - ', b
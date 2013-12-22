#!/usr/bin/env python
# -*- coding: utf_8 -*-
__author__ = 'issahar'
from scan_threads import loading_data
from comparison import comparison_port
import sys
import time
import re

if __name__ == '__main__':
    ips = []
    ports = []

    ip_input = sys.argv[1]
    ip_ranges = ip_input.split(',')
    reg = '([1-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])[- /.]([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])' \
          '[- /.]([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])[- /.]([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])'
    port_input = sys.argv[2]
    port_ranges = port_input.split(',')
    threads = sys.argv[3]

    def make_ip_list(start_ip, last_ip):
        s1, s2, s3, s4 = start_ip.split('.')
        l1, l2, l3, l4 = last_ip.split('.')
        host_list = []
        while True:
            if int(s1) == int(l1) and int(s2) == int(l2):
                if int(s3) == int(l3):
                    if int(s4) != int(l4):
                        size = int(l4)-int(s4)
                        host_list.append(str(s1)+'.'+str(s2)+'.'+str(s3)+'.'+str(s4))
                        for i in range(size):
                            s4 = int(s4) + 1
                            host_list.append(str(s1)+'.'+str(s2)+'.'+str(s3)+'.'+str(s4))
                    else:
                        break
                else:
                    if int(s4) <= 254:
                        size = 255-int(s4)
                        host_list.append(str(s1)+'.'+str(s2)+'.'+str(s3)+'.'+str(s4))
                        for i in range(size):
                            s4 = int(s4) + 1
                            host_list.append(str(s1)+'.'+str(s2)+'.'+str(s3)+'.'+str(s4))
                        time.sleep(1)
                    s3 = int(s3) + 1
                    s4 = 1
            else:
                print "too long ip range, aborting..."
                return None
        return host_list

    def make_port_list(start_port, last_port):
        port_list = []
        while start_port <= last_port:
            port_list.append(start_port)
            start_port += 1
        return port_list

    for ran in ip_ranges:
        if not '-' in ran:
            if re.match(reg, ran):
                ips.append(ran)
        else:
            a, b = ran.split('-')
            if re.match(reg, a) and re.match(reg, b):
                ips.extend(make_ip_list(a, b))
            else:
                er_key = True

    for p in port_ranges:
        if not '-' in p:
            ports.append(int(p))
        else:
            a, b = p.split('-')
            if int(a) < 65536 and int(b) < 65536:
                ports.extend(make_port_list(int(a), int(b)))
    print "Ready for looking... Please, waiting some times..."
    tcp, udp = loading_data(ips, ports, int(threads))
    print "Search complited. Comparing TCP ports... "
    comparison_port(tcp)
    print "\nComparing UDP ports... "
    comparison_port(udp)
    sys.exit("\nHave a good day!")
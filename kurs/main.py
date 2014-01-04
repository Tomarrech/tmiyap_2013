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
    er_key = False
    ip_input = sys.argv[1]
    ip_ranges = ip_input.split(',')
    ip_match_reg = '([1-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])[.]([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])' \
                   '[.]([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])[.]([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])'
    port_input = sys.argv[2]
    port_ranges = port_input.split(',')
    threads = sys.argv[4]
    s_type = sys.argv[3]

    def make_ip_list(start_ip, last_ip):
        s1, s2, s3, s4 = start_ip.split('.')
        l1, l2, l3, l4 = last_ip.split('.')
        host_list = []
        while True:
            if int(s1) == int(l1) and int(s2) == int(l2):
                if int(s3) == int(l3):
                    if int(s4) != int(l4):
                        size = int(l4) - int(s4)
                        host_list.append(str(s1) + '.' + str(s2) + '.' + str(s3) + '.' + str(s4))
                        for i in range(size):
                            s4 = int(s4) + 1
                            host_list.append(str(s1) + '.' + str(s2) + '.' + str(s3) + '.' + str(s4))
                    else:
                        break
                else:
                    if int(s4) <= 254:
                        size = 255 - int(s4)
                        host_list.append(str(s1) + '.' + str(s2) + '.' + str(s3) + '.' + str(s4))
                        for i in range(size):
                            s4 = int(s4) + 1
                            host_list.append(str(s1) + '.' + str(s2) + '.' + str(s3) + '.' + str(s4))
                        time.sleep(1)
                    s3 = int(s3) + 1
                    s4 = 1
            else:
                print "too long ip range or smt not correct, aborting..."
                sys.exit(-1)
        return host_list

    try:
        for ran in ip_ranges:
            if not '-' in ran:
                if re.match(ip_match_reg, ran):
                    ips.append(ran)
                else:
                    er_key = True
            else:
                a, b = ran.split('-')
                if re.match(ip_match_reg, a) and re.match(ip_match_reg, b):
                    ips.extend(make_ip_list(a, b))
                else:
                    er_key = True
    except:
        er_key = True

# по номеру в массиве определять порт, 1 - сканирвоать, 0 - пропустить

    def make_port_list(port_list, start_port, last_port):
        for val in range(1, 65535):
                if int(last_port) >= val >= int(start_port):
                    port_list[val] = 1
                else:
                    port_list[val] = 0

    ports = [0]
    for val in range(1, 65535):
        ports.append(0)
        for p in port_ranges:
            if not '-' in p:
                if val == int(p) and int(p) < 65536:
                    ports[val] = 1
                elif val != int(p) and int(p) < 65536:
                    pass
                else:
                    er_key = True
    for p in port_ranges:
        if '-' in p:
            a, b = p.split('-')
            if int(a) < 65536 and int(b) < 65536:
                make_port_list(ports, int(a), int(b))
            else:
                er_key = True

    if er_key is True:
        sys.exit("Something is not correct with IP or port, try again.")

    print "Ready for scanning... Please, waiting some times..."
    tcp, udp = loading_data(ips, ports, s_type, int(threads))
    print "\n\n\nScan complited."
    if s_type == 'tcp':
        print "\nComparing TCP ports... "
        comparison_port(tcp)
    else:
        print "\nComparing UDP ports... "
        comparison_port(udp)
    sys.exit("\nWork done, enjoy!")
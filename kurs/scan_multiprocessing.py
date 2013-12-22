#!/usr/bin/env python
# -*- coding: utf_8 -*-
import time
import sys
__author__ = 'issahar'
import socket
from multiprocessing import Process

open_tcp_ports = {}
open_udp_ports = {}
# opens = {'host1': [1, 2, 3, 4, 5], 'host2': [231, 23, 543, 521]}


def scan(hosts, ports):

    #print 'get: ', hosts
    global open_tcp_ports
    global open_udp_ports

    for host in hosts:
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.01)
                sock.connect((host, port))
                sock.close()
            except:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(0.01)
                    sock.sendto("--TEST LINE__", (host, port))
                    recv, svr = sock.recvfrom(255)
                    sock.shutdown(2)
                    sock.close()

                    if not host in open_udp_ports:
                        open_udp_ports[host] = []
                    open_udp_ports[host].append(port)
                except:
                    pass
            else:
                if not host in open_tcp_ports:
                    open_tcp_ports[host] = []
                open_tcp_ports[host].append(port)
        print 'ports on host %s: %s %s' % (host, open_tcp_ports, open_udp_ports)


def loading_data(t_hosts, t_ports, threads=1):

    real_threads = threads if threads >= len(t_hosts) else len(t_hosts)
    #print "real thr: ", real_threads
    hosts_on_thread = len(t_hosts) / real_threads
    #print "t_hosts/thr: ", hosts_on_thread

    for thr in range(real_threads):
        start = thr * hosts_on_thread
        stop = (thr + 1) * hosts_on_thread if thr != real_threads - 1 else real_threads
        #print "start, stop, thr: ", start, stop, thr
        #print "host for process: ", t_hosts[start:stop]
        Process(target=scan, args=(t_hosts[start:stop], t_ports)).start()
        time.sleep(0.25)
        print "total:\n\ttcp: %s; udp: %s" % (open_tcp_ports, open_udp_ports)
    return open_tcp_ports, open_udp_ports
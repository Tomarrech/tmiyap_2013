#!/usr/bin/env python
# -*- coding: utf_8 -*-
import time
import thread
import sys
__author__ = 'issahar'
import socket
from threading import *

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


def scan(hosts, ports):

    #print 'get: ', hosts
    global open_tcp_ports
    global open_udp_ports

    for host in hosts:
        #print host
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
                    print "host:port %s:%s /udp open" % (host, port)
                    if not host in open_udp_ports:
                        open_udp_ports[host] = []
                    open_udp_ports[host].append(port)
                    print 'udp ', open_udp_ports
                except:
                    #print "smth was wrong..."
                    #print "port %s /udp closed" % port
                    pass

                #print "port %s /tcp closed"
            else:
                #print "host:port %s:%s /tcp open" % (host, port)
                if not host in open_tcp_ports:
                    open_tcp_ports[host] = []
                open_tcp_ports[host].append(port)
                print 'tcp ', open_tcp_ports, open_udp_ports
    #thread.exit()

def loading_data(t_hosts, t_ports, threads=1):
    real_threads = threads if threads >= len(t_hosts) else len(t_hosts)
    print "real thr: ", real_threads
    hosts_on_thread = len(t_ports) / real_threads
    print "t_hosts/thr: ", hosts_on_thread

    for thr in range(real_threads):
        start = thr * hosts_on_thread
        stop = (thr + 1) * hosts_on_thread if thr != real_threads - 1 else real_threads
        #print "start, stop: ", start, stop
        #print "host for thread: ", t_hosts[start:stop]
        worker = Thread(target=scan, args=(t_hosts[start:stop], t_ports))
        worker.daemon = True
        worker.start()
        time.sleep(1)

loading_data(load_hosts, load_ports, 2)
#print "total:\n\ttcp: %s; udp: %s" % (open_tcp_ports, open_udp_ports)
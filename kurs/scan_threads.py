#!/usr/bin/env python
# -*- coding: utf_8 -*-
__author__ = 'issahar'
import socket
import time
from threading import *

open_tcp_ports = {}
open_udp_ports = {}

# 127.0.0.1 2-20 tcp 1
def scan_tcp(hosts, ports):

    for host in hosts:
        if not host:
            print "Empty host"
            break
        for port in range(1, len(ports)):
            print port, ports[port]
            if ports[port] != 1:
                continue
            else:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((host, port))
                    sock.close()
                except socket.error:
                    pass
                else:
                    if not host in open_tcp_ports:
                        open_tcp_ports[host] = []
                    open_tcp_ports[host].append(port)
        print "host %s for TCP is ready." % host


def scan_udp(hosts, ports):
    for host in hosts:
        if not host:
            print "Empty host"
            break
        for port in ports:
            if port == ports[len(ports)/2]:
                print "for host %s scanned a half of ports\n" % host
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(1)
                sock.sendto("--TEST LINE__", (host, port))
                recv, svr = sock.recvfrom(5)
                sock.shutdown(2)
                sock.close()
            except socket.error:
                pass
            else:
                if not host in open_udp_ports:
                    open_udp_ports[host] = []
                open_udp_ports[host].append(port)
        print "host %s for UDP is ready." % host


def loading_data(t_hosts, t_ports, s_type, threads=1):

    real_threads = threads if threads <= len(t_hosts) else len(t_hosts)
    hosts_on_thread = len(t_hosts) / real_threads

    threads = []

    for thr in range(real_threads):
        start = thr * hosts_on_thread
        stop = (thr + 1) * hosts_on_thread if thr != real_threads - 1 else len(t_hosts)
        print 'Start new thread with hosts %s' % t_hosts[start:stop]
        if s_type == "tcp":
            th = Thread(target=scan_tcp, args=(t_hosts[start:stop], t_ports))
        elif s_type == "udp":
            th = Thread(target=scan_udp, args=(t_hosts[start:stop], t_ports))
        else:
            print "unknown type, quiting.."
            exit('protocol error')
        th.start()
        threads.append(th)

    for tr in threads:
        tr.join()

    return open_tcp_ports, open_udp_ports
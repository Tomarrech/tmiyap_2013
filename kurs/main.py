#!/usr/bin/env python
# -*- coding: utf_8 -*-
__author__ = 'issahar'
import socket

host1 = '192.168.1.1'
host2 = '192.168.1.3'
host3 = '192.168.1.5'
host4 = '192.168.1.7'
hosts = [host1, host2, host3, host4]
ports = [21, 23, 53, 67, 69, 80, 443, 445]
open_tcp_ports = {}
open_udp_ports = {}


def scan(hosts, ports):
    #ports = []
    #for x in xrange(6000):
    #    ports.append(x)
    global open_tcp_ports
    open_tcp_ports = {}
    global open_udp_ports
    open_udp_ports = {}

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
                    print "port %s /udp open" % port
                    open_udp_ports.append(port)
                except:
                    #print "port %s /udp closed" % port
                    continue

                #print "port %s /tcp closed"
            else:
                print "port %s /tcp open" % port
                open_tcp_ports.append(port)

        print "on host %s open ports:" % host
        print "tcp: %s; udp: %s" % (open_tcp_ports, open_udp_ports)



scan(hosts, ports)

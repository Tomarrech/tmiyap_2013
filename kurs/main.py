#!/usr/bin/env python
# -*- coding: utf_8 -*-
__author__ = 'issahar'

import socket

host = '192.168.1.1'

ports = []

for x in xrange(65536):
    ports.append(x)

open_ports = []

for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        sock.connect((host, port))
    except:
        continue
        #print "port closed"
    else:
        result = sock.recv(1024)
        print "port %s open" % port
        print result
    sock.close()

print "open ports:"
print open_ports

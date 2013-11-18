__author__ = 'issahar'
#coding: utf-8
from time import sleep
import socket
import os
HOST = ""
PORT = 9090

FILE = 'send.txt'
if os.path.getsize(FILE) == 64:
    print "SIZE - OK"
    connectLost = True
else:
    print "SIZE - ERROR"
    connectLost = False
sleep(1)
while connectLost:
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs.connect((HOST, PORT))
        cs.send("SEND " + FILE)
        sleep(1)

        f = open(FILE, "rb")
        data = f.read()
        f.close()
        print 'Sending file %s' % FILE
        cs.send(data)
        print 'Sending file %s - OK' % FILE
        while 1:
            print 'loading flag...'
            cs.settimeout(1)
            data = cs.recv(100)
            print data
            if not data:
                break
        cs.close()
        break
        #connectLost = False
    except:
        print '\nConnection lost to %s:%s' % (HOST, PORT)
        sleep(0.1)
        connectLost = False
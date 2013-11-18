from time import sleep

__author__ = 'issahar'
import socket
import os
HOST = "127.0.0.1"
PORT = 9090

FILE = 'send2.txt'
if os.path.getsize(FILE) == 64:
    print "SIZE - OK"
    connectLost = True
else:
    print "SIZE - ERROR"
    connectLost = True
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
            print 'getting flag...'
            data = cs.recv(30)
            if not data:
                break
            print 'flag is ', data
        cs.close()
        break
        #connectLost = False
    except:
        print '\nConnection lost to %s:%s' % (HOST, PORT)
        sleep(0.1)
        connectLost = False
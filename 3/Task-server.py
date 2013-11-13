__author__ = 'issahar'
#coding: utf-8
import socket
from threading import *
from os import path, remove

flag = "{0123456789abcdef0123456789ABCDEF}"
sigma = False


class StreamHandler (Thread):

    def __init__(this):
        Thread.__init__(this)

    def run(this):
        this.process()

    def bindsock(this):
        this.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.sock.bind(("", 9090))
        this.sock.listen(10)
        print '[File-Server] Listening on port 9090'

    def acceptsock(this):
        this.conn, this.addr = this.sock.accept()
        print "[File-Server] have connected from", this.addr
        while True:
            data = this.conn.recv(16)
            if not data:
                break
            if data[0:4] == "SEND": this.filename = data[5:]
            print "[File-Server] is ready to receive ", this.filename
            break

    def transfer(this):
        filename = './in/' + path.basename(this.filename)
        print "open new"
        f = open(filename, "wb")
        while 1:
            print 'loading...'
            this.sock.settimeout(1)
            data = this.conn.recv(100)
            if not data:
                break
            f.write(data)
        f.close()

        if path.getsize(this.filename) == 64:
            print "Bingo!"
            this.sock.send(flag)
        else:
            print "Suck!"
            this.sock.send("try again!")

        print '[File-Server] Got "%s"' % filename
        print '[File-Server] Closing transfer for "%s"' % filename

    def close(this):
        this.conn.close()
        this.sock.close()

    def process(this):
        while 1:
            this.bindsock()
            this.acceptsock()
            this.transfer()
            this.close()


s = StreamHandler()
s.start()
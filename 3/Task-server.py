__author__ = 'issahar'
#coding: utf-8
import socket
from threading import *
from os import path

flag = "flag{154afd654cae654f}"
sigma = False


class StreamHandler (Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.process()

    def bindsock(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("", 9090))
        self.sock.listen(10)
        print '[File-Server] Listening on port 9090'

    def acceptsock(self):
        self.conn, self.addr = self.sock.accept()
        print "[File-Server] have connected from", self.addr
        while True:
            data = self.conn.recv(16)
            if not data:
                break
            if data[0:4] == "SEND": self.filename = data[5:]
            print "[File-Server] is ready to receive ", self.filename
            break

    def transfer(self):
        filename = './in/' + path.basename(self.filename)
        print "open new"
        f = open(filename, "wb")
        data = ''
        try:
            while not data:
                print 'loading...'
                self.conn.settimeout(3)
                data = self.conn.recv(100)

                f.writelines(data)
        except:
            print "fail =)"

        f.close()
        print "file written!\n"

        if path.getsize(self.filename) == 64:
            print "Correct file from", self.addr
            self.conn.send(str(flag))
            self.conn.close()
        else:
            print "Suck!"
            self.conn.send("Uncorrected file try again!{16KB only}")

        print '[File-Server] Got "%s"' % filename
        print '[File-Server] Closing transfer for "%s"' % filename

    def close(self):
        self.conn.close()
        self.sock.close()

    def process(self):
        while 1:
            self.bindsock()
            self.acceptsock()
            self.transfer()
            self.close()


s = StreamHandler()
s.start()
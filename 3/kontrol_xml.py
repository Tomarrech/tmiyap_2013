__author__ = 'issahar'
import socket
from threading import *
from lxml import etree
from lxml.builder import E

HOST = "127.0.0.1"
PORT = 5858


class StreamHandler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.templ_int = 0

    def run(self):
        self.process()

    def bindsock(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen(10)
        print '[File-Server] Listening on port ', PORT

    def acceptsock(self):
        self.conn, self.addr = self.sock.accept()
        print "[File-Server] have connected from", self.addr
        while True:
            data = self.conn.recv(1024)
            print data
            if not data:
                break
            try:
                root = etree.fromstring(data)
                print root
                command = {
                    'command': root.attrib['com'],
                    'acts': [{
                                 'sign': el.attrib['sign'],
                                 'num': el.attrib['num'],
                             } for el in root.find('acts').iter('act')]
                }
                print command

                if command['command'] == 'get':
                    self.send_int()
                elif command['command'] == 'clear':
                    self.clear()
                elif command['command'] == 'set':
                    self.set(command['acts'])
                else:
                    print "unkn command!"
            except:
                print "Not json"

    def clear(self):
        print 'clear data'
        self.conn.send('data cleared')

    def send_int(self):
        print "sending temp"
        res = '<?xml version="1.0" encoding="UTF-8"?> <result res= %s </result>' % self.templ_int
        print res
        self.conn.send(res)

    def set(self, acts):
        print 'change temp as', acts['sign'], acts['num']
        if acts['sign'] == '+':
            self.templ_int += acts['num']
        elif acts['sign'] == '-':
            self.templ_int -= acts['num']
        elif acts['sign'] == '*':
            self.templ_int = self.templ_int * acts['num']
        elif acts['sign'] == '/' and acts['num'] != 0:
            self.templ_int = self.templ_int / acts['num']
        else:
            print "Err"
        self.conn.send('complited!')

    def close(self):
        self.conn.close()
        self.sock.close()

    def process(self):
        while 1:
            self.bindsock()
            self.acceptsock()
            self.close()


s = StreamHandler()
s.start()
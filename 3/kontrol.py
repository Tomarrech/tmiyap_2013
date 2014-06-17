__author__ = 'issahar'
import socket
from threading import *
import json
from os import path, remove, makedirs
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8585


class StreamHandler (Thread):

    def __init__(self):
        Thread.__init__(self)

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
        self.templ_int = 0
        while True:
            data = self.conn.recv(1024)
            print data
            if not data:
                break
            try:
                json_data = json.loads(data)
                if json_data['command'] == 'get':
                    self.send_int()
                elif json_data['command'] == 'clear':
                    self.clear()
                elif json_data['command'] == 'set':
                    self.set(json_data['sign'], json_data['int'])
                else:
                    print "unknown command"
                    break
            except:
                print "Not json"

    def clear(self):
        print 'clear data'
        self.conn.send('data cleared')

    def send_int(self):
        print "sending temp"
        res = '{"result": "%s"}' % self.templ_int
        print res
        self.conn.send(res)

    def set(self, sign, num):
        print 'change temp as', sign, num
        if sign == '+':
            self.templ_int += num
        elif sign == '-':
            self.templ_int -= num
        elif sign == '*':
            self.templ_int = self.templ_int * num
        elif sign == '/' and num != 0:
            self.templ_int = self.templ_int / num
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
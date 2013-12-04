#coding: utf-8
__author__ = 'tomar_000'
import socket
import os
HOST = "127.0.0.1"
PORT = 8989

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((HOST, PORT))

#cs.send("ping")
data = cs.recv(1024)
print data
while True:
    com = raw_input('input command: ')
    cs.send(com)
    if com == '-q':
        break
    data = cs.recv(1024)
    print data
cs.close()
print "end!"
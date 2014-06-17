#coding: utf-8
__author__ = 'tomar_000'
import socket
import os
HOST = "127.0.0.1"
PORT = 8585

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((HOST, PORT))

#cs.send("ping")
#data = cs.recv(1024)
#print data
#while True:
    #com = '{"command": "get"}'
    #com = '{"command": "clear"}'
com = '{"command": "set", "sign": "+", "int": 111}'
cs.send(com)
data = cs.recv(1024)
print data

com = '{"command": "get"}'
cs.send(com)
data = cs.recv(1024)
print data

com = '{"command": "set", "sign": "*", "int": 25}'
cs.send(com)
data = cs.recv(1024)
print data

com = '{"command": "get"}'
cs.send(com)
data = cs.recv(1024)
print data

com = '{"command": "clear"}'
cs.send(com)
data = cs.recv(1024)
print data

cs.close()
print "end!"
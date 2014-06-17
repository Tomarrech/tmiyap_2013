#coding: utf-8
__author__ = 'tomar_000'
import socket
import os
HOST = "127.0.0.1"
PORT = 5858

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((HOST, PORT))

#cs.send("ping")
#data = cs.recv(1024)
#print data
#while True:
    #com = '{"command": "get"}'
    #com = '{"command": "clear"}'
com1 = '<?xml version="1.0" encoding="UTF-8"?> <command com="get"</command>'
com2 = "<?xml version='1.0' encoding='UTF-8'?> <command com='set'> <acts> <act sign='+' num = 12</acts></command>"
com3 = '<?xml version="1.0" encoding="UTF-8"?> <command com="clear"</command>'
com4 = "<?xml version='1.0' encoding='UTF-8'?> <command com='set'> <acts> <act sign='*' num = 15</acts></command>"

cs.send(com2)
data = cs.recv(1024)
print data

cs.send(com1)
data = cs.recv(1024)
print data

cs.send(com4)
data = cs.recv(1024)
print data

cs.send(com1)
data = cs.recv(1024)
print data

cs.send(com3)
data = cs.recv(1024)
print data


cs.send(com1)
data = cs.recv(1024)
print data

cs.close()
print "end!"
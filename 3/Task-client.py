__author__ = 'issahar'
import socket
import os

conn = socket.socket()
conn.connect(("192.168.1.3", 14900))

print os.path.getsize('send.txt')

f = open('send.txt', 'r')
info = f.read()
while info:
    conn.send(info)
    info = f.readline()

data = conn.recv(100)
while True:
    if not data:
        print "No data"
        break
    else:
        print(data.decode("utf-8"))
        data = conn.recv(50)


conn.close()
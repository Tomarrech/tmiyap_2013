__author__ = 'tomar_000'
import socket

sock = socket.socket()

sock.bind('192.168.1.3',14900)
sock.listen(10)

conn, addr = sock.accept()

print 'qwe'

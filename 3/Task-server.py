__author__ = 'issahar'
import socket

sock = socket.socket()

sock.bind(("192.168.1.3", 14900))
sock.listen(10)

conn, addr = sock.accept()
conn.settimeout(60)
data = conn.recv(16384)

if not data:
    print "No data"
else:
    udata = data.decode("utf-8")
    print("Data: " + udata)

conn.send(b"Hello\n")
conn.send(b"Welcome!")

conn.close()
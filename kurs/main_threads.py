__author__ = 'issahar'
from threading import *
import socket
import subprocess
from Queue import Queue

queue = Queue()
#pueue = Queue()
load_hosts = ['192.168.1.1', '192.168.1.3', '192.168.1.5', '192.168.1.7', '192.168.1.8', '192.168.1.9']
load_ports = [21, 23, 53, 67, 69, 80, 443, 445]
#load_ports = []
#for x in xrange(1, 82):
#    load_ports.append(x)
num_threads = len(load_ports)
open_tcp_ports = []
open_udp_ports = []

def scan(q, ports):
    host = q.get()
    #port = p.get()
    global open_tcp_ports
    open_tcp_ports = []
    global open_udp_ports
    open_udp_ports = []

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((host, port))
            sock.close()
        except Exception:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(0.01)
                sock.sendto("--TEST LINE__", (host, port))
                recv, svr = sock.recvfrom(255)
                sock.shutdown(2)
                sock.close()
                print "port %s:  %s /udp open" % (host, port)
                open_udp_ports.append(port)
            except Exception:
                print "port %s:%s /udp closed" % (host, port)
                pass

            #print "port %s /tcp closed"
        else:
            print "port %s:%s /tcp open" % (host, port)
            open_tcp_ports.append(port)
    q.task_done()

for ip in load_hosts:
    queue.put(ip)


for i in range(num_threads):
    worker = Thread(target=scan, args=(queue, load_ports))
    worker.setDaemon(True)
    worker.start()


print "Main Thread Waiting"
queue.join()
#pueue.join()
print "Done "#, open_tcp_ports, open_udp_ports
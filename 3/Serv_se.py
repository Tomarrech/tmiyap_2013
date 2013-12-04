__author__ = 'issahar'
import select
import socket
import sys

host = ''
port = 8989
backlog = 5
size = 1024


def add_good(params):
    print 'Good:', params


def add_order(params):
    print 'Order: ', params


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(backlog)

input = [server]

running = True
while running:
    inputready, outputready, exceptready = select.select(input, [], [])

    for s in inputready:

        if s == server:
            # handle the server socket
            client, address = server.accept()
            input.append(client)
            print address
            mess = u"If you want to stop server, send -s\n If you want to create new good send -g\n" \
                u"If you want to create new order send -o\n For quit send -q\n"
            client.send(mess)
            print "hello message sent"
        else:
            # handle all other sockets
            try:
                command = s.recv(size)
                if command == "-s":
                    print "stop server will be"
                    s.send(u'Server will be stopped')
                    s.close()
                    sys.exit(1)
                elif command == "-g":
                    s.send("ok, input params of good")
                    add_good(s.recv(size))
                    print "done!"
                    s.send(u'Good created!')
                elif command == "-o":
                    s.send('ok, input params of order')
                    add_order(s.recv(size))
                    print "done!"
                    s.send(u'Order created!')
                elif command == "-q":
                    print "disconnecting.."
                    s.close()
                    input.remove(s)
                else:
                    print "got Uncorrected command."
                    s.send(u'Uncorrected command. try again!')
            except socket.error:
                s.close()
                input.remove(s)

server.close()

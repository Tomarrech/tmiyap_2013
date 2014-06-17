#coding: utf-8
__author__ = 'tomar_000'
import asyncore
import socket
import sys
#import console_interface as CI


class MainHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        '''
        mess = u"Hello. If you want to stop server, send -s\n If you want to create new good send -g\n" \
               u"If you want to create new order send -o\n For quit send -q\n"
        self.send(mess)
        print "message sent"
        #print self.recv(10)
        '''
        try:
            command = self.recv(1024)
            print "!command: ", str(command), '.'
            if not command:
                self.close()
            elif command == "-s":
                print "ss"
                self.send(u'Server will be stopped')
                #break
            elif command == "-g":
                self.send(42)
            elif command == "-o":
                print "add Order"
            elif command == "-q":
                print "disconnecting.."
                self.close()
        except socket.error:
            self.close()


class MainServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            MainHandler(sock)
            #print '!hand:', handler

    def handle_error(self):
        print "server error: %s" % sys.exc_value
        sys.exit(1)

server = MainServer('localhost', 8989)
try:
    asyncore.loop()
except KeyboardInterrupt:
    server.stop()
    print 'HTTP Server was stopped'
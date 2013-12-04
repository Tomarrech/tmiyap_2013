#coding: utf-8
__author__ = 'issahar'
#import console_interface
import classes
import sys
import socket
import asyncore
import exceptions

from socket import AF_INET, SOCK_STREAM
from asyncore import dispatcher
from threading import Thread, RLock


class Stream(object):
    def __init__(self, generator):
        object.__init__(self)
        self.data = ''
        self.generator = generator
        self.closed = False

        generator.subscribe(self)

    def update(self, data):
        self.data += data

    def read(self):
        if self.closed:
            return None
        data = self.data
        self.data = ''
        return data

    def close(self):
        self.generator.unsubscribe(self)
        self.closed = True
        self.data = ''


class Server(dispatcher, dict):
    writeable = lambda x: False

    def __init__(self, host=None, port=8989):
        dispatcher.__init__(self)

        self.create_socket(AF_INET, SOCK_STREAM)
        dict.__init__(self, {self.fileno(): self})
        print "server started!"
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(0xA)
        self.dataSource = 3.14134124124124

    def removeClient(self, client):
        del self[client.fileno()]

    def handle_accept(self):
        sock, (host, port) = self.accept()
        print 'new client from %S:%d' % (host, port)

        stream = Stream(self.dataSource)
        self[sock.fileno()] = Client(sock, self, stream)

    def handle_error(self):
        print "server error: %s" % sys.exc_value
        sys.exit(1)


class Client(dispatcher):
    readable = lambda x: False

    def __init__(self, sock, server, stream):
        dispatcher.__init__(self, sock)
        self.server = server
        self.stream = stream
        self.buffer = ''

    def handle_error(self):
        print 'Client error: %s' % sys.exc_value
        import traceback
        print traceback.format_exc(1000)
        sys.exit(1)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def handle_expt(self):
        print 'client dropped connection'
        self.close()

    def close(self):
        self.server.removeClient(self)
        self.stream.close()
        self.buffer = ''
        dispatcher.close(self)

    def writable(self):
        data = self.stream.read()
        if data == None:
            print 'client finished reading'
            self.close()
            return False

        self.buffer += data
        return len(self.buffer) > 0


def main():
    try:
        asyncore.loop(0.1, True, Server('127.0.0.1'))
    except KeyboardInterrupt:
        print '\nBye :)'
        sys.exit(0)

if __name__ == '__main__':
    main()
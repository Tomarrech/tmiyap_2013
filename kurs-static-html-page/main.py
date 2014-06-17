# -*- coding: utf-8 -*-
import socket
import traceback
from threading import Thread
from os import path, remove, makedirs
from datetime import datetime


def encode_http(query, body='', **headers):
    data = [" ".join(query)]

    headers = "\r\n".join("%s: %s" % ("-".join(part.title() for part in key.split('_')), value)
                          for key, value in sorted(headers.iteritems()))

    if headers:
        data.append(headers)

    data.append('')

    if body:
        data.append(body)

    return "\r\n".join(data)


def parse_http(data):
        lines = data.split('\r\n')
        query = lines[0].split(' ', 2)
        body = ''
        headers = {}
        for position, line in enumerate(lines[1:]):
            if not line.strip():
                break
            key, value = line.split(': ', 1)
            headers[key.upper()] = value

            body = '\r\n'.join(lines[position + 2:])
        #print body
        return query, headers, body


class HTTPError(Exception):
    pass


class Request(object):
    """Контейнер с данными текущего запроса и средством ответа на него"""

    def __init__(self, method, url, headers, body, conn):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
        self.conn = conn

    def __str__(self):
        return "%s %s %r" % (self.method, self.url, self.headers)

    def reply(self, code='200', status='OK', body='', **headers):
        headers.setdefault('server', 'localHost/666')
        headers.setdefault('content_type', 'text/html')
        #headers.setdefault('charset', 'UTF-8') why not, fuck?

        headers.setdefault('content_length', len(body))
        headers.setdefault('connection', 'close')
        headers.setdefault('date', datetime.now().ctime())

        self.conn.send(encode_http(('HTTP/1.0', code, status), body, **headers))
        #self.conn.close()


class HTTPServer(Thread):
    def __init__(self, host='', port=8000):
        Thread.__init__(self)

        self.host = host
        self.port = port
        self.handlers = []

    def run(self):
        self.process()

    def bindsock(self):
        """Цикл ожидания входящих соединений"""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.bind(('', 8000))
        self.sock.listen(50)
        print "Сервер поднят. Порт %s прослушивается" % self.port

    def acceptsock(self):
        self.conn, self.addr = self.sock.accept()
        data = self.conn.recv(1024)
        print "data: \n%s\nfrom %s\n" % (data, self.addr)

        (method, url, proto), headers, body = parse_http(data)

        #print method, url, proto, headers, body,
        self.on_request(Request(method, url, headers, body, self.conn))

    def on_request(self, request):
        """Обработка запроса"""
        print "Request ", request

        try:
            for pattern, handler in self.handlers:
                if pattern(request):
                    handler(request)
                    return True
        except HTTPError as error:
            code = error.args[0]
            reply = {
                404: 'Not found',
                403: 'Permission denied',
            }[code]
            request.reply(str(code), reply, "%s: %s" % (reply, request.url))
            return False
        except Exception as err:
            request.reply('500', 'Infernal server error')
            return False

        # никто не взялся ответить
        #request.reply('404', 'Not found', 'Письмо самурай получил<p>Тают следы на песке<p>Page not found.')

        #*********
        self.close_all()

    def register(self, pattern, handler):
        self.handlers.append((pattern, handler))
        pass

    def close_all(self):
        self.conn.close()
        self.sock.close()

    def process(self):
        while 1:
            self.bindsock()
            self.acceptsock()
            #self.transfer()
            self.close_all()

if __name__ == '__main__':
    from handlers import serve_static

    port, root = 8000, '.'

    try:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--port', nargs='?', type=int, default=port)
        parser.add_argument('--root', nargs='?', type=str, default=root)
        options = parser.parse_args()
        port, root = options.port, options.root
    except ImportError:
        pass

    server = HTTPServer(port=8000)
    server.register(*serve_static('/', root))
    server.start()
#coding: utf-8
__author__ = 'issahar'
import sys
import socket
import select

# Telnet protocol defaults
TELNET_PORT = 23  #порт по умолчанию
irawq = 0


class Telnet:
    def __init__(self, host=None, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        self.debuglevel = 0
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        #переменные для очередей
        self.rawq = ''
        self.irawq = 0
        #"сохраненные" строки от сервера, еще не переданные пользователю
        self.cookedq = ''
        #конец строки
        self.eof = 0

        self.iacseq = ''  # Buffer for IAC sequence.
        self.sb = 0  # flag for SB and SE sequence.
        self.sbdataq = ''
        self.option_callback = None
        self._has_poll = hasattr(select, 'poll')
        if host is not None:
            self.open(host, port, timeout)

    def open(self, host, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """Connect to a host.

        The optional second argument is the port number, which
        defaults to the standard telnet port (23).

        Don't try to reopen an already connected instance.
        """
        self.eof = 0
        if not port:
            port = TELNET_PORT
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((host, port), timeout)

    def __del__(self):
        """Destructor -- close the connection."""
        self.close()

    def close(self):
        """Close the connection."""
        if self.sock:
            self.sock.close()
        #закрывает сокеты
        self.sock = None
        #флаг конца файла в 1
        self.eof = 1
        #чистим овчередь
        self.iacseq = ''
        self.sb = 0

    def interact(self):
        import thread
        #создаем в несколько потоков слушателей ответов серера
        thread.start_new_thread(self.listener, ())
        while 1:
            #вводим с клавиатуры команды для сервера
            line = sys.stdin.readline()
            if not line:
                break

            self.write(line)

    def write(self, buffer):
        #все что мы написали, кидаем на сервер
        self.sock.sendall(buffer)

    def listener(self):
        #если соединение не закрыто, принимаем сообщения от сервера
        while 1:
            try:
                #попытка
                data = self.read_eager()
            except EOFError:
                #если не получилось - выводим ошибку
                print '*** Connection closed by remote host ***'
                return
            if data:
                #если получилось, выводим полученое сообщение
                sys.stdout.write(data)
            else:
                #магия
                sys.stdout.flush()

    def read_eager(self):
        #получение информации от сервера
        # ф-ция обработки буфера полученныхз данных
        self.process_rawq()
        while not self.cookedq and not self.eof and self.sock_avail():
            #ф-ция добавления получаемыых данных в буфер
            self.fill_rawq()
            # ф-ция обработки буфера полученныхз данных
            self.process_rawq()
        return self.read_very_lazy()

    def sock_avail(self):
        #проверяет доступность соединения (магия)
        return select.select([self.sock], [], [], 0) == ([self.sock], [], [])

    def fill_rawq(self):
        """
        если очередь строк пустая ,то принимаем новую порцию информации от сервера

        """
        if self.irawq >= len(self.rawq):
            self.rawq = ''
            self.irawq = 0
            # The buffer size should be fairly small so as to avoid quadratic
        # behavior in process_rawq() above
        #собственно прием данных
        buf = self.sock.recv(50)
        #self.msg("recv %r", buf)
        # если данных нет, пишем ,что конец файла
        self.eof = (not buf)
        #приписываем буфер в конец очереди
        self.rawq = self.rawq + buf

    def process_rawq(self):
        # Эта функция разбирает уже полученную информацию по символам и кидает в буфер принятых данных
        buf = ['', '']
        try:
            while self.rawq:
                c = self.rawq_getchar()
                #пихаем в буфер по одному символу
                buf[self.sb] += c
        except EOFError:  # raised by self.rawq_getchar()
            self.iacseq = ''  # Reset on EOF
            self.sb = 0
            pass
        #и добавляем строку из буфера к сохраненной ифнормации
        self.cookedq += buf[0]
        #self.sbdataq = self.sbdataq + buf[1]

    def read_very_lazy(self):
        """
        Возвращает строку из сохраненной очереди, полученных от сервера данных
        Вызывает исключение, если строка в очереди пуста. или достигнут конец сообщения
        вернет '' если никакой сохраненной в очереди информации нет
        """
        #кидаем в буфер информацию, сохраненную ранеее
        buf = self.cookedq
        #очищаем полученные данные
        self.cookedq = ''
        if not buf and self.eof and not self.rawq:
            raise EOFError,'telnet connection closed'
        #и возвращаем содержимое буфера
        return buf

    def rawq_getchar(self):
        """
        Получаем по символу из очереди данных

        """
        #проверяем не пустая ли очередь
        if not self.rawq:
            #если надо - получаем новый блок данных
            self.fill_rawq()
            if self.eof:
                raise EOFError
        # берем новый символ
        c = self.rawq[self.irawq]
        #увеличиваем счетчик внутри очереди
        self.irawq += 1
        # если счетчик стал больше, чем длина очереди ,то обнуляем
        if self.irawq >= len(self.rawq):
            self.rawq = ''
            self.irawq = 0
        # возвращаем символ
        return c


def test():
    """Test program for telnetlib.

    Usage: python telnetlib.py [-d] ... [host [port]]

    Default host is localhost; default port is 23.

    """
    debuglevel = 0
    while sys.argv[1:] and sys.argv[1] == '-d':
        debuglevel = debuglevel+1
        del sys.argv[1]
    host = 'pop.mail.ru'

    port = 110

    tn = Telnet()
    #tn.set_debuglevel(debuglevel)
    tn.open(host, port, timeout=0.5)
    tn.interact()
    tn.close()

if __name__ == '__main__':
    test()
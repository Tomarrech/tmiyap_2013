__author__ = 'XxX'
#coding: utf-8
import socket
import sys

#   open http://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83
#   open http://www.google.com/search?q=qwerty

# присваем переменной сок сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# открывакм соединение на порт 3000
sock.connect(('127.0.0.1', 6969))
# переменная отвечающая за статус соед-я
working = True
# пока есть сое-е,
while working:
    # получаем инфу от сервера
    data = sock.recv(1024)
    # если нет ответа, то переменную working делаем ложь
    if not data:
        working = False
    # если принятая команда ок
    elif data[:3] == "+OK":
        # то пишем, что прием окончен, передана вся инфа
        print "Прием окончен."
        # когда закончена передача, ожидаем комагды от пользователя,
        while True:
            # ожидаем ввод (просим поль-ля ввести данные)
            cmd = raw_input("Введите команду: \n\topen %site% - открыть сайт,\n\texit - завершить работу сервера\n:")
            # если подь-ль ввел search
            if cmd[:4] == 'open':
                # то отпавляем запрос серверу
                sock.send(cmd)
                break
            # если команда выход
            elif cmd == 'exit':
                sock.send(cmd)
                working = False
                # закрываем соед-е
                sock.close()
                sys.exit(102)
            # если команда не распознана, то продолжаем (начинаем цикл заново)
            else:
                continue
    # иначе печатаем полученную инфу, если не ок и не пустое
    else:
    # печатаем полученное
        print data
print "Работа завершена"
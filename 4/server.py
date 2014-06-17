__author__ = 'Nastya'
#coding: utf-8
import socket
import sys
import urllib2
import lxml.html
import re

# эти строчки использ-ся для отображения кодировки
reload(sys)
sys.setdefaultencoding(sys.stdout.encoding or sys.stderr.encoding)


 # ф-я для поиска
def open_site_for_search(url):

    # создаем ф-ю для открытия адреса
    opener = urllib2.build_opener()
    # добавляем заголовок, чтобы этот запрос распознали как запрос браузера
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.12 (KHTML, like Gecko)'
                                       'Chrome/26.0.1410.43 Safari/535.12')]
    #открываем адрес и получаем код страницы
    html = opener.open(url).read()
    #print html
    # создаем lxml-структуру
    doc = lxml.html.document_fromstring(html)

    # по xpath вытягиваем все нужные  теги, где указаны ссылки на рез-ты
    lists = doc.xpath('.//*/li/.//a')
    print lists

    # создаем пустой словарь для рез-ов
    result = {}
    # в нумерованном списке из найденных тегов
    for num, elem in enumerate(lists):
        print num, elem
        try:
            print "содержимое: ", elem.text
            if None != elem.text:
                result[num+1] = elem.text
        except:
            result[num+1] = elem
            pass

    return result


# ф-яобработки команд клиента
def parse_data(data):
    print data

    # если команда поиск, то
    if data[0:4] == "open":
        print "открываем сайт - %s" % data[5:]
        # то вызываем фу-ю поиска со строкой для поиска в кач-ве агумента
        if re.match(r'http[.\D]*[\w]+', data[5:]):
            print "да. пришла ссылка: %s" % data[5:]
            results = open_site_for_search(data[5:])
            return results
    elif data[0:4] == "exit":
        sys.exit("closed by client")
    else:
        return "Unknown type of command"

# создаем сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# вешаем его на порт 6969
sock.bind(('', 6969))
# слушаем входящие соединения до 10 штук
sock.listen(10)
while True:
    # записываем в переменную инфу о соединкении и адресс, откуда пришло соед-е
    print "Ожидаю соединения..."
    conn, addr = sock.accept()
    print "Клиент с адресом:", addr
    # отсылаем приветственную строку клиету
    conn.send("Это сервер для поиска списков (О__о) на сатйах. Введите адрес сайта для поиска в формате "
              "open http://www.some-site.com.")
    # отсылвем команду - подтверждение клиенту о конце передачи
    conn.send("+OK")
    # устанавливаем значение переменной истины
    connection = True
    # в цикле
    while connection:
        # записываем полученную информацию
        data = conn.recv(1024)  # то, что посылает клиент
        # если ничего не получено
        if not data:
            break
        # если команда клоуз
        if data[0:5] == "close":
            conn.close()
            connection = False
            break
        # если в дата есть, то запускаем функцию обрработки инфы
        answer = parse_data(data)
        #print answer
        # пытаемся отправить ответ как словарь
        try:
            # если ответ есть
            if answer:
                # то в цикле для каждого номера и ссылки
                for num, item in answer.items():
                    # создаем буфер, сост. из номера, описания и ссылки
                    buf = str(num)+') ' + item + "\r\n"
                    # отправляем буфур клиенту
                    conn.send(buf)
            conn.send("+OK")
        # если не получилось,просто отправляем, что есть
        except:
            print "some exception"
            conn.send(answer+'\n')
            conn.send("+OK")
        # начинаем цикл ожидания подключения заново
        continue
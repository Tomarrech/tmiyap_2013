#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys
from email.parser import Parser
from email import message_from_string
import re
import os
import base64


CR = '\r'
LF = '\n'
CRLF = CR+LF

host = "pop.mail.ru"
port = 110

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mail_body = None


def request(command):
    sock.send(command + CRLF)
    answer = sock.recv(1024)
    #print answer
    return answer


def conn():
    sock.connect((host, port))
    global mail_body
    mail_body = sock.makefile('rb')
    res = sock.recv(1024)
    if res == "+OK" + CRLF:
        return True
    else:
        return False


def auth(login, password):
    if request("USER " + login)[:3] == "+OK" and request("PASS " + password)[:3] == "+OK":
        return True
    else:
        return False


def del_mess_by_id(id):
    answer = request("dele " + str(id))
    if answer[0] == "+":
        print "сообщение с id %s удалено успешно" % id
    else:
        print "ошибка в процессе удаления"


def repeal():
    answer = request("RSET")
    print answer
    if answer[0] == "+":
        print "операция упешно отменена"


def get_list():
    list_res = request("LIST")
    print "Возможно, команду следует повторить несколько раз, т.к. сервер не всегда отвечает сразу полностью."
    try:
        if list_res[:3] == "+OK":
            line = list_res.split("\r\n")
            print "Всего сообщений %s" % line[0].split(" ")[1]
            for mess in line[1:]:
                num, size = mess.split(" ")
                print "Сообщение c ID %s имеет размер %s байт" % (num, size)
    except:
        pass


def save_mess():
    stat_result = request("stat")

    if stat_result[0] == "+":
        num = stat_result.split(" ")[1]
        for n in range(int(num)+1):
            answer = request("RETR " + str(n))
            if answer[0] == "+":
                message = ''
                while True:
                    line = mail_body.readline()
                    if line != '.' + CRLF:
                        message += line
                    else:
                        break

                author = re.findall("Return-path: <(.+)>", message)
                if author:
                    path = "./inbox/" + str(author[0]) + "/"
                else:
                    path = "./inbox/unnamed/"

                if not os.path.exists(path):
                    os.mkdir(path)
                out = open(path + str(n) + ".txt", 'w')
                out.write(message)
                out.close()


def get_mess_by_id(number_message, cod=None):
    reload(sys)
    sys.setdefaultencoding(sys.stdout.encoding or sys.stderr.encoding)

    answer = request("RETR " + str(number_message))
    if answer[:3] == "+OK":
        message = ''

        while True:
            line = mail_body.readline()
            if line != '.' + CRLF:
                message += line
            else:
                break
        try:
            headers = Parser().parsestr(message)
            print "От:", headers['from']
            print "Тема:", headers['subject']

            b = message_from_string(message)
            if b.is_multipart():
                for payload in b.get_payload():
                    if not cod:
                        print payload.get_payload()
                    elif cod == 'base64':
                        print base64.decodestring(payload.get_payload())
                    elif cod == '64+koi8':
                        print base64.decodestring(payload.get_payload()).decode('koi8-r')
                    elif cod == 'cp1251':
                        print payload.get_payload().decode('cp1251')
                    elif cod == 'utf8':
                        print payload.get_payload().decode('utf8')
            else:
                if not cod:
                    print b.get_payload()
                elif cod == 'base64':
                    print base64.decodestring(b.get_payload())
                elif cod == '64+koi8':
                    print base64.decodestring(b.get_payload()).decode('koi8-r')
                elif cod == 'cp1251':
                    print b.get_payload().decode('cp1251')
                elif cod == 'utf8':
                    print b.get_payload().decode('utf8')
        except:
            print u"Ошибка кодировки. Вывод 'как есть':\n"
            b = message_from_string(message)
            if b.is_multipart():
                for payload in b.get_payload():
                    print payload.get_payload()
            else:
                print b.get_payload()
        return True
    return False


def pop_quit():
    if request("QUIT")[:3] == "+OK":
        request("QUIT")
        sock.close()
        return True
    else:
        sock.close()
        return False
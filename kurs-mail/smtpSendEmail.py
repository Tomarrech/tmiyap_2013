#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from email.base64mime import encode as encode_base64
import base64
import hmac


host = "smtp.mail.ru"
port = 25

CR = '\r'
LF = '\n'
CRLF = CR+LF

message_max_size = 0
auth_method = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def s_conn():
    sock.connect((host, port))
    if sock.recv(1024)[:3] == "220":
        return True
    return False


def request(command):
    sock.send(command + CRLF)
    return sock.recv(1024)


def send_letter(author, responders):
    print author
    print responders
    if request("MAIL FROM: <" + author + ">")[0] == '2':
        print "Отправитель указан как '%s'" % author
        if responders:
            for resp in responders:
                if request("RCPT TO:<" + resp + ">")[0] == '2':
                    print "Адресат '%s' успешно добавлен\n" % resp
                else:
                    print "Ошибка при добавлении адресата '%s'. Продолжаем без него.\n" % resp

            mail_body = raw_input("Введите текст сообщения...\n$>:")
            if request("DATA")[0] == '3':
                if request(mail_body + CRLF + "." + CRLF)[0] == '2':
                    print "Сообщение было успешно отправлено!\n"
                else:
                    print "Сообщение не было отправлено сервером\n"
            else:
                print "Запрос DATA не прошёл.\n"
    else:
        print "Не удалось указать адрес отправителя, проверьте данные\n"


def login_auth(user, password):
    login = encode_base64(user, eol="")         #aXNzYWhhckBpbmJveC5ydQ==
    password = encode_base64(password, eol="")  #Mjh6UjVRMXRK
    if request("AUTH LOGIN")[0] == '3' and request(login)[0] == '3' and request(password)[0] == '2':
        return True
    return False


def plain_auth(user, password):
    if request("AUTH PLAIN " + encode_base64("\0%s\0%s" % (user, password), eol=""))[0] == "2":
        return True
    return False


def md5_auth(user, password):
    res = request("AUTH CRAM-MD5")
    if res[0] != "5":
        challenge = res[4:]
        challenge = base64.decodestring(challenge)
        response = user + " " + hmac.HMAC(password, challenge).hexdigest()
        if request(encode_base64(response, eol=""))[0] == '2':
            return True
    return False


def send_ehlo():
    answer = request("EHLO smtp.client")
    if answer[0] == "2":
        answer = answer.split('\r\n')
        global message_max_size
        message_max_size = int(answer[1][9:])
        global auth_method
        auth_method = answer[3][4:].split()
        return True
    else:
        return False


def s_auth(user, password):
    if send_ehlo():
        auth_list = ["LOGIN", "PLAIN", "CRAM-MD5", ]
        workable = None
        for method in auth_list:
            if method in auth_method:
                workable = method
                break

        if workable == "LOGIN":
            return login_auth(user, password)
        elif workable == "PLAIN":
            return plain_auth(user, password)
        elif workable == "CRAM-MD5":
            return md5_auth(user, password)
        return True
    else:
        return False


def smtp_quit():
    if request('QUIT')[0] == '2':
        sock.close()
        return True
    else:
        sock.close()
        return False
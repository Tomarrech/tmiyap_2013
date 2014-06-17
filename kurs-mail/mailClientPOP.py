#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import socket


CR = '\r'
LF = '\n'
CRLF = CR+LF

host = "pop.mail.ru"
port = 110

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
file


def conn():
    sock.connect((host, port))
    global file
    file = sock.makefile('rb')
    res = sock.recv(1024)
    if res == "+OK" + CRLF:
        return True
    else:
        return False


def send(command):
    sock.send(command + CRLF)
    return sock.recv(1024)


def auth(login, password):
    if send("USER " + login)[:3] == "+OK" and send("PASS " + password)[:3] == "+OK":
        return True
    else:
        return False


def list_cmd(number_message=None):

    if not number_message:
        messages_count = 0
        octets_count = 0
        numbers_and_octets_messages = []
        result = send("LIST")
        if result[:3] == "+OK":
            result = result.split("\r\n")
            line1 = result[0].split(" ")
            messages_count = int(line1[1])
            octets_count = int(line1[3][1:])
            for i in range(1, messages_count + 1):
                number_octets_message = result[i].split(" ")
                try:
                    numbers_and_octets_messages.append((int(number_octets_message[0]), int(number_octets_message[1])))
                except:
                    break
            return (messages_count, octets_count, numbers_and_octets_messages)
        else:
            return False

    else:
        if isinstance(number_message, int):
            result = send("LIST")
            if result[:3] == "+OK":
                result = result.split(" ")
                return int(result[1]), int(result[3][1:])
            else:
                return False
        else:
            return False


def retr(number_message):
    retr_res = send("RETR " + str(number_message))
    if retr_res[:3] == "+OK":
        message = ''
        while True:
            line = file.readline()
            if line != '.' + CRLF:
                message += line
            else:
                break
        return message
    return False


def rset():
    if send("RSET")[:3] == "+OK":
        return True
    else:
        return False


def stat():
    stat_res = send("STAT")
    if stat_res[:3] == "+OK":
        stat_res = stat_res.split(' ')
        return (int(stat_res[1]), int(stat_res[2][:-2]))
    else:
        return False


def quit():
    if send("QUIT")[:3] == "+OK":
        sock.close()
        return True
    else:
        sock.close()
        return False





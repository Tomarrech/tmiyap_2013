__author__ = '700ghz'
import socket
from email.base64mime import encode as encode_base64
import base64
import hmac
import re
import os

CR = '\r'
LF = '\n'
CRLF = CR+LF

host = "smtp.mail.ru"
port = 25

message_max_size = 0
authlist = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def conn():
    sock.connect((host, port))
    if sock.recv(1024)[0] == "2":
        return True
    return False


def send(command):
    sock.send(command + CRLF)
    return sock.recv(1024)


def ehlo():
    result = send("EHLO danilov.client.program")
    if result[0] == "2":
        result = result.split('\r\n')
        global message_max_size
        max_size_message_octets = int(result[1][9:])
        global authlist
        authlist = result[3][4:].split()
        return True
    return False


def auth_plain(login, password):
    if send("AUTH PLAIN " + encode_base64("\0%s\0%s" % (login, password), eol=""))[0] == "2":
        return True
    return False


def auth_login(user, password):
    login_base64 = encode_base64(user, eol="")
    password_base64 = encode_base64(password, eol="")
    if send("AUTH LOGIN")[0] == '3' and send(login_base64)[0] == '3' and send(password_base64)[0] == '2':
        return True
    return False


def auth_cram_md5(user, password):
    res = send("AUTH CRAM-MD5")
    if res[0] != "5":
        challenge = res[4:]
        challenge = base64.decodestring(challenge)
        response = user + " " + hmac.HMAC(password, challenge).hexdigest()
        if send(encode_base64(response, eol=""))[0] == '2':
            return True
    return False


def mail_from(MailFrom):
    if send("MAIL FROM: <" + MailFrom + ">")[0] == '2':
        return True
    return False


def rcpt_to(MailsTo):
    status_emails = []
    if isinstance(MailsTo, list):
        for i in range(0, len(MailsTo)):
            if send("RCPT TO:<" + MailsTo[i] + ">")[0] == '2':
                status_emails.append((MailsTo[i], True))
            else:
                status_emails.append((MailsTo[i], False))
        return status_emails

    elif isinstance(MailsTo, str):
        if send("RCPT TO:<" + MailsTo + ">")[0] == '2':
            return True
        else:
            return False
    else:
        return False


def data(text_msg):
    res1 = send("DATA")
    if res1[0] == '3':
        res2 = send(text_msg + CRLF + "." + CRLF)
        if res2[0] == '2':
            return True
    return False


def login(user, password):
    preferred_auths = ["LOGIN", "PLAIN", "CRAM-MD5", ]
    authmethod = None
    for method in preferred_auths:
        if method in authlist:
            authmethod = method
            break
    if authmethod == "LOGIN":
        return auth_login(user, password)
    elif authmethod == "PLAIN":
        return auth_plain(user, password)
    elif authmethod == "CRAM-MD5":
        return auth_cram_md5(user, password)


def rset():
    if send('RSET')[0] == '2':
        return True
    return False


def noop():
    if send('RSET')[0] == '2':
        return True
    return False


def quit():
    if send('QUIT')[0] == '2':
        sock.close()
        return True
    return False



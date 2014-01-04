#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'issahar'
from pop3GetEmail import *
from smtpSendEmail import *
import sys

reload(sys)
sys.setdefaultencoding(sys.stdout.encoding or sys.stderr.encoding)

user = ''
password = ''


def get_user_auth():
    global user, password
    user = raw_input("\tДля дальнейшей работы требуются данные.\n\tВведите имя пользователя:\n$>:")
    password = raw_input("\n\tВведите пароль:\n$>:")
    print user, password


def work_with_pop3():
    while True:
        cmd = raw_input(u"Введите команду для сервера:\n\tsave -сохранить письма из ящика\n\t"
                        u"get Id -получить сообщение по его id\n\tlist - получить размер писем\n\t"
                        u"del Id - удалить письмо по его id\n\trepeal - отменить последнюю операцию\n\t"
                        u"main - возврат в меню\n~")

        if cmd == "save":
            save_mess()
        elif cmd[:3] == "get":
            if cmd[4:]:
                print u"Получение письма № %s" % cmd[4:]
                cod = raw_input(u"Указать кодировку?[base64/utf8/cp1251/koi8/64+koi]\n~")
                get_mess_by_id(int(cmd[4:]), cod)
            else:
                print u"Пустое значение"

        elif cmd == "list":
            get_list()
        elif cmd[:3] == "del":
            if cmd[4:]:
                print u"Удаление письма c id %s" % cmd[4:]
                if raw_input("вы уверены? [д/н]") != 'n' or 'н':
                    del_mess_by_id(int(cmd[4:]))
        elif cmd == "repeal":
            repeal()
        elif cmd == "main":
            print "Возврат в главное меню"
            return


def work_with_smtp():
    while True:
        cmd = raw_input(u"Введите команду для сервера:\n\tsend - отправить письмо\n\t"
                        u"main - возврат в меню\n~")

        if cmd == "send":
            responders = []
            new = raw_input("Введите адресатов через ','\n$>:").split(",")
            for each in new:
                responders.append(each.strip())
            send_letter(user, responders)
        elif cmd == "main":
            print "Возврат в главное меню"
            return

if __name__ == "__main__":

    get_user_auth()

    if conn():
        if auth(user, password):
            print "POP login successful"
        else:
            sys.exit(u"Неверные данные авторизации на pop сервере")
    else:
        sys.exit(u"Нет соединения с pop ссервером")

    if s_conn():
        if s_auth(user, password):
            print "SMTP login successful"
        else:
            sys.exit(u"Неверные данные авторизации на SMTP сервере")
    else:
        sys.exit(u"Нет соединения с SMTP ссервером")
    try:
        while True:
            cmd = raw_input(u"Введите команду:\n\tpop - для получения писем\n\tsmtp - для отправки писем.\n\t"
                            u"exit - для выхода\n~")
            if cmd == "pop":
                work_with_pop3()
            elif cmd == "smtp":
                work_with_smtp()
            elif cmd == "exit":
                sys.exit("Выход по требованию.")
            else:
                print u"Некорректная команда"
    except EOFError:
        print u"\nЧто-то пошло не так. Выход."
        sys.exit(666)
    except KeyboardInterrupt:
        print u"\nОперация прервана пользователем."
        sys.exit(0)
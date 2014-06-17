# -*- coding: utf-8 -*-
__author__ = '700ghz'

import mailClientPOP
import mailClientSMTP
import re
import os
import sys

reload(sys)
sys.setdefaultencoding(sys.stdout.encoding or sys.stderr.encoding)

user = ''
password = ''


def get_user_pass():
    global user, password
    user = raw_input("User:")
    password = raw_input("Pass:")
    #password = getpass.getpass("Pass:")


def save_inbox_message(inbox_message, number):
    sender_re = re.compile("Return-path: <(.+)>")
    sender_mail = re.findall(sender_re, inbox_message)
    if sender_mail:
        folder_name = "inbox\\" + sender_mail[0] + "\\"
    else:
        folder_name = "inbox\\other\\"

    if folder_name:
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

    message_file = open(folder_name + str(number) + ".txt", 'w')
    message_file.write(inbox_message)
    message_file.close()


def get_and_save_all_messages():
    stat_result = mailClientPOP.stat()
    if stat_result:
        messages_cnt = int(stat_result[0])
        if messages_cnt:
            for message_numb in range(1, messages_cnt + 1):
                message_text = mailClientPOP.retr(message_numb)
                if message_text:
                    save_inbox_message(message_text, message_numb)
            return True
    return False


def main_menu():
    global get_messages
    if raw_input(u"Выберите режим работы:\n\t1 Получение сообщений \n\t2 Отправка сообщений\n>>") == "1":
        get_messages_mode_menu()
    else:
        send_messages_mode_menu()


def get_messages_mode_menu():
    if not mailClientPOP.conn():
        print u"Не удалось выполнить подключение!"
        return

    if not mailClientPOP.auth(user, password):
        print u"Не удалось выполнить авторизацию!"
        return

    stat_res = mailClientPOP.stat()
    print u"Количество сообщений на почте: " + str(stat_res[0]) + u". Общий размер сообщений: " + str(stat_res[1]) + \
          u" байт."
    while True:
        cmd = raw_input(u"\n\t1 Получить и сохранить все письма\n\t2 Получить текст письма по номеру"
                        u"\n\t3 Получить размеры писем\n\t4 Получить размер письма по номеру"
                        u"\n\t5 Выход и возврат в главное меню\n>>")
        if cmd == "1":
            if get_and_save_all_messages():
                print u"Получение писем завершено."
            else:
                print u"Не удалось получить письма."

        elif cmd == "2":
            text_message = mailClientPOP.retr(int(raw_input(u"Номер сообщения:")))
            if text_message:
                print text_message
            else:
                print u"Не удалось получить текст сообщения"

        elif cmd == "3":
            res = mailClientPOP.list_cmd()
            if res:
                (messages_count, octets_count, numbers_and_octets_messages) = res
                if (messages_count, octets_count, numbers_and_octets_messages):
                    for i in range(0, len(numbers_and_octets_messages)):
                        print u"№" + str(numbers_and_octets_messages[i][0]) + " " + str(numbers_and_octets_messages[i][1]) + u" байт"
            else:
                print "Не удалось получить список писем!"

        elif cmd == "4":
            (numb, size) = mailClientPOP.list_cmd(int(raw_input(u"Номер сообщения:")))
            print u"Размер сообщения:" + str(size)

        elif cmd == "5":
            mailClientPOP.quit()
            main_menu()


def send_messages_mode_menu():

    if not mailClientSMTP.conn():
        print u"Не удалось выполнить подключение!"
        return

    if not mailClientSMTP.ehlo():
        print u"Не удалось выполнить EHLO"
        mailClientSMTP.quit()
        return

    if not mailClientSMTP.login(user, password):
        print u"Не удалось выполнить авторизацию!"
        mailClientSMTP.quit()
        return

    if not mailClientSMTP.mail_from(user):
        print u"Не удалось указать адрес отправителя"
        return

    rcpt_res = []

    while True:
        rcpt_mail = '1'
        rcpt_mail_list = []

        print u"Введите e-mail адреса назначения.\n\tДля окончания ввода оставьте поле пустым."
        rcpt_mail = raw_input(u">>")
        while rcpt_mail:
            rcpt_mail_list.append(rcpt_mail)
            rcpt_mail = raw_input(u">>")

        if rcpt_mail_list:
            rcpt_res = mailClientSMTP.rcpt_to(rcpt_mail_list)
            break
        else:
            print u"E-mail адреса назначения не введены"

    for mail, res in rcpt_res:
        if res:
            print mail + " OK"
        else:
            print mail + " FAIL"

    text_message = ''
    if raw_input(u"Способ получения текста письма для отправки: \n\t1 из файла send.txt \n\t2 вставить текст в косоль\n") == "1":
        text_mail_file = open("send.txt", 'r')
        text_message = text_mail_file.read()
    else:
        text_message = raw_input(u"Введите текст сообщения:\n>>")

    if mailClientSMTP.data(text_message):
        print u"Письмо успешно отправлено\n"
    else:
        print u"Не удалось отправить письмо\n"

    mailClientSMTP.quit()
    return


get_user_pass()
main_menu()
#coding: utf-8
from bs4 import BeautifulSoup
import time

import requests
prime_link = 'http://10.10.' #%(thrd)s.%(fourth)s' % {'thrd': str(third_node), 'fourth': str(fourth_node)}
#print prime_link
#todo: if timeout of request more then 5s next ip


def try_ip(link):
    try:
        print link
        requests.get(link, timeout=0.2)
        print 'exist!'
    except requests.exceptions.Timeout:
        print "Connection TimeOut."


def check_third_node(link):
    for third in range(256):
        new_link = link+str(third)+'.'
        check_fourth_node(new_link)


def check_fourth_node(link):
    for fourth in range(256):
        new_link = link+str(fourth)
        try_ip(new_link)
        time.sleep(1)



check_third_node(prime_link)
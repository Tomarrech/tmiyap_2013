#coding:utf-8
from io import StringIO

__author__ = 'issahar'

import urllib, urllib2
import lxml.html
from lxml.html import HtmlElement
import cookielib
import re
email, password = open('pass.key', 'r').readlines()

#s = requests.Session()

headers = {
    'Origin': 'http://barbars.ru',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'http://barbars.ru/login'}

data = {
    'act': 'login',
    'origin': 'https://m.vk.com',
    'ip_h': '8f4cb74c1fdcbd2b64',
    'role': 'pda',
    'utf8': '1',
    'email': email,
    'pass': password}

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
data_to_req = data
param_auth = urllib.urlencode(data_to_req)
req_auth = urllib2.Request("https://login.vk.com/", param_auth, headers)
page_auth = urllib2.urlopen(req_auth).read()

songs = {'artists': [], 'tracks': [], 'links': []}
search = 'Xandria'
html = urllib2.urlopen("https://vk.com/audio").read()


links = re.findall(r'https.*.mp3', html)
print links
reg = re.compile(ur">(\.*?)</a></b>", re.IGNORECASE)
titles = re.findall(reg, html)
print titles

#html = lxml.html.document_fromstring(page)
#print html.text_content()

#print root.forms[0].name




#print page_l.text
#post по музыке +
# парсер 3мя способоами  (re, lxml, lxml-xpath)


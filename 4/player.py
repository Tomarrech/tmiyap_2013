#coding:utf-8
__author__ = 'issahar'
import requests
email, password = open('pass.key', 'r').readlines()

s = requests.Session()

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


resp = s.post("https://login.vk.com/", data)
print resp.text
resp = s.get('https://vk.com/audio')
page = s.post('https://vk.com/audio?q=xandria')
print page.text
#coding: utf-8
__author__ = 'issahar'
import os
from os import path
from classes import Good, Order
import re
import json
from datetime import datetime

STORAGE_ROOT = './files'
SETTINGS_PATH = STORAGE_ROOT + '/last_id'


def create_id():
    f = open(SETTINGS_PATH, 'w')
    json.dump({'last_id': 0}, f)
    f.close()


def save_id(last_id):
    f = open(SETTINGS_PATH, 'w')
    json.dump(last_id, f)
    f.close()

if not os.path.exists(SETTINGS_PATH):
        create_id()
# Загружаем настройки
settings = json.load(open(SETTINGS_PATH, 'r'))


def dict_to_good(dict):
    new_good = Good(dict['name'], dict['country'], dict['price'],
                    datetime.strptime(dict['production_date'], '%d.%m.%Y').strftime('%d.%m.%Y'))
    return new_good


def dict_to_goods(dictionary):
    goods = []
    for good in dictionary:
        new_good = Good(good['name'], good['country'], good['price'],
                        datetime.strptime(good['production_date'], '%d.%m.%Y').strftime('%d.%m.%Y'))
        goods.append(new_good)
    return goods


def extract_params(command):
    res = re.findall(r'\s+-(\w+)\s+(\S+)', command)
    params = {}
    for key, value in res:
        params[key] = value
    return params


def create_g_o(c, params):
    if c[1] == 'G':
        #теперь создадим объект класса Good
        temp = Good(params['name'], params['country'], params['cost'], params['date'])
        type = 'good'
        #и сразу в файл его, в файл.
    elif c[1] == 'O':
        temp = Order(params['name'], params['country'], params['date'])
        temp.price_of_order = 0
        type = 'order'
    else:
        print 'fuck('
        return None
    new_id = settings['last_id'] + 1
    print new_id
    obj = temp.to_dict()
    settings['last_id'] = new_id
    save_id(settings)
    full_path = "%s\%s-%s_%s_%d.json" % (STORAGE_ROOT, type, obj['name'], obj['country'], new_id)
    wfile = open(full_path, 'w')
    json.dump(obj, wfile)
    wfile.close()


def add_g_to_o(params):
    print "adding"
    g_path = STORAGE_ROOT+'/good-'+params['name']+'_'+params['country']+'_'+params['g_id']+'.json'
    t_good = json.load(open(g_path, 'r'))
    t_good = dict_to_good(t_good)
    print t_good

    o_path = STORAGE_ROOT+'/order-'+params['to']+'_'+params['ord_c']+'_'+params['o_id']+'.json'
    t_order = json.load(open(o_path, 'r'))
    #print t_good, t_order
    new_order = Order(t_order['name'], t_order['country'], datetime.strptime(t_order['delivery_time'], '%d.%m.%Y').strftime('%d.%m.%Y'))
    new_order.goods = dict_to_goods(t_order['goods'])
    new_order.price_of_order = int(t_order['price']) + int(t_good.good_price)
    new_order.goods.append(t_good)
    obj = new_order.to_dict()
    full_path = "%s\%s-%s_%s_%s.json" % (STORAGE_ROOT, 'order', new_order.order_name, new_order.delivery_country,
                                         params['o_id'])
    wfile = open(full_path, 'w')
    json.dump(obj, wfile)
    wfile.close()


def read_file(params):
    print "reading"
    t_path = '%s/%s-%s_%s_%d.json' % (STORAGE_ROOT, params['type'], params['name'], params['country'], params['id'])
    print t_path
    try:
        obj = json.load(open(t_path, 'r'))
        for v in obj:
            print v
    except:
        print "can't find such file..."
        return None


def select_order(params):
    files = []

    for fille_name in os.listdir(STORAGE_ROOT):
        if fille_name.find('order') == -1:
            continue
        elif 'name' in params and 'country' in params:
            pattern = '^order.' + params['name'] + '.' + params['country'] + '.[1-9]+'
            reg = re.compile(pattern)
            if reg.match(fille_name):
                files.append(fille_name)
        elif params.get('name'):
            if fille_name.find(params['name']) != -1:
                files.append(fille_name)
        elif params.get('country'):
            if fille_name.find(params['country']) != -1:
                files.append(fille_name)

    #вхождение ключа в словарь
    #print files
    for fille_name in files:
        t_path = STORAGE_ROOT+'/'+fille_name
        t_order = json.load(open(t_path, 'r'))
        # if key in dict
        if params.get('price'):
            if int(t_order['price']) == int(params['price']):
                #print "I found file %s/%s" % (STORAGE_ROOT, f)
                return t_order
            else:
                print "Erererer"
                return None
        else:
            return t_order


while True:
    cmd = raw_input("Write your command: ")
    par_dict = extract_params(cmd)
    print 'parsed: ', par_dict

    if cmd == 'q':
        print "go off! bye!"
        break
    # cG -name AAA -country BBB -cost 123 -date 10.11.2013
    # cO -name Avan -country USA -date 11.12.2013
    elif cmd[0] == 'c':
        print 'create Good or Order'
        create_g_o(cmd, par_dict)
    # a -name good1 -country Africa -g_id 3 -to Avan -ord_c USA -o_id 5
    elif cmd[0] == 'a':
        add_g_to_o(par_dict)
        print "good", par_dict['name'], 'added to Order', par_dict['to']
    # r -type good -name Avan -country USA -id 7
    # r -name Avan -country USA -price 123
    elif cmd[0] == 'r':
        #read_file(par_dict)
        keys = par_dict
        print select_order(keys)
        #todo: select orders (keys[name, country, price...],)
    else:
        print 'go` off, stupid!'

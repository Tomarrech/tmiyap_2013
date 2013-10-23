import json
from classes import Order, Good
from lxml import etree
from lxml.builder import E
from lxml.etree import tostring
from datetime import datetime


#def good_to_dict(obj_good):
#    if not isinstance(obj_good, Good):
#        raise TypeError("It's not a Good..")
#    return {'name': obj_good.good_name, 'country': obj_good.good_country, 'price': obj_good.good_price}


#def order_to_dict(obj_order):
#    if not isinstance(obj_order, Order):
#        raise TypeError("It's not a Good..")
#    return {'name': obj_order.order_name, 'country': obj_order.delivery_country,
#            'price': obj_order.price_of_order, 'goods': [Good.to_dict(good) for good in obj_order.goods]}


def export_dict_to_json(dictionary):
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
    with open('basic.json', mode='w') as f:
        json.dump(dictionary, f, default=dthandler, indent=3, sort_keys=True)


def load_json_file(file_name):
    with open(file_name, 'r') as f:
        entry = json.load(f)
    return entry


def dict_to_good(dictionary):
    goods = []
    for good in dictionary:
        new_good = Good(good['name'], good['country'], good['price'],
                        datetime.strptime(good['production_date'], '%Y-%m-%dT%H:%M:%S'))
        goods.append(new_good)
    return goods


def dict_to_order(order):
    new_order = Order(order['name'], order['country'], order['delivery_time'])
    new_order.price_of_order = order['price']
    new_order.goods = dict_to_good(order['goods'])
    return new_order

#todo: one function for each order. #done: only orders in json.


def load_xml_file(file_name):
    with open(file_name, 'r') as f:
        content = f.read()
    return etree.fromstring(content)


def from_xml_to_order(root):
    order = {
        'order_name': root.attrib['order_name'],
        'order_price': root.attrib['order_price'],
        'order_country': root.attrib['order_country'],
        'delivery_time': root.attrib['delivery_time'],
        'goods': [{
                      'good_country': el.attrib['good_country'],
                      'good_name': el.attrib['good_name'],
                      'good_price': el.attrib['good_price'],
                      'good_production_date': el.attrib['good_production_date']
                  } for el in root.find('goods').iter('good')]
    }
    new_order = Order(order['order_name'], order['order_country'], datetime.strptime(order['delivery_time'],
                                                                                     '%Y-%m-%dT%H:%M:%S'))
    new_order.price_of_order = order['order_price']
    new_order.goods = order['goods']
    return new_order


def export_order_to_xml(order):
    order_xml = tostring(
        E.order(
            E.goods(*[E.good(
                good_name=good.good_name,
                good_country=good.good_country,
                good_price=str(good.good_price),
                good_production_date=good.production_date.isoformat()
            ) for good in order.goods]
            ),
            order_name=order.order_name,
            order_country=order.delivery_country,
            delivery_time=order.delivery_time.isoformat(),
            order_price=str(order.price_of_order)
        ),
        xml_declaration=True, encoding='UTF-8', pretty_print=True
    )
    xml_file = open('basic.xml', 'wb')
    xml_file.write(order_xml)
    xml_file.close()
    return order_xml


from classes import Order, Good
import my_filter
import my_sorting
import services
from datetime import datetime

good_1 = Good('shovel', 'Germany', 50000, datetime(2013, 12, 11))
good_2 = Good('steel', 'Italy', 25000, datetime(2013, 8, 4))
good_3 = Good('snow', 'Russia', 5000, datetime(2012, 10, 12))
good_4 = Good('kola', 'Nigeria', 9000, datetime(2012, 12, 14))
good_5 = Good('ananases', "USA", 80000, datetime(2012, 11, 15))
good_6 = Good('coffee', "Africa", 75600, datetime(2011, 10, 24))
good_7 = Good('meat', "Mexico", 35200, datetime(2013, 9, 8))
good_8 = Good('bread', "Japan", 3200, datetime(2013, 10, 6))
good_9 = Good('bad', "UK", 76580, datetime(2013, 11, 10))
all_goods = [good_1, good_2, good_3, good_4, good_5, good_6, good_7, good_8, good_9]

order_1 = Order("'Avangard'", 'USA', datetime(2013, 10, 24))
order_1.goods = [good_1, good_2, good_3]
order_1.price_of_order = Order.total_price(order_1)

order_2 = Order("'Azazaza'", 'RUS', datetime(2013, 11, 14))
order_2.goods = [good_4, good_5, good_6]
order_2.price_of_order = Order.total_price(order_2)

order_3 = Order("'Trust'", 'UK', datetime(2014, 2, 8))
order_3.goods = [good_7, good_8, good_9]
order_3.price_of_order = Order.total_price(order_3)
all_orders = [order_1, order_2, order_3]


new_dict = {'orders': []}
new_dict['orders'].append(Order.to_dict(order_1))
new_dict['orders'].append(Order.to_dict(order_2))
new_dict['orders'].append(Order.to_dict(order_3))
#order in dict export to json
services.export_dict_to_json(new_dict)

#read json from file
loaded_json = services.load_json_file('basic.json')
orders_from_json = []
# and make Order from each order in json
for order in loaded_json['orders']:
    orders_from_json.append(services.dict_to_order(order))

#XML. order -> xml format and write to file
order_in_xml = services.export_order_to_xml(order_1)
#load from file as xml
loaded_xml_root = services.load_xml_file('basic.xml')
#make Order from xml
order_4 = services.from_xml_to_order(loaded_xml_root)

'''
#def summ(a, b, c):
#    return a+b+c

#params = [3, 7, 9]

#def summ(a=0, b=0, c=0):
#    return a+b+c
#print summ(b=3, c=10)

#params = {'c': 10, 'b': 7}
#print sum(**params)

def summ(*args):
    sum = 0
    for arg in args:
        sum+=arg
    return sum

print summ(1,5,3,6)


def summ2(**kwargs):
    sum = 0
    for key in kwargs:
        sum+=kwargs[key]
    return sum

dict = {'a': 2, 'b': 4, 'c': 6}
print summ2(**dict)

print summ2()
'''

from classes import Order, Good
import filtration
from datetime import datetime
import random

good_1 = Good('shovel', 'Germany', 50000, datetime(2013, 12, 11))
good_2 = Good('steel', 'Italy', 25000, datetime(2013, 8, 4))
good_3 = Good('snow', 'Russia', 5000, datetime(2012, 10, 12))
good_4 = Good('kola', 'Nigeria', 9000, datetime(2012, 12, 14))
good_5 = Good('ananases', "USA", 80000, datetime(2012, 11, 15))
good_6 = Good('coffee', "Africa", 75600, datetime(2011, 10, 24))
good_7 = Good('meat', "Mexico", 35200, datetime(2013, 9, 8))
good_8 = Good('bread', "Japan", 3200, datetime(2013, 10, 6))
good_9 = Good('bad', "UK", 76580, datetime(2013, 11, 10))

order_1 = Order("'Avangard'", 'USA', datetime(2013, 10, 24))
order_1.goods = [good_1, good_2, good_3]
order_1.price_of_order = Order.total_price(order_1)

order_2 = Order("'Azazaza'", 'RUS', datetime(2013, 11, 14))
order_2.goods = [good_4, good_5, good_6]
order_2.price_of_order = Order.total_price(order_2)

order_3 = Order("'Trust'", 'UK', datetime(2014, 2, 8))
order_3.goods = [good_7, good_8, good_9]
order_3.price_of_order = Order.total_price(order_3)

order_4 = Order("'Just'", 'URUR', datetime(2013, 2, 18))
order_4.goods = [good_2, good_5, good_8]
order_4.price_of_order = Order.total_price(order_4)

all_orders = [order_1, order_2, order_3, order_4]

date_1 = datetime(2013, 9, 25)
date_2 = datetime(2013, 12, 31)

#print filtration.filter_order_by_time_interval(all_orders, date_1, date_2)

#print filtration.filter_goods_in_order_by_time_interval(order_3, date_1, date_2)

#print order_3.goods






list_1 = []
for a in range(0, 20):
    list_1.append(random.randint(-999, 999))

res = 1
for b in list_1:
    res = b*res
print res

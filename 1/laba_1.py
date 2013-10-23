__author__ = 'issahar'
#coding = utf-8
from datetime import datetime
import json


class Good:

    def __init__(self, name=None, country=None, cost=None, date_creating=None):
        self.name = name
        self.country = country
        self.cost = cost
        self.date_creating = date_creating

    def __str__(self):
        return "%s %s %s %s" % (self.name, self.country, self.cost, self.date_creating.strftime("%d/%m/%y"))


good_1 = Good('shovel', 'Germany', 50000, datetime.strptime("22/04/13", "%d/%m/%y"))
good_2 = Good('rake', 'Italy', 25000, datetime.strptime("13/07/13", "%d/%m/%y"))
good_3 = Good('snow', 'Russia', 5000, datetime.strptime("30/05/13", "%d/%m/%y"))
good_4 = Good('peoples', 'Nigeria', 9000, datetime.strptime("01/06/13", "%d/%m/%y"))
good_5 = Good('good1', "USA", 80000, datetime.strptime("15/04/13", "%d/%m/%y"))
good_6 = Good('good2', "Africa", 75600, datetime.strptime("15/04/13", "%d/%m/%y"))
good_7 = Good('good3', "Mexic", 35200, datetime.strptime("15/04/13", "%d/%m/%y"))
good_8 = Good('good4', "Japan", 3200, datetime.strptime("15/04/13", "%d/%m/%y"))
good_9 = Good('good5', "UK", 76580, datetime.strptime("15/04/13", "%d/%m/%y"))
all_goods = [good_1, good_2, good_3, good_4, good_5, good_6, good_7, good_8, good_9]


class Order:

    def __init__(self, name=None, country=None, date_delivering=None):
        self.name = name
        self.country = country
        self.goods = []
        self.date_delivering = date_delivering

    def __str__(self):
        return "%s %s %s" % (self.name, self.country, self.date_delivering.strftime("%d/%m/%y"))

    def total_cost(self):
        return sum([good.cost for good in self.goods])


order_1 = Order("'Avangard'", 'UK', datetime.strptime("15/08/13", "%d/%m/%y"))
order_1.goods = [good_1, good_2, good_3]
order_2 = Order("'Azazaza'", 'RUS', datetime.strptime("21/01/13", "%d/%m/%y"))
order_2.goods = [good_4, good_5, good_6]
order_3 = Order("'Trust'", 'UK', datetime.strptime("21/01/13", "%d/%m/%y"))
order_3.goods = [good_7, good_8, good_9]


def import_from_JSON(json_obj):
    return json.loads(json_obj)

with open('basic.json', mode='w') as f:
    json.dump(good_2, f, indent=2)

#TODO from list to dict

'''

good_10 = {}
good_10['name'] = 'Good_name'
good_10['country'] = 'FRG'

good_11 = {}
good_11['name'] = 'Good_2_name'
good_11['country'] = 'QWEWQ'

ship = {}
ship['goods'] = []
ship['goods'].append(good_10)
ship['goods'].append(good_11)

with open('basic.json', mode='w') as f:
    j_dump = json.dump(ship, f, indent=2)

with open('basic.json', 'r', ) as f:
    entry = json.loads(f)
'''
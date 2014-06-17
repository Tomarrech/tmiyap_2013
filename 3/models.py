__author__ = 'tomar_000'
from datetime import datetime


class Good:
    def __init__(self, good_name=None, good_country=None, good_price=None, production_date=None):
        self.good_name = good_name
        self.good_country = good_country
        self.good_price = good_price
        self.production_date = production_date

    def __str__(self):
        return "%s %s %s" % (self.good_name, self.good_country, self.good_price)

    def to_dict(self):
        if not isinstance(self, Good):
            raise TypeError("It's not a Good..")
        return {'name': self.good_name, 'country': self.good_country, 'price': self.good_price,
                'production_date': self.production_date}

    def __repr__(self):
        return self.__str__()


class Order:
    def __init__(self, order_name, delivery_country, delivery_time):
        self.order_name = order_name
        self.delivery_country = delivery_country
        self.delivery_time = delivery_time
        self.price_of_order = None
        self.goods = []

    def total_price(self):
        return sum([good.good_price for good in self.goods])

    def to_dict(self):
        if not isinstance(self, Order):
            raise TypeError("It's not a Good..")
        return {'name': self.order_name, 'country': self.delivery_country, 'delivery_time': self.delivery_time,
                'price': self.price_of_order, 'goods': [Good.to_dict(good) for good in self.goods]}

    def __str__(self):
        return "%s %s %s" % (self.order_name, self.delivery_country, self.price_of_order)

    __repr__ = __str__
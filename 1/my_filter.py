def filter_goods_with_more_price(goods, price):
    result = filter(lambda good: good.good_price > price, goods)
    return result


def filter_goods_with_lower_price(goods, price):
    result = filter(lambda good: good.good_price < price, goods)
    return result


def filter_goods_from_country(goods, country):
    result = filter(lambda good: good.good_country == country, goods)
    return result
def filter_order_by_time_interval(orders, date_1, date_2):
    result = filter(lambda order: (order.delivery_time > date_1) & (order.delivery_time < date_2), orders)
    return result


def filter_goods_in_order_by_time_interval(order, date_1, date_2):
    result = filter(lambda good: (good.production_date > date_1) & (good.production_date < date_2), order.goods)
    return result

import configparser
from DatabaseHandler import DatabaseHandler
from tracker.requester_all_stores import *
import psycopg2.extras


def link_valid(link):
    if link == 'Invalid link given.':
        return False
    else:
        return True


def get_best_values():

    db_handler = DatabaseHandler()

    products = db_handler.select_all_products()
    prices_array = []

    for product in products:
        product_scrap = dict()
        print(product)
        print('Looking for product ID: {}'.format(product[0]))
        print('Name: {}'.format(product[2]))

        kabum_price = get_kabum(product[4]) if link_valid(product[4]) else 'Does not sell'
        pichau_price = get_pichau(product[5]) if link_valid(product[4]) else 'Does not sell'
        terabyte_price = get_terabyte(product[6]) if link_valid(product[4]) else 'Does not sell'

        product_scrap['id'] = product[0]
        product_scrap['kabum'] = kabum_price
        product_scrap['pichau'] = pichau_price
        product_scrap['terabyte'] = terabyte_price

        prices_array.append(product_scrap)

    for item in prices_array:

        price_tuples = []
        for store in stores_analyzed:
            if item[store]['price_cash'] != 'SOLD OUT' or 'Does not sell':
                price_tuples.append([item[store]['price_cash'], store])

        best_price = min(price_tuples, key=lambda x: x[0])

        print(item['id'])
        print(item['kabum']['product_name'])
        print(price_tuples)
        print(best_price)
    # TODO add function to put prices on Database
    return best_price

from DatabaseHandler import DatabaseHandler
from static.static_vars import *
from functions import *
import configparser
import psycopg2.extras
import re
import json


def link_valid(link):
    if link == 'Invalid link given.':
        return False
    else:
        return True


db_handler = DatabaseHandler()


product_array = db_handler.select_all_products()
prices_array = []
for product in product_array:
    product_scrap = dict()
    print(product)
    print('Looking for product ID: {}'.format(product[0]))
    print('Name: {}'.format(product[2]))

    kabum_price = get_kabum(product[4]) if link_valid(product[4]) else 0
    pichau_price = get_pichau(product[5]) if link_valid(product[4]) else 0
    terabyte_price = get_terabyte(product[6]) if link_valid(product[4]) else 0

    product_scrap['id'] = product[0]
    product_scrap['kabum_price'] = kabum_price
    product_scrap['pichau_price'] = pichau_price
    product_scrap['terabyte_price'] = terabyte_price

    prices_array.append(product_scrap)

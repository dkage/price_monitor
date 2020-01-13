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
for product in product_array:
    print(product)
    print('Looking for product ID: {}'.format(product[0]))
    print('Name: {}'.format(product[2]))

    kabum_price = get_kabum(product[4]) if link_valid(product[4]) else 0
    pichau_price = get_pichau(product[5]) if link_valid(product[4]) else 0
    terabyte_price = get_terabyte(product[6]) if link_valid(product[4]) else 0

    product[4] = kabum_price
    product[5] = pichau_price
    product[6] = terabyte_price

print(product_array)



from DatabaseHandler import DatabaseHandler
from static.static_vars import *
from functions import *
import configparser
import psycopg2.extras
import re
import json


db_handler = DatabaseHandler()

# products = db_handler.select_all_products()
# prices_array = []
#
# for product in products:
#     product_scrap = dict()
#     print(product)
#     print('Looking for product ID: {}'.format(product[0]))
#     print('Name: {}'.format(product[2]))
#
#     kabum_price = get_kabum(product[4]) if link_valid(product[4]) else 'Does not sell'
#     pichau_price = get_pichau(product[5]) if link_valid(product[4]) else 'Does not sell'
#     terabyte_price = get_terabyte(product[6]) if link_valid(product[4]) else 'Does not sell'
#
#     product_scrap['id'] = product[0]
#     product_scrap['kabum'] = kabum_price
#     product_scrap['pichau'] = pichau_price
#     product_scrap['terabyte'] = terabyte_price
#
#     prices_array.append(product_scrap)
#
# for item in prices_array:
#
#     price_tuples = []
#     for store in stores_analyzed:
#         if item[store]['price_cash'] != 'SOLD OUT' or 'Does not sell':
#             price_tuples.append([item[store]['price_cash'], store])
#
#     best_price = min(price_tuples, key=lambda x: x[0])
#
#     best_price_store = best_price[1]
#
#     print(item['id'])
#     print(item['kabum']['product_name'])
#     print(price_tuples)
#     print(best_price)
#     print(item[best_price_store])

    # db_handler.insert_best_price(item['id'], item[best_price_store])


# print(db_handler.grab_best_price(1))
# print(db_handler.grab_best_price(2))

array_return = db_handler.create_current_prices_array()

print(array_return[1]['terabyte'])

from functions import *
import configparser
import psycopg2.extras
import re
import json
from DatabaseHandler import DatabaseHandler


db_handler = DatabaseHandler()
products = db_handler.get_products_array()


for product in products:
    kabum = get_kabum(product['link_kabum'])
    pichau = get_pichau(product['link_pichau'])
    terabyte = get_terabyte(product['link_terabyte'])
    print(kabum)
    print(pichau)
    print(terabyte)


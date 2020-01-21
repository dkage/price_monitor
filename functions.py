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
        price_array_element = dict()
        print(product)
        print('Looking for product ID: {}'.format(product[0]))
        print('Name: {}'.format(product[2]))

        kabum_price = get_kabum(product[4]) if link_valid(product[4]) else 'Does not sell'
        pichau_price = get_pichau(product[5]) if link_valid(product[4]) else 'Does not sell'
        terabyte_price = get_terabyte(product[6]) if link_valid(product[4]) else 'Does not sell'

        price_array_element['id'] = product[0]
        price_array_element['kabum'] = kabum_price
        price_array_element['pichau'] = pichau_price
        price_array_element['terabyte'] = terabyte_price

        prices_array.append(price_array_element)

    for scraped_product_info in prices_array:
        print('\n\n\n')
        print('Now checking product {}'.format(scraped_product_info))

        price_tuples = []
        for store in stores_analyzed:
            if scraped_product_info[store]['price_cash'] != 'SOLD OUT' or 'Does not sell':
                price_tuples.append([scraped_product_info[store]['price_cash'], store])
        print(price_tuples)
        # If not a single store sells or is sold out in every one, jumps to next item
        if not price_tuples:
            continue

        # Grabs lowest value inside the tuples list
        best_price_tuple = min(price_tuples, key=lambda x: x[0])
        current_best_price = best_price_tuple[0]
        current_best_price_store = best_price_tuple[1]

        # Grabs from DB last best price of product ID
        last_best_price = db_handler.grab_best_price(scraped_product_info['id'])

        if float(current_best_price) < float(last_best_price) or float(last_best_price) == 0:
            # Insert prices into db
            db_handler.insert_best_price(scraped_product_info['id'], scraped_product_info[current_best_price_store],
                                         current_best_price_store)

    return 'test'

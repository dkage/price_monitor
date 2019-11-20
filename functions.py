import configparser
from trackers.kabum_functions import *
from trackers.terabyte_functions import *
from trackers.pichau_functions import *


def get_ini():
    ini_data = configparser.ConfigParser()
    ini_data.read_file(open('products.ini'))

    return ini_data


def generate_prices_dict():
    data = get_ini()

    products_dicts = dict()
    products_dicts['store_prices'] = dict()
    return_dict = list
    products = []
    for section in data.sections():
        products_dicts['store_prices'][section] = dict()
        for item in data.items(section):
            products.append(item[0])
            if section == 'kabum':
                return_dict = get_kabum(data.get(section, item[0]))
            if section == 'pichau':
                return_dict = get_pichau(data.get(section, item[0]))
            if section == 'terabyte':
                return_dict = get_terabyte(data.get(section, item[0]))
            products_dicts['store_prices'][section][item[0]] = return_dict

    products_dicts['product_keys'] = set(products)

    return products_dicts


# TODO create new function to check for best value and tag it (maybe call it on function generate?)
# TODO example products_dicts[best] = [store, price, price_cash]

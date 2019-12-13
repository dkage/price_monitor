import configparser
from tracker.requester_all_stores import *
import psycopg2.extras


# TODO delete this section
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
    stores = []
    for section in data.sections():
        stores.append(section)
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
    products_dicts['stores'] = stores

    return products_dicts


# TODO needs refactoring
def get_best_values(product_dict):

    # Def encapsulated because it's only used inside this function
    def get_best_price(prices_tuple_list):
        clean_tuple_list = [((float(price_element.replace("R$", "").replace(".", "").replace(",", "."))), store_element)
                            for price_element, store_element in prices_tuple_list]

        best = min(clean_tuple_list, key=lambda x: x[0])

        return best

    best_values = dict()

    for product in product_dict['product_keys']:
        best_values[product] = dict()
        cash_price = []  # Resets for each product
        price = []  # Resets for each product
        for store in product_dict['stores']:
            if product_dict['store_prices'][store][product]['price_cash'] != "SOLD OUT":
                cash_price.append([product_dict['store_prices'][store][product]['price_cash'], store])
                price.append([product_dict['store_prices'][store][product]['price'], store])
        best_price_cash = get_best_price(cash_price)
        best_price = get_best_price(price)
        best_values[product]['cash'] = best_price_cash
        best_values[product]['price'] = best_price

    return best_values

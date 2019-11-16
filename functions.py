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
    return_dict = list
    for section in data.sections():
        products_dicts[section] = dict()
        for item in data.items(section):
            if section == 'kabum':
                return_dict = get_kabum(data.get(section, item[0]))
            if section == 'pichau':
                return_dict = get_pichau(data.get(section, item[0]))
            if section == 'terabyte':
                return_dict = get_terabyte(data.get(section, item[0]))
            products_dicts[section][item[0]] = return_dict

    return products_dicts


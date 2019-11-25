from bs4 import BeautifulSoup
import re
import requests
from misc_functions import *


def get_terabyte(product_string):
    base_url = 'https://www.terabyteshop.com.br/produto/'

    http_return = requests.get(base_url + product_string)
    soup = BeautifulSoup(http_return.content, 'lxml')

    product = terabyte_check_availability(soup)
    product["product_name"] = soup.find('h1', {"class": "tit-prod"}).text

    # If product already has key price, that means that it was populated in check_availability(), so product is SOLD OUT
    if 'price' in product.keys():
        return product

    # As Terabyte website loads the prices on the fly, the script get the values using a REGEX directly from the
    # jquery calls to put the values inside the documents elements.
    product_prices = terabyte_grab_from_jquery(soup.find_all('script'))
    product["price_cash"] = clear_string(product_prices[0][0])
    product["price"] = clear_string(product_prices[0][1])
    product["installments"] = clear_string(product_prices[1][0])

    return product


def terabyte_grab_from_jquery(script_soup):
    """
    Grabs prices directly from jquery
    :param: Beautiful object "soup" with all script tags inside get returned from url
    :return: returns tuple, where first element contains [price_cash, price, price_for_max_installments] and second
             element contains [maximum_number_of_installments]
    """
    prices = []

    prices = [re.findall(r'.*(R\$.*)\'', str(script_soup)), re.findall(r".*nParc'.*\('(.*)'", str(script_soup))]

    return prices


def terabyte_check_availability(soup):
    if soup.find('div', {'id': 'indisponivel'}):
        return {"price_cash": 'SOLD OUT',
                "price": 'SOLD OUT',
                "installments": 'SOLD OUT'}
    else:
        return dict()

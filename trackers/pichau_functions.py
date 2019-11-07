from bs4 import BeautifulSoup
import requests


def get_pichau(product_string):
    base_url = 'https://www.pichau.com.br/'

    http_return = requests.get(base_url + product_string)
    soap = BeautifulSoup(http_return.content, 'lxml')

    product = dict()

    product["product_name"] = soap.find('div', {'class': 'product title'}).find('h1').text
    product["price"] = soap.find('span', {'class': 'price'}).text
    product["price_cash"] = str(soap.find('span', {'class': 'price-boleto'}).find('span').text).split(' ')[-1]

    return product

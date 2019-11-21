from bs4 import BeautifulSoup
import requests


def get_pichau(product_string):
    base_url = 'https://www.pichau.com.br/'

    http_return = requests.get(base_url + product_string)
    soup = BeautifulSoup(http_return.content, 'lxml')

    product = dict()

    product["product_name"] = soup.find('div', {'class': 'product title'}).find('h1').text

    if check_availability(soup):
        product["price"] = soup.find('span', {'class': 'price'}).text
        product["price_cash"] = str(soup.find('span', {'class': 'price-boleto'}).find('span').text).split(' ')[-1]
    else:
        product["price"] = 'SOLD OUT'
        product["price_cash"] = 'SOLD OUT'
    product["installments"] = 'x10'  # TODO NEEDS TO BE TAKEN FROM SOUP, this decreases for low value products

    return product


def check_availability(soup):
    if soup.find('div', {'class': 'stock unavailable'}):
        return False
    else:
        return True

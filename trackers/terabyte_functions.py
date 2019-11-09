from bs4 import BeautifulSoup
import re
import requests


def get_terabyte(product_string):
    base_url = 'https://www.terabyteshop.com.br/produto/'

    http_return = requests.get(base_url + product_string)
    soup = BeautifulSoup(http_return.content, 'lxml')

    product = dict()

    grab_from_jquery(soup.find_all('script'))
    product["product_name"] = soup.find('h1', {"class": "tit-prod"}).text
    # product["price"] = soup.find('p', {"class": "val-parc"})

    # product["price_cash"] = soup.find_all('script')

    # $('.val-prod').text('R$ 1.099,00');
    # $('#label-val-prod').text('13% de desconto à vista');
    # $('.valParc').text('R$ 1.263,22');
    # $('.nParc').text('12x');
    # $('.Parc').text('R$ 105,27');

    return product


def grab_from_jquery(script_soup):
    prices = []

    prices = [re.findall(r'.*(R\$.*)\'', str(script_soup)), re.findall(r".*nParc'.*\('(.*)'", str(script_soup))]

    print(prices)
    return prices

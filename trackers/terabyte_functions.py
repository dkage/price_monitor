from bs4 import BeautifulSoup
import requests


def get_terabyte(product_string):
    base_url = 'https://www.terabyteshop.com.br/produto/'

    http_return = requests.get(base_url + product_string)
    soup = BeautifulSoup(http_return.content, 'lxml')

    product = dict()

    product["product_name"] = soup.find('h1', {"class": "tit-prod"}).text
    product["price"] = soup.find('p', {"class": "val-parc"})
    print( soup.find('p', {"class": "val-parc"}))
    # product["price_cash"] = soup.find('span', {"class": "preco_desconto_avista-cm"}).text


    return product

from static.static_vars import *
from bs4 import BeautifulSoup
import re
import requests
from tracker.tracker_functions import *


def get_kabum(product_code):
    """
        Given a product code from Kabum (can be picked from product URL accessing their website)
    :param product_code:  number utilized as ID for kabum products
    :return: dict with 3 indexes, 'product_name', 'price' for full prize and 'price_cash' for paying with boleto.
    """

    print("KABUM Product")
    product_url = kabum_base_url + str(product_code)

    print("Product FULL_URL generated: " + product_url)
    print("Requesting now.")

    http_return = requests.get(product_url)

    print("Request finished, generating new soup!")

    soup = BeautifulSoup(http_return.content, 'lxml')

    # Initialize
    url_redirect = str()

    # Kabum uses two different URL structures. If we use 'base_url' variable and put code of a product that uses the
    # other type, page requested it is a simple meta redirect. So we grab that url to receive the true URL.
    if len(str(soup)) < 1000:  # If soup is too small, it's obviously a redirect page, so we grab url and GET again.
        for tag in soup.find_all("meta"):
            if 'url=' in tag.get('content'):
                url_redirect = str(tag.get('content')).split('=', 1)[1]

        print("Request received too small, trying second URL structure.")
        print("New FULL_URL: " + url_redirect)
        print("Requesting now.")

        http_return = requests.get(url_redirect)

        print("Request finished, generating new soup!")

        soup = BeautifulSoup(http_return.content, 'lxml')

    return kabum_get_product_dict(soup)


def kabum_get_product_dict(soup):
    product = dict()
    product_available = kabum_check_availability(soup)

    if product_available:
        # If product is on sale, different HTML elements are used. If on sale contains div class "contTEXTO"
        # else it's not.
        if soup.find('div', {'class': 'contTEXTO'}):
            product["product_name"] = soup.find('h1', {"class": "titulo_det"}).text
            product["price"] = only_numbers(soup.find('div', {"class": "preco_desconto-cm"}).find('strong').text)
            product["price_cash"] = only_numbers(soup.find('span', {"class": "preco_desconto_avista-cm"}).text)
        else:
            product["product_name"] = soup.find('h1', {"class": "titulo_det"}).text
            product["price"] = only_numbers(soup.find('div', {"class": "preco_normal"}).text)
            product["price_cash"] = only_numbers(soup.find('span', {"class": "preco_desconto"}).find('strong').text)
    else:
        # if product is not available at Kabum, the only data used is the product name
        product = kabum_set_sold_out(soup.find('h1', {"class": "titulo_det"}).text)
    product["installments"] = "x3"

    return product


def kabum_check_availability(soup):
    if soup.find('div', {'id': 'contador-cm'}):  # if there is div called 'contador-cm' product is on sale, so available
        return True
    available = soup.find('div', {'class': 'disponibilidade'}).find('img')['alt']
    if available == 'produto_indisponivel':
        return False
    else:
        return True


def kabum_set_sold_out(product_name):
    return {"product_name": product_name,
            "price": 'SOLD OUT',
            "price_cash": 'SOLD OUT'}


def get_pichau(product_string):

    http_return = requests.get(pichau_base_url + product_string)
    soup = BeautifulSoup(http_return.content, 'lxml')

    product = dict()

    try:
        product["product_name"] = soup.find('div', {'class': 'product title'}).find('h1').text
    except AttributeError:
        product["product_name"] = 'REMOVED'

    if pichau_check_availability(soup):
        product["price"] = only_numbers(soup.find('span', {'class': 'price'}).text)
        product["price_cash"] = only_numbers(str(soup.find('span', {'class': 'price-boleto'}).
                                                 find('span').text).split(' ')[-1])
    else:
        product["price"] = 'SOLD OUT'
        product["price_cash"] = 'SOLD OUT'
    product["installments"] = 'x10'  # TODO NEEDS TO BE TAKEN FROM SOUP, this decreases for low value products

    return product


def pichau_check_availability(soup):
    if soup.find('div', {'class': 'stock unavailable'}) or soup.find('div', {'class': 'mensagem-vazio'}):
        return False
    else:
        return True


def get_terabyte(product_string):

    http_return = requests.get(terabyte_base_url + product_string)
    soup = BeautifulSoup(http_return.content, 'lxml')

    product = terabyte_check_availability(soup)
    product["product_name"] = soup.find('h1', {"class": "tit-prod"}).text

    # If product already has key price, that means that it was populated in check_availability(), so product is SOLD OUT
    if 'price' in product.keys():
        return product

    # As Terabyte website loads the prices on the fly, the script get the values using a REGEX directly from the
    # jquery calls to put the values inside the documents elements.
    product_prices = terabyte_grab_from_jquery(soup.find_all('script'))
    product["price_cash"] = only_numbers(product_prices[0][0])
    product["price"] = only_numbers(product_prices[0][1])
    product["installments"] = clear_string(product_prices[1][0])

    return product


def terabyte_grab_from_jquery(script_soup):
    """
    Grabs prices directly from jquery
    :param: Beautiful object "soup" with all script tags inside get returned from url
    :return: returns tuple, where first element contains [price_cash, price, price_for_max_installments] and second
             element contains [maximum_number_of_installments]
    """

    prices = [re.findall(r'.*(R\$.*)\'', str(script_soup)), re.findall(r".*nParc'.*\('(.*)'", str(script_soup))]

    return prices


def terabyte_check_availability(soup):
    if soup.find('div', {'id': 'indisponivel'}):
        return {"price_cash": 'SOLD OUT',
                "price": 'SOLD OUT',
                "installments": 'SOLD OUT'}
    else:
        return dict()

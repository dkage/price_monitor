from bs4 import BeautifulSoup
import requests


def get_kabum (product_code):
    base_url = 'https://www.kabum.com.br/cgi-local/site/produtos/descricao_ofertas.cgi?codigo='

    http_return = requests.get(base_url + str(product_code))
    soup = BeautifulSoup(http_return.content, 'lxml')

    product = dict()

    # TODO create case where product has promotion
    product["product_name"] = soup.find('h1', {"class": "titulo_det"}).text
    print(product["product_name"])
    product["price"] = soup.find('div', {"class": "preco_desconto-cm"}).find('strong').text
    product["price_cash"] = soup.find('span', {"class": "preco_desconto_avista-cm"}).text

    return product

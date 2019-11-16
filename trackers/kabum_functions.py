from bs4 import BeautifulSoup
import requests


def get_kabum(product_code):
    """
        Given a product code from Kabum (can be picked from product URL accessing their website)
    :param product_code:  number utilized as ID for kabum products
    :return: dict with 3 indexes, 'product_name', 'price' for full prize and 'price_cash' for paying with boleto.
    """

    base_url = 'https://www.kabum.com.br/cgi-local/site/produtos/descricao_ofertas.cgi?codigo='

    http_return = requests.get(base_url + str(product_code))
    soup = BeautifulSoup(http_return.content, 'lxml')

    # Initialize
    url_redirect = str()

    # Kabum uses two different URL structures. If we use 'base_url' variable and put code of a product that uses the
    # other type, page requested it is a simple meta redirect. So we grab that url to receive the true URL.
    if len(str(soup)) < 1000:  # If soup is too small, it's obviously a redirect page, so we grab url and GET again.
        for tag in soup.find_all("meta"):
            if 'url=' in tag.get('content'):
                url_redirect = str(tag.get('content')).split('=', 1)[1]

        http_return = requests.get(url_redirect)
        soup = BeautifulSoup(http_return.content, 'lxml')

    return get_product_dict(soup)


def get_product_dict(soup):
    product = dict()
    product_available = check_availability(soup)

    if product_available:
        # If product is on sale, different HTML elements are used. If on sale contains div class "contTEXTO" else
        # it's not.
        if soup.find('div', {'class': 'contTEXTO'}):
            product["product_name"] = soup.find('h1', {"class": "titulo_det"}).text
            product["price"] = str(soup.find('div', {"class": "preco_desconto-cm"}).find('strong').text).strip()
            product["price_cash"] = str(soup.find('span', {"class": "preco_desconto_avista-cm"}).text).strip()
        else:
            product["product_name"] = soup.find('h1', {"class": "titulo_det"}).text
            product["price"] = str(soup.find('div', {"class": "preco_normal"}).text).strip()
            product["price_cash"] = str(soup.find('span', {"class": "preco_desconto"}).find('strong').text).strip()
    else:
        # if product is not available at Kabum, the only data used is the product name
        product = set_sold_out(soup.find('h1', {"class": "titulo_det"}).text)

    return product


def check_availability(soup):
    if soup.find('div', {'id': 'contador-cm'}):  # if there is div called 'contador-cm' product is on sale, so available
        return True
    available = soup.find('div', {'class': 'disponibilidade'}).find('img')['alt']
    if available == 'produto_indisponivel':
        return False
    else:
        return True


def set_sold_out(product_name):
    return {"product_name": product_name,
            "price": 'SOLD OUT',
            "price_cash": 'SOLD OUT'}

from bs4 import BeautifulSoup
import requests


def get_kabum (product_code):
    base_url = 'https://www.kabum.com.br/cgi-local/site/produtos/descricao_ofertas.cgi?codigo='

    http_return = requests.get(base_url + str(product_code))
    soup = BeautifulSoup(http_return.content, 'lxml')

    # Initialize
    product = dict()
    url_redirect = str()

    # Kabum uses two different URL structures. If we use 'base_url' variable and put code of a product that uses the
    # other type, page requested it is a simple meta redirect. So we grab that url to receive the true URL.
    if len(str(soup)) < 1000:  # If soup is too small, it's obviously a redirect page, so we grab url and GET again.
        for tag in soup.find_all("meta"):
            if 'url=' in tag.get('content'):
                url_redirect = str(tag.get('content')).split('=', 1)[1]

        http_return = requests.get(url_redirect)
        soup = BeautifulSoup(http_return.content, 'lxml')

    # If product is on sale, different HTML elements are used. If on sale contains div class "contTEXTO" else it's not.
    if soup.find('div', {'class': 'contTEXTO'}):
        product["product_name"] = soup.find('h1', {"class": "titulo_det"}).text
        product["price"] = soup.find('div', {"class": "preco_desconto-cm"}).find('strong').text
        product["price_cash"] = soup.find('span', {"class": "preco_desconto_avista-cm"}).text
    else:
        product["product_name"] = soup.find('h1', {"class": "titulo_det"}).text
        product["price"] = str(soup.find('div', {"class": "preco_normal"}).text).strip()
        product["price_cash"] = soup.find('span', {"class": "preco_desconto"}).find('strong').text

    return product

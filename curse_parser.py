import requests
from bs4 import BeautifulSoup


def get_curse(url):
    currency_info = {}
    r = requests.get(url)
    encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(r.content, 'xml', from_encoding=encoding)
    currency = soup.find_all('Valute')
    for elem in currency:
        currency_info[elem.find('NumCode').text] = {
            'char_code': elem.find('CharCode').text,
            'name': elem.find('Name').text,
            'value': elem.find('Value').text
        }
    return currency_info

import requests
from bs4 import BeautifulSoup

url = 'https://www.cbr.ru/scripts/XML_daily.asp'


async def get_url() -> BeautifulSoup:
    r = requests.get(url)
    encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(r.content, 'xml', from_encoding=encoding)
    return soup


async def get_curse():
    currency_info = {}
    soup = await get_url()
    currency = soup.find_all('Valute')
    for elem in currency:
        currency_info[elem.find('NumCode').text] = {
            'char_code': elem.find('CharCode').text,
            'name': elem.find('Name').text,
            'value': elem.find('Value').text
        }
    return currency_info


async def convert_valute(valute1, valute2):
    answer = {}

    if valute1 == 'RUB':
        answer['v1'] = 1
    if valute2 == 'RUB':
        answer['v2'] = 1

    soup = await get_url()
    currency = soup.find_all('Valute')

    for elem in currency:
        if elem.find('CharCode').text == valute1:
            answer['v1'] = float(elem.find('Value').text.replace(',', '.')) / int(elem.find('Nominal').text)
        if elem.find('CharCode').text == valute2:
            answer['v2'] = float(elem.find('Value').text.replace(',', '.')) / int(elem.find('Nominal').text)
        if len(answer) == 2:
            return answer
    return answer
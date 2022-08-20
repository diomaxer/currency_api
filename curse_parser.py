import datetime
import requests

from typing import List
from fastapi import HTTPException
from starlette import status
from bs4 import BeautifulSoup

from database.pydantic_models import Convert, Currency, CountAmount


async def get_url(date=None) -> BeautifulSoup:
    if date:
        url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date.strftime("%d/%m/%Y")}'
    else:
        url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    r = requests.get(url)
    encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(r.content, 'xml', from_encoding=encoding)
    return soup


class Parser:
    @staticmethod
    async def get_all_courses(date=None) -> List[Currency]:
        if date and date < datetime.date(1993, 1, 1):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data available after 1993-01-01")
        currency_info = []
        soup = await get_url(date=date)
        currency = soup.find_all('Valute')
        for elem in currency:
            currency_info.append(
                Currency(
                    num_code=elem.find('NumCode').text,
                    char_code=elem.find('CharCode').text,
                    name=elem.find('Name').text,
                    value=float(elem.find('Value').text.replace(',', '.'))

                )
            )
        return currency_info

    @staticmethod
    async def get_currencies(convert: Convert) -> CountAmount:
        answer = {}

        if convert.from_char_code == 'RUB':
            answer['sum'] = 1
        if convert.to_char_code == 'RUB':
            answer['sum2'] = 1


        soup = await get_url(date=convert.date)
        currencies = soup.find_all('Valute')

        for currency in currencies:
            if currency.find('CharCode').text == convert.from_char_code:
                answer['sum'] = float(currency.find('Value').text.replace(',', '.')) / int(currency.find('Nominal').text)
            if currency.find('CharCode').text == convert.to_char_code:
                answer['sum2'] = float(currency.find('Value').text.replace(',', '.')) / int(currency.find('Nominal').text)
            if len(answer) == 2:
                return CountAmount(**answer)

        print(answer)

        missing_char_code = convert.from_char_code if 'sum2' in answer.keys() else convert.to_char_code
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"no data for this char code '{missing_char_code}'")

import datetime

from typing import List
from bs4 import BeautifulSoup
from fastapi import HTTPException
from starlette import status

from parser.curse_parser import Parser
from database.pydantic_models import Convert, Amount, Currency, MultiCurrency


class CurseManager:
    @staticmethod
    async def get_current_curse(char_code: str, date: datetime.date = None) -> Currency:
        if date and date < datetime.date(1993, 1, 1):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data available after 1997-01-01")
        response = await Parser.get_url(date=date)
        elem = response.find("CharCode", string=char_code).find_parent("Valute")
        currency = Currency(
            num_code=elem.find("NumCode").text,
            char_code=elem.find("CharCode").text,
            name=elem.find("Name").text,
            nominal=int(elem.find("Nominal").text),
            value=float(elem.find("Value").text.replace(',', '.'))
        )
        return currency

    @staticmethod
    async def get_multi_curses(multi_currency: MultiCurrency = None) -> List[Currency]:
        if multi_currency.date and multi_currency.date < datetime.date(1993, 1, 1):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data available after 1997-01-01")
        response = await Parser.get_url(date=multi_currency.date)
        currency_info = []
        currencies = response.find_all("CharCode", string=[code.char_code for code in multi_currency.char_codes])
        for currency in currencies:
            elem = currency.find_parent("Valute")
            currency_info.append(
                Currency(
                    num_code=elem.find("NumCode").text,
                    char_code=elem.find("CharCode").text,
                    name=elem.find("Name").text,
                    nominal=int(elem.find("Nominal").text),
                    value=float(elem.find("Value").text.replace(',', '.'))

                )
            )
        return currency_info

    @staticmethod
    async def get_all_courses(date: datetime.date = None) -> List[Currency]:
        if date:
            if date < datetime.date(1993, 1, 1):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data available after 1993-01-01")
            if date > datetime.date.today():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="date can't be greater then today")
        currency_info = []
        response = await Parser.get_url(date=date)
        currencies = response.find_all("Valute")
        for elem in currencies:
            currency_info.append(
                Currency(
                    num_code=elem.find("NumCode").text,
                    char_code=elem.find("CharCode").text,
                    name=elem.find("Name").text,
                    nominal=int(elem.find("Nominal").text),
                    value=float(elem.find("Value").text.replace(',', '.'))

                )
            )
        return currency_info

    @staticmethod
    async def count_currency_value(soup: BeautifulSoup, char_code: str) -> float:
        if char_code == "RUB":
            return 1
        currency = soup.find("CharCode", string=char_code)
        if not currency:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"no data for this char code '{char_code}'")

        value = float(currency.find_next_sibling("Value").text.replace(",", "."))
        nominal = int(currency.find_next_sibling("Nominal").text)
        actual_value = value / nominal
        return round(actual_value, 2)

    @staticmethod
    async def convert_currency(convert: Convert) -> Amount:
        response = await Parser.get_url(date=convert.date)
        valute1 = await CurseManager.count_currency_value(soup=response, char_code=convert.char_code)
        valute2 = await CurseManager.count_currency_value(soup=response, char_code=convert.to_char_code)
        amount = valute1 / valute2 * convert.sum
        return Amount(sum=round(amount, 2))

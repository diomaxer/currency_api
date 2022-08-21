import datetime

from typing import List
from bs4 import BeautifulSoup
from fastapi import HTTPException
from starlette import status

from parser.curse_parser import Parser
from database.pydantic_models import Convert, Amount, Currency


class CurseManager:
    @staticmethod
    async def get_all_courses(date: datetime.date = None) -> List[Currency]:
        if date and date < datetime.date(1993, 1, 1):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data available after 1993-01-01")
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
        valute1 = await CurseManager.count_currency_value(soup=response, char_code=convert.from_char_code)
        valute2 = await CurseManager.count_currency_value(soup=response, char_code=convert.to_char_code)
        amount = valute1 / valute2 * convert.sum
        return Amount(sum=round(amount, 2))

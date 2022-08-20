import datetime
from typing import List

from curse_parser import  Parser
from database.pydantic_models import Convert, Amount, Currency


class CurseManager:
    @staticmethod
    async def get_all_courses(date: datetime.date=None) -> List[Currency]:
        return await Parser.get_all_courses(date=date)

    @staticmethod
    async def convert_currency(convert: Convert) -> Amount :
        currency = await Parser.get_currencies(convert=convert)
        amount = currency.sum / currency.sum2 * convert.sum
        return Amount(sum=round(amount, 2))


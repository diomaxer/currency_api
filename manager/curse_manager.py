from curse_parser import convert_valute
from database.pydantic_models import Convert


async def count_convert(convert: Convert):
    currensy = await convert_valute(convert.from_char_code, convert.to_char_code)
    if len(currensy) != 2:
            return {"error": "char code doesn't exist"}
    amount = currensy['v1'] / currensy['v2'] * convert.sum
    return round(amount, 2)


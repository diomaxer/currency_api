import datetime

from typing import List
from fastapi import FastAPI

from manager.curse_manager import CurseManager
from database.pydantic_models import Convert, Currency, Amount, MultiCurrency, CharCodeCurrency

app = FastAPI()


@app.get(
    path="/",
    response_model=List[Currency],
    summary="Popular exchange rates",
    description="USD & EUR exchange rates according to the Central Bank of the Russian Federation",
    responses={
        400: {
            "content": {"application/json": {"example": {
                "detail": ["no data for this char code 'CharCode'", "date can't be greater then today"]
            }}}
        },

        404: {
            "content": {"application/json": {"example": {"detail": "data available after 1993-01-01"}}},
        }}
)
async def today_curse(date: datetime.date = None) -> List[Currency]:
    popular_currency = MultiCurrency(
        date=date if date else datetime.date.today(),
        char_codes=[CharCodeCurrency(char_code="USD"), CharCodeCurrency(char_code="EUR")]
    )
    return await CurseManager.get_multi_curses(multi_currency=popular_currency)


@app.get(
    path="/all_courses",
    response_model=List[Currency],
    summary="All exchange rates",
    description="All exchange rates according to the Central Bank of the Russian Federation",
    responses={
        400: {
            "content": {"application/json": {"example": {
                "detail": ["no data for this char code 'CharCode'", "date can't be greater then today"]
            }}}
        },

        404: {
            "content": {"application/json": {"example": {"detail": "data available after 1993-01-01"}}},
        }}
)
async def today_curse(date: datetime.date = None) -> List[Currency]:
    return await CurseManager.get_all_courses(date=date)


@app.get(
    path="/char_codes",
    response_model=List[CharCodeCurrency],
    summary="All currency codes",
    description="Get all available currency codes",
    responses={
        400: {
            "content": {"application/json": {"example": {
                "detail": ["no data for this char code 'CharCode'", "date can't be greater then today"]
            }}}
        },

        404: {
            "content": {"application/json": {"example": {"detail": "data available after 1993-01-01"}}},
        }}
)
async def currency_codes(date: datetime.date = None) -> List[CharCodeCurrency]:
    return await CurseManager.get_all_char_codes(date=date)


@app.post(
    path="/convert",
    response_model=Amount,
    summary="Currency conversion",
    description="Currency conversion at the rate of the Central Bank of the Russian Federation. "
                "date: Optional, "
                "char_code: currency which convert, "
                "sum: amount of currency, "
                "char_code_to: currency into convert",
    responses={
        400: {
            "content": {"application/json": {"example": {
                "detail": ["no data for this char code 'CharCode'", "date can't be greater then today"]
            }}}
        },
        404: {
            "content": {"application/json": {"example": {"detail": "data available after 1997-01-01"}}},
        }}
)
async def convert_currency(convert: Convert) -> Amount:
    return await CurseManager.convert_currency(convert=convert)

import datetime

from typing import List
from fastapi import FastAPI

from manager.curse_manager import CurseManager
from database.pydantic_models import Convert, Currency, Amount, MultiCurrency, CharCodeCurrency

app = FastAPI()


@app.get(
    path="/",
    response_model=List[Currency],
    summary="popular exchange rates",
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
    print(popular_currency)
    return await CurseManager.get_multi_curses(multi_currency=popular_currency)


@app.get(
    path="/all_courses/",
    response_model=List[Currency],
    summary="Exchange rates",
    description="Exchange rates according to the Central Bank of the Russian Federation",
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


@app.post(
    path="/multiple_curses/",
    response_model=List[Currency],
    summary="Multiple currency exchange rate",
    description="Multiple currency exchange rates according to the Central Bank of the Russian Federation",
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
async def today_curse(multi_currency: MultiCurrency) -> List[Currency]:
    return await CurseManager.get_multi_curses(multi_currency=multi_currency)


@app.post(
    path="/convert/",
    response_model=Amount,
    summary="Currency conversion",
    description="Currency conversion at the rate of the Central Bank of the Russian Federation",
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

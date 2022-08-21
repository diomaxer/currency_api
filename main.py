import datetime

from typing import List
from fastapi import FastAPI

from manager.curse_manager import CurseManager
from database.pydantic_models import Convert, Currency, Amount

app = FastAPI()


@app.get(
    path="/",
    response_model=List[Currency],
    summary="Exchange rates",
    description="Exchange rates according to the Central Bank of the Russian Federation",
    responses={
        404: {
            "content": {"application/json": {"example": {"detail": "data available after 1993-01-01"}}},
        }}
)
async def today_curse(date: datetime.date=None) -> List[Currency]:
    return await CurseManager.get_all_courses(date=date)


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

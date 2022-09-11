import datetime

from datetime import date
from typing import List
from fastapi import HTTPException
from starlette import status
from pydantic import BaseModel, validator


class CharCodeCurrency(BaseModel):
    char_code: str

    @validator("char_code")
    def upper_char_code(cls, v):
        return v.upper()


class Date(BaseModel):
    date: datetime.date | None

    @validator("date")
    def check_year(cls, v):
        if v < date(1997, 1, 1):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data available after 1997-01-01")
        if v > date.today():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="date can't be greater then today")
        return v


class Convert(CharCodeCurrency, Date):
    sum: float
    to_char_code: str

    @validator("to_char_code")
    def upper_char_code(cls, v):
        return v.upper()


class MultiCurrency(Date):
    char_codes: List[CharCodeCurrency]


class Currency(CharCodeCurrency):
    num_code: int
    name: str
    nominal: int
    value: float


class Amount(BaseModel):
    sum: float

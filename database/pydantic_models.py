from datetime import date
from fastapi import HTTPException
from starlette import status
from pydantic import BaseModel, validator


class Convert(BaseModel):
    sum: float
    from_char_code: str
    to_char_code: str
    date: date | None

    @validator("from_char_code", "to_char_code")
    def upper_char_code(cls, v):
        return v.upper()

    @validator("date")
    def check_year(cls, v):
        if v < date(1997, 1, 1):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data available after 1997-01-01")
        if v > date.today():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="date can't be greater then today")
        return v


class Currency(BaseModel):
    num_code: int
    char_code: str
    name: str
    nominal: int
    value: float


class Amount(BaseModel):
    sum: float


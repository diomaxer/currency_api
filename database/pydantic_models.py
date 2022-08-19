from pydantic import BaseModel, validator


class Convert(BaseModel):
    sum: float
    from_char_code: str
    to_char_code: str

    @validator('from_char_code', 'to_char_code')
    def upper_char_code(cls, v):
        return v.upper()

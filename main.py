from fastapi import FastAPI

from manager.curse_manager import count_convert
from curse_parser import get_curse
from database.pydantic_models import Convert


app = FastAPI()


@app.get('/')
async def today_curse():
    return await get_curse()


@app.post('/convert/')
async def convert_valute(convert: Convert):
    return await count_convert(convert=convert)

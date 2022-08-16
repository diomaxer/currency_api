from fastapi import FastAPI

from curse_parser import get_curse


app = FastAPI()


@app.get('/')
def today_curse():
    return get_curse(url='https://www.cbr.ru/scripts/XML_daily.asp')


@app.get('/convert')
def convert_rub():
    return {'c'}


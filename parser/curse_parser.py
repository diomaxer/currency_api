import requests

from bs4 import BeautifulSoup


class Parser:
    @staticmethod
    async def get_url(date=None) -> BeautifulSoup:
        if date:
            url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date.strftime('%d/%m/%Y')}"
        else:
            url = "https://www.cbr.ru/scripts/XML_daily.asp"
        r = requests.get(url)
        encoding = r.encoding if "charset" in r.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(r.content, "xml", from_encoding=encoding)
        return soup


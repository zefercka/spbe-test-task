import json
import time
from typing import Optional
from urllib.parse import urlencode, urljoin
from exceptions import UnsupportedMethodError, InvalidRequestError
from datetime import datetime
from enums import IntervalEnum

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://query1.finance.yahoo.com/v8/"
http_client = requests.Session()
http_client.headers.update(
    {
        "USER-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.143 Safari/537.36"
    }
)


def _http_request(end_point: str, method: str, payload: dict) -> dict:
    method = method.lower()
    if method not in ["post", "get"]:
        raise UnsupportedMethodError()
    
    url = urljoin(BASE_URL, end_point)
    
    if method == "post":
        response = http_client.request(
            "POST",
            url,
            data=json.dumps(payload)
        )
    elif method == "get":
        response = http_client.request(
            "GET",
            f"{url}?{urlencode(payload)}",
        )

    if response.status_code != 200:
        raise InvalidRequestError(response.text)

    result = json.loads(response.text)

    return result


def get_historical_data(
    ticker: str,
    start: datetime,
    end: Optional[datetime] = datetime.now(tz=None),
    interval: Optional[IntervalEnum] = IntervalEnum.ONE_DAY,
) -> dict:
    end_point = f"finance/chart/{ticker.upper()}"

    interval = IntervalEnum.from_str(interval)\
        if type(interval) != IntervalEnum else interval

    payload = {
        "period1": int(start.timestamp()),
        "period2": int(end.timestamp()),
        "interval": interval,
    }
    
    result = _http_request(end_point, "get", payload)
    
    return result


def _parse_market_cap(value: str) -> int:
    value = value.strip()
    if value[-1] == "T":
        return int(float(value[:-1]) * 1_000_000_000_000)
    elif value[-1] == "B":
        return int(float(value[:-1]) * 1_000_000_000)
    elif value[-1] == "M":
        return int(float(value[:-1]) * 1_000_000)
    elif value[-1] == "K":
        return int(float(value[:-1]) * 1000)
    else:
        return int(value)



def _parse_statistics(
    ticker: str
) -> dict:
    response = http_client.get(
        f"https://finance.yahoo.com/quote/{ticker.upper()}/key-statistics/"
    )

    if response.status_code != 200:
        raise InvalidRequestError(response.text)
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    statistics_table = soup.find("table")
    if not statistics_table:
        raise InvalidRequestError("Statistics table not found.")
    
    statistics_table_tr = statistics_table.find_all("tr")
    statistics = {}

    for tr in statistics_table_tr[1:]:
        statistic_name = tr.find("td").text
        statistic_value = tr.find_all("td")[1].text

        if statistic_name in ["Market Cap", "Enterprise Value"]:
            statistic_value = _parse_market_cap(statistic_value)
        else:
            statistic_value = float(statistic_value)
        
        statistics[statistic_name] = statistic_value

    return statistics


def get_statistics(
    ticker: str,
) -> dict:
    result = _parse_statistics(ticker)
    
    return result
import hashlib
import hmac
import json
import time
from typing import Optional
from urllib.parse import urlencode, urljoin

import requests
from config import config
from exceptions import UnsupportedMethodError, InvalidRequestError

http_client = requests.Session()
BASE_URL = "https://api.bybit.com"


def _http_request(end_point: str, method: str, payload: dict) -> dict:
    method = method.lower()
    if method not in ["post", "get"]:
        raise UnsupportedMethodError()
    
    timestamp = int(time.time() * 1000)
    headers = {
        'X-BAPI-API-KEY': config.API_KEY,
        'X-BAPI-SIGN': _gen_signature(timestamp, payload),
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': str(timestamp),
        'Content-Type': 'application/json'
    }
    
    url = urljoin(BASE_URL, end_point)
    
    if method == "post":
        response = http_client.request(
            "POST",
            url,
            headers=headers,
            data=json.dumps(payload)
        )
    elif method == "get":
        response = http_client.request(
            "GET",
            f"{url}?{urlencode(payload)}",
            headers=headers
        )

    result = json.loads(response.text)

    if result["retCode"] != 0:
        raise InvalidRequestError(result["retMsg"])

    return result


def _gen_signature(timestamp: int, payload: dict):
    param_str: str = str(timestamp) + config.API_KEY + urlencode(payload)
    hash = hmac.new(
        bytes(config.API_SECRET_KEY, "utf-8"),
        param_str.encode("utf-8"),
        hashlib.sha256
    )
    signature = hash.hexdigest()
    return signature


def get_kline(
    symbol: str,
    interval: str,
    limit: Optional[int] = 200,
    category: Optional[str] = None,
    start: Optional[int] = None,
    end: Optional[int] = None,
) -> dict:
    end_point = "/v5/market/kline"
    
    payload = {
        "category": category,
        "symbol": symbol.upper(),
        "interval": interval,
        "start": start,
        "end": end,
        "limit": limit
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    
    result = _http_request(
        end_point=end_point,
        method="GET",
        payload=payload
    )
    
    return result
import requests
import json
from config import main_logger

from random import choice

from config import HEADER_FOR_HEMNET, USING_PROXY

from .parse_proxies import get_proxies

if USING_PROXY:
    proxies = get_proxies()
else:
    proxies = [None]


def request_to_page(link: str) -> dict:
    try:
        response_html = requests.get(
            link,
            headers=HEADER_FOR_HEMNET,
            proxies=choice(proxies)
        )
    except requests.exceptions.ConnectionError:
        main_logger.error("NO NETWORK")
        return None
    except requests.exceptions.MissingSchema as e:
        main_logger.error(f"troubles with links: {str(e)}")
        return None
    try:
        raw_json = str(
            response_html.text
        ).split('<script id="__NEXT_DATA__" type="application/json">')[1]
        raw_json = raw_json.split(r"</script>")[0]
    except IndexError:
        main_logger.error(f"bad HTML {link}")
        with open("error.html", "w", encoding="utf-8") as F:
            F.write(response_html.text)
        return None

    try:
        data_json = json.loads(raw_json)
    except Exception:
        main_logger.error(f"bad json: {link}")
        return None
    return data_json

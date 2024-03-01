from typing import List, Tuple, Final

from config import main_logger

from config import (
    LIMIT_API
)

from .methods import get_links_by_page
from data.methods import get_links_from_site


def parse_response(response: str) -> List[str]:
    links_from_page: List[str] = []

    lines_of_response: List[str] = response.split("\n")
    lines_of_response.pop(0)  # it's data about rows in response

    for line in lines_of_response:
        # not empty line
        if line:
            line = line.replace('"', "")
            link = ",".join(line.split(",")[:-2])
            links_from_page.append(link)
    return links_from_page


def get_links_from_api() -> List[str]:
    all_links: List[str] = []
    now_page: Final = 1
    # i don't know counter of pages of this info,
    # and I wait while request take < 10_000 posts
    while True:
        response_for_page: str = get_links_by_page(now_page)
        links_from_page: List[str] = parse_response(response_for_page)
        counter_links = len(links_from_page)
        all_links += links_from_page
        if counter_links < LIMIT_API:
            break
        now_page += 1
    message = f"got {len(all_links)} links from api "
    message += "about {type_links.api_name} links"
    main_logger.info(message)
    return all_links


def find_need_links() -> Tuple[List[str], List[str], List[str]]:
    links_from_api: set = set(get_links_from_api())
    links_from_site: set = set(get_links_from_site())

    links_moving_to_sold = list(links_from_site - links_from_api)

    return links_moving_to_sold

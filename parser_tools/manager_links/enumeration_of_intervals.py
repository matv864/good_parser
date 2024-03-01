from typing import List, Tuple

from math import ceil
from config import main_logger
import threading

from local_types import Types_links
from config import MAX_LINK_ON_PAGE

from data.methods import get_slice_of_interval_ids, save_links
from ..working_with_site import get_links


def generate_link(
    min_price: int,
    max_price: int,
    page: int,
    type_links: Types_links
) -> str:
    link = f"{type_links.link}?selling_price_min={min_price}"
    link += f"&selling_price_max={max_price}"
    link += f"&page={page}"
    link += "&by=sale_date&order=desc"
    return link


def working_with_price_interval(
    min_price: int,
    max_price: int,
    counter: int,
    type_links: Types_links
) -> None:
    counter_real_link = 0
    counter_pages = ceil(counter / MAX_LINK_ON_PAGE)
    for page in range(1, counter_pages+1):
        link_to_site = generate_link(
            min_price=min_price,
            max_price=max_price,
            page=page,
            type_links=type_links
        )
        links: List[str] = get_links(link_to_site)
        counter_real_link += len(links)
        save_links(links, type_links)

    message = f"collect {counter_real_link} links from {counter}, "
    message += f"parameters: {min_price} - {max_price}"
    main_logger.info(message)


def enumerate_intervals(
    interval_ids: Tuple[int, int],
    type_links: Types_links,
    lock: threading.Lock
) -> None:
    with lock:
        need_intervals: List[Tuple[int, int, int]] = get_slice_of_interval_ids(
            left_border=interval_ids[0],
            right_border=interval_ids[1],
            type_links=type_links
        )
        for price_interval in need_intervals:
            working_with_price_interval(
                min_price=price_interval[0],
                max_price=price_interval[1],
                counter=price_interval[2],
                type_links=type_links
            )

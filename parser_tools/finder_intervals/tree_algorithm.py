from typing import List, Tuple, Optional

import threading

from config import MAX_LINK_ON_FILTER_SETTINGS
from local_types import Types_links

from ..working_with_site import get_counter_of_links_from_page


def main_collector(
    interval: Tuple[int, int],
    type_links: Types_links,
    lock: threading.Lock
) -> None:

    queue_of_intervals: List[Tuple[int, int]] = [interval]
    while queue_of_intervals:  # while not empty queue
        min_price, max_price = queue_of_intervals.pop()
        counter_links: Optional[int] = get_counter_of_links_from_page(
            min_price,
            max_price,
            type_links
        )

        if counter_links is None:
            continue

        if counter_links == 0:
            # check to empty page
            pass
        elif counter_links < MAX_LINK_ON_FILTER_SETTINGS:
            # good interval
            save_interval(
                min_price,
                max_price,
                counter_links,
                type_links,
                lock
            )

        elif abs(max_price - min_price) < 3:
            # huge counter links on interval but we can't decrease interval
            save_interval(
                min_price,
                max_price,
                counter_links,
                type_links,
                lock
            )
        else:
            # bad page, a lot of posts
            middle_price = (min_price + max_price) // 2
            queue_of_intervals.append((min_price, middle_price - 1))
            queue_of_intervals.append((middle_price, max_price))


def save_interval(
    min_price: int,
    max_price: int,
    counter_links: int,
    type_links: Types_links,
    lock: threading.Thread
) -> None:
    info_interval = f"{min_price} {max_price} {counter_links}"
    filename = type_links.filename
    with lock:
        with open(f"data/intervals/{filename}.txt", "a") as F:
            print(info_interval, file=F)

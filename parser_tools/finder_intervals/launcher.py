from typing import List, Tuple

import threading

from config import main_logger

from local_types import Types_links
from config import COMMON_INTERVAL_PRICE, NUMBER_THREADS

from .tree_algorithm import main_collector

from ..small_tools import time_wrapper, multithreading

# thread lost task because 3 to 5 billion price
# is 10 houses (for example) and it finish work
COEF_TO_THREADS_IN_TREE = 5


def divided_price_interval() -> List[Tuple[int, int]]:
    intervals_prices = []
    distance_intervals = (
        COMMON_INTERVAL_PRICE[1] -
        COMMON_INTERVAL_PRICE[0]
    ) // (NUMBER_THREADS * COEF_TO_THREADS_IN_TREE)
    iter_left_border = COMMON_INTERVAL_PRICE[0]

    for _ in range(NUMBER_THREADS * COEF_TO_THREADS_IN_TREE):
        intervals_prices.append((
            iter_left_border,
            iter_left_border + distance_intervals - 1
        ))
        iter_left_border += distance_intervals

    return intervals_prices


@time_wrapper
def launch_finder_intervals(type_links: Types_links) -> None:
    intervals_prices = divided_price_interval()
    multithreading(
        main_collector,
        args=intervals_prices,
        type_links=type_links,
        lock=threading.Lock()
    )
    main_logger.info(f"start threads: {NUMBER_THREADS}")

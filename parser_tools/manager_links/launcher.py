from typing import List, Tuple

import threading

from local_types import Types_links
from config import NUMBER_THREADS

from .enumeration_of_intervals import enumerate_intervals
from data.methods import get_counter_of_interval_prices

from ..small_tools import time_wrapper, multithreading

from config import main_logger


def divided_ids_interval(
    common_interval_ids: Tuple[int, int]
) -> List[Tuple[int, int]]:
    intervals_ids = []
    distance_intervals = (
        common_interval_ids[1] -
        common_interval_ids[0]
    ) // NUMBER_THREADS
    iter_left_border = common_interval_ids[0]

    for _ in range(NUMBER_THREADS):
        intervals_ids.append((
            iter_left_border,
            iter_left_border + distance_intervals - 1
        ))
        iter_left_border += distance_intervals
    # don't forget about last links
    intervals_ids[-1] = (intervals_ids[-1][0], common_interval_ids[1])
    return intervals_ids


@time_wrapper
def launch_collector_links(type_links: Types_links) -> None:
    counter_intervals = get_counter_of_interval_prices(type_links)
    common_interval_ids = (0, counter_intervals)

    intervals_ids = divided_ids_interval(common_interval_ids)

    multithreading(
        enumerate_intervals,
        args=intervals_ids,
        type_links=type_links,
        lock=threading.Lock()
    )
    main_logger.info(f"start threads: {NUMBER_THREADS}")

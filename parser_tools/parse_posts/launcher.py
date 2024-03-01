from typing import List, Tuple

from config import main_logger

from config import NUMBER_THREADS

from .manager import parse_posts_from_links

from ..small_tools import time_wrapper, multithreading


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
def launch_saver_posts(
    links: List[str],
    with_counter_views: bool = False
) -> None:
    counter_links = len(links)
    common_interval_ids = (0, counter_links)

    intervals_ids: List[Tuple[int, int]] = \
        divided_ids_interval(common_interval_ids)

    divided_list_links = [
        links[interval[0]:interval[1]+1] for interval in intervals_ids
    ]

    multithreading(
        parse_posts_from_links,
        divided_list_links,
        with_counter_views=with_counter_views
    )

    main_logger.info(f"start threads parse posts: {NUMBER_THREADS}")

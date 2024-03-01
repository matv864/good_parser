from config import main_logger

from config import FOR_SALE_TYPE_LINKS, FINAL_PRICE_TYPE_LINKS

from parser_tools import (
    launch_finder_intervals,
    launch_collector_links,
    launch_saver_posts
)

from database import find_need_links
from data.methods import clean_intervals_files, clean_links_files


# we found good intervals, in which good counter of posts
def start_parser():
    clean_intervals_files()
    clean_links_files()
    main_logger.info("start collect intervals")
    launch_finder_intervals(FOR_SALE_TYPE_LINKS)
    launch_finder_intervals(FINAL_PRICE_TYPE_LINKS)
    main_logger.info("finish collect intervals")

    main_logger.info("start collect links")
    launch_collector_links(FOR_SALE_TYPE_LINKS)
    launch_collector_links(FINAL_PRICE_TYPE_LINKS)
    main_logger.info("finish collect links")

    main_logger.info("start searching need links")
    links_moving_to_sold: list[str] = find_need_links()
    main_logger.info("finish searching need links")

    main_logger.info("start parse links")
    launch_saver_posts(links_moving_to_sold, with_counter_views=True)
    main_logger.info("finish parse need links")

from config import main_logger

from config import FINAL_PRICE_TYPE_LINKS, FOR_SALE_TYPE_LINKS

from parser_tools import (
    launch_finder_intervals,
    launch_collector_links,
    launch_saver_posts
)

from data.methods import (
    clean_intervals_files,
    clean_links_files,
    get_links_from_site
)


def start_parser() -> None:
    clean_intervals_files()
    clean_links_files()
    main_logger.info("start collect intervals")
    launch_finder_intervals(FINAL_PRICE_TYPE_LINKS)
    launch_finder_intervals(FOR_SALE_TYPE_LINKS)
    main_logger.info("finish collect intervals")

    main_logger.info("start collect links")
    launch_collector_links(FINAL_PRICE_TYPE_LINKS)
    launch_collector_links(FOR_SALE_TYPE_LINKS)
    main_logger.info("finish collect links")

    main_logger.info("start parsing")
    all_links = get_links_from_site(FINAL_PRICE_TYPE_LINKS)
    all_links += get_links_from_site(FOR_SALE_TYPE_LINKS)
    launch_saver_posts(all_links)
    main_logger.info("finish parsing")

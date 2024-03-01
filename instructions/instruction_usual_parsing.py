from config import main_logger

from config import FOR_SALE_TYPE_LINKS, FINAL_PRICE_TYPE_LINKS

from parser_tools import (
    set_fresh_links,
    launch_saver_posts
)
from data.methods import get_links_from_site, clean_links_files


def start_parser():
    clean_links_files()
    main_logger.info("start usual_mode")
    clean_links_files()
    main_logger.info("start collect links")
    set_fresh_links(FOR_SALE_TYPE_LINKS)
    set_fresh_links(FINAL_PRICE_TYPE_LINKS)
    main_logger.info("finish collect links")
    main_logger.info("start parsing pages")
    unsold_links: list[str] = get_links_from_site(FOR_SALE_TYPE_LINKS)
    sold_links: list[str] = get_links_from_site(FINAL_PRICE_TYPE_LINKS)

    launch_saver_posts(unsold_links)
    launch_saver_posts(sold_links, with_counter_views=True)
    main_logger.info("finish parsing pages")

from typing import List

from ..working_with_site import parse_post
from database import send_info


def parse_posts_from_links(
    links: List[str],
    with_counter_views: bool = False
) -> None:
    for link in links:
        algorithm_post(link, with_counter_views=with_counter_views)


def algorithm_post(
    link: str,
    with_counter_views: bool = False
) -> None:
    try:
        data_about_post = parse_post(link)
        if data_about_post is None:
            return
        data, target_id = data_about_post

        if with_counter_views:
            bostad_link = f"https://www.hemnet.se/bostad/{target_id}"

            data_about_post = parse_post(bostad_link)
            if data_about_post is None:
                return
            deactivated_data, _ = data_about_post

            counter_views = deactivated_data["timesViewed"]
            data["timesViewed"] = counter_views

    except Exception as e:
        print("exception error", type(e), str(e))
        return

    send_info(data, target_id)

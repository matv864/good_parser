from typing import Optional

from config import main_logger

from local_types import Types_links

from .request_to_page import request_to_page


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


def get_counter_of_links_from_page(
    min_price: int,
    max_price: int,
    type_links: Types_links
) -> Optional[int]:
    try:
        link = generate_link(
            min_price=min_price,
            max_price=max_price,
            type_links=type_links,
            page=1
        )
        data_json = request_to_page(link)

        temp_dict = data_json["props"]["pageProps"]["__APOLLO_STATE__"]
        temp_dict = temp_dict["ROOT_QUERY"]
        for key in temp_dict.keys():
            if type(temp_dict[key]) is dict:
                if "cards" in temp_dict[key].keys():
                    return temp_dict[key]["total"]
        else:
            main_logger.error(
                "troubles with keys of json, catch None " +
                f"{min_price}-{max_price}-{type_links}"
            )

    except KeyError as e:
        main_logger.error(f"NOT THIS KEY IN JSON: {str(e)}")
    except Exception as e:
        main_logger.critical(
            f"I DON'T KNOW WHAT IS THIS {type(e)} --- {str(e)}"
        )

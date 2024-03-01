from typing import List, Optional

from config import main_logger

from ..small_tools import try_decorator
from .request_to_page import request_to_page


@try_decorator
def get_links(link: str) -> List:  # List[?]
    all_links_on_page: List[str] = []
    data_json: Optional[dict] = request_to_page(link)
    assert not (data_json is None)

    temp_dict = data_json["props"]["pageProps"]["__APOLLO_STATE__"]
    temp_dict = temp_dict["ROOT_QUERY"]
    for key in temp_dict.keys():
        if type(temp_dict[key]) is dict:
            if "cards" in temp_dict[key].keys():
                raw_cards = temp_dict[key]["cards"]
                break
    else:
        main_logger.error(
            "troubles with keys of json, catch None " +
            f"{link}"
        )
        assert 1 == 1

    names_of_cards: List[str] = [raw_card["__ref"] for raw_card in raw_cards]
    temp_dict: dict = data_json["props"]["pageProps"]["__APOLLO_STATE__"]

    for name_card in names_of_cards:
        json_card: Optional[dict] = temp_dict.get(name_card)
        if json_card is None:
            main_logger.error("no_json_card")
            continue
        if "SaleCard" in name_card:
            link = "salda/" + temp_dict[name_card]["slug"]
        elif "ListingCard" in name_card:
            link = "bostad/" + temp_dict[name_card]["slug"]
        link = "https://www.hemnet.se/" + link
        all_links_on_page.append(link)

    return all_links_on_page

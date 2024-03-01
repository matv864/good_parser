from typing import List

from datetime import datetime

from .request_to_page import request_to_page
from data.methods import save_error
from ..small_tools import try_decorator

from .tools_for_page_info import (
    pop_none,
    format_integer,
    check_balkon,
    check_and_get_properties,
    make_full_address
)

RULES_SITE_DATA = {
    "fullAddress": ["streetAddress"],
    "bedrooms": ["numberOfRooms"],
    "housingType": ["housingForm", "name"],
    "releaseForm": ["tenure", "name"],
    "yearOfConstruction": ["legacyConstructionYear"],
    "livingArea": ["livingArea"],
    "plotArea": ["landArea"],
    "operatingCost": ["runningCosts", "amount"],
    "dateOfPublish": ["publishedAt"],
    "dateOfSell": ["soldAt"]
}


def instruction_common(
    data_about_post: dict,
    json_from_site: dict
) -> None:
    for key_our_data, keys_for_site_data in RULES_SITE_DATA.items():
        data_about_post[key_our_data] = \
            check_and_get_properties(json_from_site, *keys_for_site_data)

    data_about_post["balcon"] = check_balkon(json_from_site)


def instruction_for_sold(
    data_about_post: dict,
    json_from_site: dict
) -> int:
    data_about_post["price"] = \
        check_and_get_properties(json_from_site, "askingPrice", "amount")
    data_about_post["priceSold"] = \
        check_and_get_properties(json_from_site, "sellingPrice", "amount")

    sold_id = check_and_get_properties(json_from_site, "id")
    data_about_post["urlSold"] = f"https://www.hemnet.se/salda/{sold_id}"

    target_id = int(json_from_site.get("listingId"))

    return target_id


def instruction_for_unsold(
    data_about_post: dict,
    json_from_site: dict
) -> int:
    data_about_post["timesViewed"] = \
        check_and_get_properties(json_from_site, "timesViewed")

    data_about_post["price"] = \
        format_integer(
            check_and_get_properties(
                json_from_site,
                "priceChange",
                "originalPrice",
                "formatted"
            )
        )

    data_about_post["priceSold"] = \
        check_and_get_properties(json_from_site, "askingPrice", "amount")
    if data_about_post["price"] is None:
        data_about_post["price"] = data_about_post["priceSold"]

    target_id = int(json_from_site.get("id"))

    return target_id


def instruction_for_deactivated(
    data_about_post: dict,
    json_from_site: dict
) -> int:
    counter_views = 0
    temp_dict: List | None = \
        check_and_get_properties(json_from_site, "breadcrumbs")
    for element in temp_dict:
        counter_views += element.get("totalHits", 0)
    data_about_post["timesViewed"] = counter_views

    temp = check_and_get_properties(json_from_site, "soldListing")
    sold_id = temp["__ref"].split(":")[1]
    data_about_post["soldUrl"] = f"https://www.hemnet.se/salda/{sold_id}"

    target_id = int(json_from_site.get("id"))

    return target_id


@try_decorator
def parse_post(link: str) -> tuple[dict, int] | None:
    data_about_post: dict[str, str | int] = dict()

    json_from_site: dict = request_to_page(link)
    try:
        json_from_site = json_from_site["props"]["pageProps"]
        json_apollo = json_from_site["__APOLLO_STATE__"]
    except Exception as type_error:
        save_error(
            text=str(json_apollo),
            name_of_part="watch_json_from_page",
            type_error=type_error
        )

    unsold_word = "ActivePropertyListing"
    deactivated_word = "Deactivated"
    sold_word = "SoldPropertyListing"

    try:
        # it must 1 key
        need_key = [key for key in json_apollo.keys()
                    if unsold_word in key or
                    deactivated_word in key or
                    sold_word in key]
        if len(need_key) == 2:
            need_key = [key for key in need_key if deactivated_word in key][0]
            data_about_post["linkStatus"] = "deactivated"
        elif unsold_word in need_key[0]:
            need_key = need_key[0]
            data_about_post["linkStatus"] = "unsold"
        elif sold_word in need_key[0]:
            need_key = need_key[0]
            data_about_post["linkStatus"] = "sold"

        json_from_site = json_apollo[need_key]
    except Exception as type_error:
        save_error(
            text=str(json_from_site),
            name_of_part="find_need_key_post",
            type_error=type_error
        )
        return None

    instruction_common(
        data_about_post,
        json_from_site
    )
    if data_about_post.get("dateOfPublish"):
        data_about_post["dateOfPublish"] = datetime.fromtimestamp(
            float(data_about_post["dateOfPublish"])
        ).strftime(r'%Y-%m-%d')
    if data_about_post.get("dateOfSell"):
        data_about_post["dateOfSell"] = datetime.fromtimestamp(
            float(data_about_post["dateOfSell"])
        ).strftime(r'%Y-%m-%d')

    # other pages - other methods (in rare part od data)
    match data_about_post["linkStatus"]:
        case "deactivated":
            target_id: int = instruction_for_deactivated(
                data_about_post,
                json_from_site
            )
        case "unsold":
            target_id: int = instruction_for_unsold(
                data_about_post,
                json_from_site
            )
        case "sold":
            target_id: int = instruction_for_sold(
                data_about_post,
                json_from_site
            )

    data_about_post["fullAddress"] = make_full_address(
        json_apollo,
        data_about_post["fullAddress"]
    )

    link_status = data_about_post.pop("linkStatus")
    if link_status == "unsold":
        data_about_post["saleStatus"] = "unsold"
    else:
        data_about_post["saleStatus"] = "sold"

    data_about_post["url"] = f"https://www.hemnet.se/bostad/{target_id}"

    pop_none(data_about_post)

    if "yearOfConstruction" in data_about_post.keys():
        if "-" in data_about_post["yearOfConstruction"]:
            data_about_post["yearOfConstruction"] = \
                data_about_post["yearOfConstruction"].split("-")[1]

    return data_about_post, target_id

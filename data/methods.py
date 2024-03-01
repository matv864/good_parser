from typing import List, Tuple, Literal

from config import main_logger

from local_types import Types_links


def clean_intervals_files() -> None:
    with open("data/intervals/final_price.txt", "w"):
        pass
    with open("data/intervals/for_sale.txt", "w"):
        pass


def clean_links_files() -> None:
    with open("data/intervals/final_price.txt", "w"):
        pass
    with open("data/intervals/for_sale.txt", "w"):
        pass


def get_counter_of_interval_prices(type_links: Types_links) -> int:
    with open(f"data/intervals/{type_links.filename}.txt") as F:
        counter_lines = len(F.readlines())
    return counter_lines


def get_slice_of_interval_ids(
    left_border: int,
    right_border: int,
    type_links: Types_links
) -> List:
    # (min_price, max_price, counter)
    result_intervals: List[Tuple[int, int, int]] = []
    with open(f"data/intervals/{type_links.filename}.txt") as F:
        slice = list(F.readlines())[left_border:right_border+1]
    for line_interval in slice:
        if line_interval:
            min_price, max_price, counter = line_interval.split()
            need_interval = (int(min_price), int(max_price), int(counter))
            result_intervals.append(need_interval)
    return result_intervals


def save_links(
    links: List[str],
    type_links: Types_links,
    method: Literal["a", "w"] = "a"
) -> None:
    with open(f"data/links/{type_links.filename}.txt", method) as F:
        print(*links, sep="\n", file=F)


def get_links_from_site(type_links: Types_links) -> List[str]:
    with open(f"data/links/{type_links.filename}.txt", "r") as F:
        links_from_site: List[str] = F.read().split("\n")
    # delete empty elements
    return list(filter(bool, links_from_site))


def delete_link_duplications(type_links: Types_links) -> None:
    links_with_duplications: List[str] = get_links_from_site(type_links)
    links_without_duplications = list(set(links_with_duplications))

    counter_links_without_duplications = len(links_without_duplications)
    counter_links_with_duplications = len(links_with_duplications)
    counter_lost_links = counter_links_with_duplications - \
        counter_links_without_duplications

    message = f"delete duplications and lost: {counter_lost_links} links"
    main_logger.info(message)
    save_links(links_without_duplications, type_links, method="w")


def save_error(text: str, name_of_part: str, type_error: Exception) -> None:
    valid_format_error = str(type(type_error)).replace("<", "_")
    valid_format_error = valid_format_error.replace(">", "_")
    valid_format_error = valid_format_error.replace("'", "_")
    filename = f"{name_of_part}_{valid_format_error}"
    main_logger.error(f"save_error: {str(type_error)}-{filename}")
    with open(f"data/errors/{filename}", "w", encoding="utf-8") as F:
        F.write(text)

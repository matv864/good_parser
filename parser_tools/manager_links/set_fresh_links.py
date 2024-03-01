from local_types import Types_links

from ..working_with_site import get_links
from data.methods import save_links

from ..small_tools import time_wrapper


def generate_links(url: str, page: int) -> str:
    link = f"{url}?by=creation&order=desc&page={page}"
    return link


@time_wrapper
def set_fresh_links(type_links: Types_links) -> None:
    all_fresh_links: list[str] = []
    url: str = type_links.link
    for page in range(1, 51):
        link_to_site = generate_links(url, page)
        links: list[str] = get_links(link_to_site)
        all_fresh_links += links
    save_links(all_fresh_links, type_links)

import requests
from config import main_logger

from config import (
    LINK_TO_DATABASE,
    PATH_TO_GET_LINKS,
    PATH_TO_POST,
    HEADER_FOR_DATABASE,
    LIMIT_API
)


def try_decorator(func):
    def decor(*args, **kwargs):
        for _ in range(5):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                main_logger.error(f"{type(e)} --- {str(e)}")
        return None
    return decor


def get_links_by_page(page: int) -> str:
    link = LINK_TO_DATABASE + PATH_TO_GET_LINKS
    link += f"?page={page}&limit={LIMIT_API}"
    response = requests.get(link, headers=HEADER_FOR_DATABASE)
    return response.text


def send_info(data_post: dict | None, target_id: int) -> None:
    if data_post is None:
        return

    link = LINK_TO_DATABASE + PATH_TO_POST
    main_logger.info(str(data_post))
    if data_post.get("urlSold"):
        edit_post(data_post, link, target_id)
    else:
        create_post(data_post, link)


# bostad
@try_decorator
def create_post(data_post: dict, link: str) -> None:
    response = requests.post(
        link,
        json=data_post,
        headers=HEADER_FOR_DATABASE
    )
    main_logger.info(f'"post", {response.status_code}, {response.text}')


# salda
@try_decorator
def edit_post(data_post: dict, link: str, target_id: int) -> None:
    link += f"?id={target_id}"
    response = requests.patch(
        link,
        json=data_post,
        headers=HEADER_FOR_DATABASE
    )
    main_logger.info(f'"patch", {response.status_code}, {response.text}')

import os
import logging
import graypy
from dotenv import load_dotenv

from logging import Logger
from local_types import Types_links


load_dotenv()

PARSER_MODE = os.getenv("MODE")
GRAYLOG_URL = os.getenv("GRAYLOG_URL")
GRAYLOG_PORT = int(os.getenv("GRAYLOG_PORT"))
LINK_TO_DATABASE = os.getenv("API_URL")
NUMBER_THREADS = int(os.getenv("NUMBER_THREADS"))
LOGGING_MODE = os.getenv("LOGGING_MODE")
USING_PROXY = bool(int(os.getenv("USING_PROXY")))

# links
FOR_SALE_TYPE_LINKS = Types_links(
    # INSERT DATA
)

FINAL_PRICE_TYPE_LINKS = Types_links(
    # INSERT DATA
)


PATH_TO_GET_LINKS = ""  # INSERT DATA
PATH_TO_POST = ""  # INSERT DATA

# interval prices
COMMON_INTERVAL_PRICE = (0, 0)  # INSERT DATA

# for requests
# hemnet can't show >2500 posts by filter settings
MAX_LINK_ON_FILTER_SETTINGS = 1  # INSERT DATA
MAX_LINK_ON_PAGE = 1  # INSERT DATA

HEADER_FOR_HEMNET = {
    "User-Agent": "Mozilla/5.0"
}

HEADER_FOR_DATABASE = {
    # INSERT DATA
}

LIMIT_API = 1  # INSERT DATA


# logging
def launch_logging() -> Logger:
    main_logger = logging.getLogger("hemnet-parser")
    match LOGGING_MODE:
        case "DEBUG":
            main_logger.setLevel(logging.DEBUG)
        case "INFO":
            main_logger.setLevel(logging.INFO)
        case "ERROR":
            main_logger.setLevel(logging.ERROR)
        case _:
            main_logger.setLevel(logging.INFO)

    # Хендлер для stdout
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    main_logger.addHandler(console_handler)

    # Хендлер для Graylog
    graylog_handler = graypy.GELFUDPHandler(
        GRAYLOG_URL,
        GRAYLOG_PORT
    )
    graylog_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    graylog_handler.setFormatter(graylog_formatter)

    main_logger.addHandler(graylog_handler)

    return main_logger


main_logger: Logger = launch_logging()

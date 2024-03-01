from typing import List, Optional

import os.path
from config import main_logger

# proxies = [
#     None,
#     {"https":"https://counternum:counternum@45.134.252.138:8542"},
#     {"https":"https://counternum:counternum@46.8.57.191:8542"},
#     {"https":"https://counternum:counternum@188.130.184.93:8542"},
#     {"https":"https://counternum:counternum@109.248.14.81:8542"},
#     {"https":"https://counternum:counternum@45.89.19.14:8542"},
# ]


def get_proxies() -> List[Optional[dict]]:
    proxies: List[Optional[dict]] = []

    proxies_file_path = "proxies.txt"

    if not os.path.exists(proxies_file_path):
        main_logger.error("NO FILE PROXIES")
        return [None]

    with open(proxies_file_path, "r") as F:
        for proxy in F.read().split():
            if proxy:
                proxies.append({"https": f"https://{proxy}"})
    if len(proxies) == 0:
        main_logger.error("NO PROXY")
        return [None]
    proxies.append(None)
    return proxies

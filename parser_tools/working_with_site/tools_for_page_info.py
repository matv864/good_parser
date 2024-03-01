

def pop_none(data: dict):
    data_keys = list(data.keys())
    for key in data_keys:
        if data.get(key, "not None") is None:
            data.pop(key)


def format_integer(string: str | None) -> str:
    # 1&nbsp;995&nbsp;000&nbsp;kr
    if string is None:
        return None
    string = string.replace("\xa0", "").replace("kr", "")
    return str(int(string))


def check_balkon(json_from_site: dict):
    temp_dict: list | None = json_from_site.get("relevantAmenities")
    if temp_dict is None:
        return None
    for element in temp_dict:
        if "BALCONY" == element.get("kind"):
            return element.get("isAvailable")
    return False


def check_and_get_properties(
    json_from_site: dict,
    *keys: list[str]
) -> str | int:
    temp_dict = json_from_site
    for key in keys:
        temp_dict = temp_dict.get(key)
        if temp_dict is None:
            return None
    return temp_dict


def make_full_address(
    json_from_site: dict,
    small_address: str
) -> str | None:
    postal_city = None
    city = None
    district = None
    municipality = None
    for key in json_from_site.keys():
        if "Location" in key:
            location_object = json_from_site[key]
            match location_object["type"]:
                case "CITY":
                    city = location_object["fullName"]
                case "POSTAL_CITY":
                    postal_city = location_object["fullName"]
                case "DISTRICT":
                    district = location_object["fullName"]
                case "MUNICIPALITY":
                    municipality = location_object["fullName"]
    if city is None:
        city = postal_city
    if city is None:
        city = district
    city = city.replace(" tätort", "")

    full_address = f"{small_address};{city};{municipality}"
    return full_address

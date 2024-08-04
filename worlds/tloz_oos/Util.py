from typing import Dict
from .data import BASE_LOCATION_ID, LOCATIONS_DATA, BASE_ITEM_ID, ITEMS_DATA


def build_location_name_to_id_dict() -> Dict[str, int]:
    location_name_to_id: Dict[str, int] = {}
    current_index = BASE_LOCATION_ID
    for loc_name in LOCATIONS_DATA:
        location_name_to_id[loc_name] = current_index
        current_index += 1
    return location_name_to_id


def build_item_name_to_id_dict() -> Dict[str, int]:
    item_name_to_id: Dict[str, int] = {}
    current_index = BASE_ITEM_ID
    for item_name in ITEMS_DATA.keys():
        item_name_to_id[item_name] = current_index
        current_index += 1
    return item_name_to_id


def build_item_id_to_name_dict() -> Dict[int, str]:
    item_id_to_name: Dict[int, str] = {}
    current_index = BASE_ITEM_ID
    for item_name in ITEMS_DATA.keys():
        item_id_to_name[current_index] = item_name
        current_index += 1
    return item_id_to_name


def get_prices_pool():
    prices_pool = [300]                 # 1%
    prices_pool.extend([200] * 7)       # 8%
    prices_pool.extend([100] * 42)      # 50%
    prices_pool.extend([80] * 15)       # 65%
    prices_pool.extend([60] * 15)       # 80%
    prices_pool.extend([40] * 15)       # 95%
    prices_pool.extend([20] * 4)        # 99%
    prices_pool.append(0)               # 100%
    return prices_pool


def get_old_man_values_pool():
    old_man_values_pool = [400]                 # 1%
    old_man_values_pool.extend([300] * 5)       # 6%
    old_man_values_pool.extend([200] * 14)      # 20%
    old_man_values_pool.extend([100] * 40)      # 60%
    old_man_values_pool.extend([50] * 20)       # 80%
    old_man_values_pool.extend([25] * 15)       # 95%
    old_man_values_pool.extend([10] * 4)        # 99%
    old_man_values_pool.append(1)               # 100%
    return old_man_values_pool

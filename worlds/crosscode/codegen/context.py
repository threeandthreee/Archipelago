from dataclasses import dataclass, field
import typing
import os
import json

from .util import get_json_object, load_json_with_includes


@dataclass
class Context:
    rando_data: dict[str, typing.Any]
    item_data: list[typing.Dict[str, typing.Any]]
    database: dict[str, typing.Any]
    cached_location_ids: dict[str, int]
    num_items: int = field(init=False)

    def __post_init__(self):
        self.num_items = len(self.item_data)


def make_context_from_package(package: str, with_assets: bool = True) -> Context:
    master = load_json_with_includes(package, "data/in/master.json")

    cached_location_ids = {}
    try:
        cached_location_ids = get_json_object(package, "data/out/locations.json")
    except:
        pass

    if with_assets:
        return Context(
            master,
            get_json_object(package, "data/assets/data/item-database.json")["items"],
            get_json_object(package, "data/assets/data/database.json"),
            cached_location_ids
        )

    else:
        return Context(
            master,
            [],
            {},
            cached_location_ids
        )

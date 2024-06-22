from collections import defaultdict
from copy import deepcopy
import logging
import typing
import ast
import os
import json

import jinja2

from worlds.crosscode.codegen.jinja import create_jinja_extension

from ..types.regions import RegionsData

from .ast import AstGenerator
from .context import Context, make_context_from_package
from .emit import emit_dict, emit_list, emit_set
from .util import GENERATED_COMMENT
from .lists import ListInfo

cglogger = logging.getLogger("crosscode.codegen")

class FileGenerator:
    environment: jinja2.Environment
    ctx: Context
    common_args: typing.Dict[str, typing.Any]
    lists: ListInfo
    regions_data: dict[str, RegionsData]
    world_dir: str
    data_out_dir: str

    ast_generator: AstGenerator

    def __init__(self, world_dir: str, lists: typing.Optional[ListInfo] = None):
        data_out_dir = os.path.join(world_dir, "data", "out")
        template_dir = os.path.join(world_dir, "templates")

        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
        )

        if lists == None:
            self.ctx = make_context_from_package(world_dir.replace('/', '.'))
            self.lists = ListInfo(self.ctx)
            self.lists.build()
        else:
            self.lists = lists
            self.ctx = lists.ctx

        self.regions_data = {
            key: self.lists.json_parser.parse_regions_data(value)
            for key, value in self.ctx.rando_data["regions"].items()
        }

        self.world_dir = world_dir
        self.data_out_dir = data_out_dir

        self.ast_generator = AstGenerator()

        self.environment.add_extension(create_jinja_extension(self.ast_generator))

        self.common_args = {
            "generated_comment": GENERATED_COMMENT,
            "modes": self.ctx.rando_data["modes"],
            "default_mode": self.ctx.rando_data["defaultMode"],
        }

    def generate_python_file_locations(self):
        template = self.environment.get_template("locations.template.py")

        locations_complete = template.render(
            locations_data=self.lists.locations_data.values(),
            events_data=self.lists.events_data.values(),
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "locations.py"), "w") as f:
            f.write(locations_complete)

    def generate_python_file_items(self):
        template = self.environment.get_template("items.template.py")

        sorted_single_item_data = sorted(
            self.lists.single_items_dict.items(),
            key=lambda i: i[1].item_id
        )

        sorted_item_data = sorted(
            self.lists.items_dict.items(),
            key=lambda i: i[1].combo_id
        )

        items_complete = template.render(
            single_items_dict=sorted_single_item_data,
            items_dict=sorted_item_data,
            num_items=self.ctx.num_items,
            keyring_items=self.ctx.rando_data["keyringItems"],
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "items.py"), "w") as f:
            f.write(items_complete)

    def generate_python_file_item_pools(self):
        template = self.environment.get_template("item_pools.template.py")

        item_pools_complete = template.render(
            item_pools=self.lists.item_pools,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "item_pools.py"), "w") as f:
            f.write(item_pools_complete)

    def generate_python_file_prog_items(self):
        template = self.environment.get_template("prog_items.template.py")

        item_pools_complete = template.render(
            prog_chains=self.lists.progressive_chains,
            prog_items=self.lists.progressive_items,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "prog_items.py"), "w") as f:
            f.write(item_pools_complete)

    def generate_python_file_regions(self):
        template = self.environment.get_template("regions.template.py")

        regions_complete = template.render(
            modes_string=", ".join([f'"{x}"' for x in self.ctx.rando_data["modes"]]),
            region_packs=self.regions_data,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "regions.py"), "w") as f:
            f.write(regions_complete)

    def generate_python_file_vars(self):
        template = self.environment.get_template("vars.template.py")

        regions_complete = template.render(
            variable_definitions=self.lists.variable_definitions,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "vars.py"), "w") as f:
            f.write(regions_complete)

    def generate_python_files(self) -> None:
        self.generate_python_file_locations()
        self.generate_python_file_items()
        self.generate_python_file_item_pools()
        self.generate_python_file_prog_items()
        self.generate_python_file_regions()
        self.generate_python_file_vars()

    def generate_mod_files(self):
        merged_data = deepcopy(self.ctx.rando_data)

        data_out = {
            "items": defaultdict(lambda: defaultdict(dict)),
            "quests": defaultdict(dict),
        }

        def get_codes(name: str) -> list[int]:
            data = self.lists.locations_data
            if name in data:
                code = data[name].code
                if code is None:
                    raise RuntimeError(f"Trying to assign null code in {data}")
                return [code]

            result = []
            idx = 1
            while True:
                full_name = f"{name} - Reward {idx}"
                if full_name not in data:
                    break
                result.append(data[full_name].code)
                idx += 1

            return result

        for name, chest in merged_data["chests"].items():
            codes = get_codes(name)
            map_name = chest["location"]["map"]
            map_id = chest["location"]["mapId"]

            room = data_out["items"][map_name]
            room["chests"][map_id] = { "name": name, "mwids": codes }

        for name, cutscene in merged_data["cutscenes"].items():
            codes = get_codes(name)
            map_name = cutscene["location"]["map"]
            map_id = cutscene["location"]["mapId"]
            path = cutscene["location"]["path"]

            room = data_out["items"][map_name]
            if map_id not in room["cutscenes"]:
                room["cutscenes"][map_id] = []

            room["cutscenes"][map_id].append({ "mwids": codes, "path": path })

        for name, element in merged_data["elements"].items():
            codes = get_codes(name)
            map_name = element["location"]["map"]
            map_id = element["location"]["mapId"]

            room = data_out["items"][map_name]
            room["elements"][map_id] = { "mwids": codes }

        for name, quest in merged_data["quests"].items():
            codes = get_codes(name)
            quest_id = quest["questid"]
            if not quest_id in self.ctx.database["quests"]:
                cglogger.error(f"{quest_id} does not exist")

            room = data_out["quests"]
            room[quest_id] = { "mwids": codes }

        try:
            os.mkdir(self.data_out_dir)
        except FileExistsError:
            pass

        with open(os.path.join(self.data_out_dir, "data.json"), "w") as f:
            json.dump(data_out, f, indent='\t')

        with open(os.path.join(self.data_out_dir, "locations.json"), "w") as f:
            location_ids = { loc.name: loc.code for loc in self.lists.locations_data.values() }
            json.dump(location_ids, f, indent='\t')

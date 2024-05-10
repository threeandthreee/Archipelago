from collections import defaultdict
from copy import deepcopy
import sys
import typing
import ast
import os
import json

import jinja2

from worlds.crosscode.codegen.merge import merge

from .ast import AstGenerator
from .context import Context, make_context_from_package
from .emit import emit_dict, emit_list
from .util import BASE_ID, GENERATED_COMMENT, RESERVED_ITEM_IDS
from .lists import ListInfo


class FileGenerator:
    environment: jinja2.Environment
    ctx: Context
    common_args: typing.Dict[str, typing.Any]
    lists: ListInfo
    world_dir: str
    data_out_dir: str

    ast_generator: AstGenerator

    def __init__(self, world_dir: str, lists: typing.Optional[ListInfo] = None):
        data_out_dir = os.path.join(world_dir, "data", "out")
        template_dir = os.path.join(world_dir, "templates")

        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir))

        if lists == None:
            self.ctx = make_context_from_package(world_dir.replace('/', '.'))
            self.lists = ListInfo(self.ctx)
            self.lists.build()
        else:
            self.lists = lists
            self.ctx = lists.ctx

        self.world_dir = world_dir
        self.data_out_dir = data_out_dir

        self.ast_generator = AstGenerator()

        self.common_args = {
            "generated_comment": GENERATED_COMMENT,
            "modes": self.ctx.rando_data["modes"],
            "default_mode": self.ctx.rando_data["defaultMode"],
        }

    def generate_python_files(self) -> None:
        # LOCATIONS
        template = self.environment.get_template("locations.template.py")

        code_locations_data = emit_list([self.ast_generator.create_ast_call_location(loc) for loc in self.lists.locations_data.values()])
        code_events_data =  emit_list([self.ast_generator.create_ast_call_location(loc) for loc in self.lists.events_data.values()])

        locations_complete = template.render(locations_data=code_locations_data, events_data=code_events_data, **self.common_args)

        with open(os.path.join(self.world_dir, "locations.py"), "w") as f:
            f.write(locations_complete)

        # ITEMS
        template = self.environment.get_template("items.template.py")

        sorted_single_item_data = [(value.item_id, key, value) for key, value in self.lists.single_items_dict.items()]
        sorted_single_item_data.sort()

        code_single_item_dict = emit_dict([(ast.Constant(key), self.ast_generator.create_ast_call_single_item(value)) for _, key, value in sorted_single_item_data])

        sorted_item_data = [(value.combo_id, key, value) for key, value in self.lists.items_dict.items()]
        sorted_item_data.sort()

        item_dict_items = []
        for _, key, value in sorted_item_data:
            key = ast.Tuple(elts=[ast.Constant(x) for x in key])
            ast.fix_missing_locations(key)
            value = self.ast_generator.create_ast_call_item(value)
            item_dict_items.append((key, value))

        code_item_dict = emit_dict(item_dict_items)

        items_complete = template.render(
            single_items_dict=code_single_item_dict,
            items_dict=code_item_dict,
            num_items=self.ctx.num_items,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "items.py"), "w") as f:
            f.write(items_complete)

    def generate_mod_files(self):
        merged_data = deepcopy(self.ctx.rando_data)
        for addon in self.ctx.addons.values():
            merged_data = merge(merged_data, addon, True)

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
                print(f"{quest_id} does not exist", sys.stderr)

            room = data_out["quests"]
            room[quest_id] = { "mwids": codes }

        try:
            os.mkdir(self.data_out_dir)
        except FileExistsError:
            pass

        with open(os.path.join(self.data_out_dir, "data.json"), "w") as f:
            json.dump(data_out, f, indent='\t')

from collections import defaultdict
from copy import deepcopy
import logging
from posixpath import commonpath
import sys
import typing
import ast
import os
import json

import jinja2

from worlds.crosscode.codegen.merge import merge
from worlds.crosscode.types.regions import RegionsData

from .ast import AstGenerator
from .context import Context, make_context_from_package
from .emit import emit_dict, emit_list, emit_set
from .util import BASE_ID, GENERATED_COMMENT, RESERVED_ITEM_IDS
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
            loader=jinja2.FileSystemLoader(template_dir))

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

        code_keyring_items = emit_set(
            [ast.Constant(item) for item in self.ctx.rando_data["keyringItems"]]
        )

        items_complete = template.render(
            single_items_dict=code_single_item_dict,
            items_dict=code_item_dict,
            num_items=self.ctx.num_items,
            keyring_items=code_keyring_items,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "items.py"), "w") as f:
            f.write(items_complete)

        # ITEM POOLS
        template = self.environment.get_template("item_pools.template.py")

        code_item_pools = {
            name: emit_list([
                self.ast_generator.create_ast_call_item_pool_entry(entry)
                for entry in pool
            ])
            for name, pool in self.lists.item_pools.items()
        }

        item_pools_complete = template.render(
            item_pools=code_item_pools,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "item_pools.py"), "w") as f:
            f.write(item_pools_complete)

        # PROG ITEMS
        template = self.environment.get_template("prog_items.template.py")

        code_prog_chain_names = {
            name: chain.display_name for name, chain in self.lists.progressive_chains.items()
        }

        code_prog_items = emit_dict([
            (ast.Constant(name), self.ast_generator.create_ast_call_item_ref(item))
            for name, item in self.lists.progressive_items.items()
        ])

        code_prog_chain_lists = {
            name: emit_list([
                self.ast_generator.create_ast_call_progressive_chain_entry(entry)
                for entry in chain.items
            ])
            for name, chain in self.lists.progressive_chains.items()
        }

        item_pools_complete = template.render(
            prog_chain_names=code_prog_chain_names,
            prog_items=code_prog_items,
            prog_chain_lists=code_prog_chain_lists,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "prog_items.py"), "w") as f:
            f.write(item_pools_complete)

        # REGIONS
        template = self.environment.get_template("regions.template.py")

        region_lists = {
            mode: emit_list([ast.Constant(r) for r in regions.region_list])
            for mode, regions in self.regions_data.items()
        }

        region_connections = {
            mode: emit_list([
                self.ast_generator.create_ast_call_region_connection(rc) for rc in regions.region_connections
            ])
            for mode, regions in self.regions_data.items()
        }

        regions_complete = template.render(
            modes_string=", ".join([f'"{x}"' for x in self.ctx.rando_data["modes"]]),
            region_packs=self.regions_data,
            region_lists=region_lists,
            region_connections=region_connections,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "regions.py"), "w") as f:
            f.write(regions_complete)

        # VARS
        template = self.environment.get_template("vars.template.py")

        code_var_defs = defaultdict(dict)

        for name, values in self.lists.variable_definitions.items():
            for val, conds in values.items():
                code_var_defs[name][val] = emit_list(
                    [self.ast_generator.create_ast_call_condition(c) for c in conds]
                )

        regions_complete = template.render(
            code_var_defs=code_var_defs,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "vars.py"), "w") as f:
            f.write(regions_complete)

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

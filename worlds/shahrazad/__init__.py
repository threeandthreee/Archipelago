from BaseClasses import Item, ItemClassification
from .options import ShahrazadOptions
from ..AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule


class ShahrazadWeb(WebWorld):
    tutorials = []


class ShahrazadItem(Item):
    game = "Shahrazad"


class ShahrazadWorld(World):
    game = "Shahrazad"
    topology_present = False
    item_name_to_id = {}  # will fill in stage_generate_basic()
    base_id = 980
    location_name_to_id = {
        "": -1001,
    }
    web = ShahrazadWeb()
    options_dataclass = ShahrazadOptions
    options: ShahrazadOptions
    item_pool_names: {}
    # random_start: []

    def stage_generate_early(multiworld: "MultiWorld"):
        cls = ShahrazadWorld
        victims = {}
        id = cls.base_id
        for world in multiworld.get_game_worlds(cls.game):
            for victim in world.options.victims.value:
                victims[f"{victim} Start"] = id
                id += 1

        cls.item_name_to_id = victims

        # update datapackage checksum
        import worlds
        worlds.network_data_package["games"][cls.game] = cls.get_data_package_data()

    def generate_early(self):
        self.item_pool_names = {}
        for player in self.multiworld.player_ids:
            if self.multiworld.player_name[player] in self.options.victims.value:
                item_name = f"{self.multiworld.player_name[player]} Start"
                self.item_pool_names[player] = item_name

    def create_item(self, name: str) -> Item:
        assert self.item_name_to_id[name]
        return ShahrazadItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        item_pool = []
        for item in self.item_pool_names.values():
            item_pool.append(self.create_item(item))
            # this will make more items than locations, i don't want to make a
            # client so nothing i can really do about that besides try and
            # steal filler from others but I'd rather let core do that

        self.random.shuffle(item_pool)

        for _ in range(self.options.random_start.value):
            if item_pool:
                start_item = item_pool.pop()
                print(f"start item: {start_item.name}")
                self.multiworld.push_precollected(start_item)
                # self.random_start = [start_item]
            else:
                print(f"tried to add more games to start than games locked")

        self.multiworld.itempool += item_pool

    # here's hoping i don't actually need this
    # def get_pre_fill_items():
    #     if self.option.random_start:
    #         print("HEY I CHECKED FOR PREFILLED ITEMS")
    #         return self.random_start
    #     else:
    #         return []

    def generate_basic(self):
        for victim_id, item_name in self.item_pool_names.items():
            menu = self.multiworld.get_region("Menu", victim_id)
            self.multiworld.worlds[victim_id].options.progression_balancing.value = 0
            for exit in menu.exits:
                add_rule(exit, lambda state, item_name=item_name: state.has(item_name, self.player))
            if menu.locations:
                print(
                    f"found {len(menu.locations)} locations in menu "
                    f"for victim {self.multiworld.player_name[victim_id]}, "
                    f"applying access rules, this may slow generation down considerably")
                for location in menu.locations:
                    add_rule(location, lambda state, item_name=item_name: state.has(item_name, self.player))
            if self.options.hint_game_start:
                self.options.start_hints.value.add(item_name)

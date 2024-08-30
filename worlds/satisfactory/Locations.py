from typing import List, Optional, Callable, Tuple, Dict, Iterable, ClassVar
from BaseClasses import CollectionState
from .GameLogic import GameLogic, Recipe, Building, PowerInfrastructureLevel
from .StateLogic import StateLogic, EventId, part_event_prefix, building_event_prefix
from .Items import Items


class LocationData():
    region: str
    name: str
    event_name: str
    code: Optional[int]
    rule: Optional[Callable[[CollectionState], bool]]

    def __init__(self, region: str, name: str, code: Optional[int], event_name: Optional[str] = None,
                 rule: Optional[Callable[[CollectionState], bool]] = None):
        self.region = region
        self.name = name
        self.code = code
        self.rule = rule
        self.event_name = event_name or name


class Part(LocationData):
    @staticmethod
    def get_parts(state_logic: StateLogic, recipes: Tuple[Recipe, ...], name: str, items: Items) -> List[LocationData]:
        recipes_per_region: Dict[str, List[Recipe]] = {}

        for recipe in recipes:
            recipes_per_region.setdefault(recipe.building or "Overworld", []).append(recipe)

        return [Part(state_logic, region, recipes_for_region, name, items) 
                for region, recipes_for_region in recipes_per_region.items()]

    def __init__(self, state_logic: StateLogic, region: str, recipes: Iterable[Recipe], name: str, items: Items):
        super().__init__(region, part_event_prefix + name + region, EventId, part_event_prefix + name,
            self.can_produce_any_recipe_for_part(state_logic, recipes, name, items))

    def can_produce_any_recipe_for_part(self, state_logic: StateLogic, recipes: Iterable[Recipe], 
                                        name: str, items: Items) -> Callable[[CollectionState], bool]:
        def can_build_by_any_recipe(state: CollectionState) -> bool:
            return any(state_logic.can_produce_specific_recipe_for_part(state, recipe) for recipe in recipes)

        def can_build_by_precalculated_recipe(state: CollectionState) -> bool:
            return state_logic.can_produce_specific_recipe_for_part( 
                state, items.precalculated_progression_recipes[name])

        if items.precalculated_progression_recipes:
            return can_build_by_precalculated_recipe
        else:
            return can_build_by_any_recipe


class EventBuilding(LocationData):
    def __init__(self, game_logic: GameLogic, state_logic: StateLogic, building_name: str, building: Building):
        super().__init__("Overworld", building_event_prefix + building_name, EventId, 
            rule = self.can_create_building(game_logic, state_logic, building))

    def can_create_building(self, game_logic: GameLogic, state_logic: StateLogic, building: Building
            ) -> Callable[[CollectionState], bool]:

        def can_build(state: CollectionState) -> bool:
            return state_logic.has_recipe(state, building) \
                and state_logic.can_power(state, building.power_requirement) \
                and state_logic.can_produce_all_allowing_handcrafting(state, game_logic, building.inputs)

        return can_build


class PowerInfrastructure(LocationData):
    def __init__(self, game_logic: GameLogic, state_logic: StateLogic, 
                 powerLevel: PowerInfrastructureLevel, recipes: Iterable[Recipe]):
        super().__init__("Overworld", building_event_prefix + str(powerLevel), EventId, 
            rule = self.can_create_power_infrastructure(game_logic, state_logic, powerLevel, recipes))

    def can_create_power_infrastructure(self, game_logic: GameLogic, state_logic: StateLogic, 
                                        powerLevel: PowerInfrastructureLevel, recipes: Iterable[Recipe]
            ) -> Callable[[CollectionState], bool]:

        def can_power(state: CollectionState) -> bool:
            return any(state_logic.can_power(state, level) for level in PowerInfrastructureLevel if level > powerLevel)\
                or any(state_logic.can_build(state, recipe.building) and 
                       state_logic.can_produce_all_allowing_handcrafting(state, game_logic, recipe.inputs) 
                        for recipe in recipes)

        return can_power


class ElevatorTier(LocationData):
    def __init__(self, tier: int, state_logic: StateLogic, game_logic: GameLogic):
        super().__init__("Overworld", f"Elevator Tier {tier + 1}", EventId,
            rule = lambda state: state_logic.can_build(state, "Space Elevator") and \
                                 state_logic.can_produce_all(state, game_logic.space_elevator_tiers[tier].keys()))


class HubSlot(LocationData):
    def __init__(self, tier: int, milestone: int, slot: int, locationId: int):
        super().__init__(f"Hub {tier}-{milestone}", f"Hub {tier}-{milestone}, item {slot}", locationId)


class MamSlot(LocationData):
    def __init__(self, tree: str, nodeName: str, locationId: int):
        super().__init__(f"{tree}: {nodeName}", f"{tree}: {nodeName}", locationId)


class ShopSlot(LocationData):
    def __init__(self, state_logic: Optional[StateLogic], slot: int, cost: int, locationId: int):
        super().__init__("AWESOME Shop", f"AWESOME Shop purchase {slot}", locationId,
            rule = self.can_purchase_from_shop(state_logic, cost))
        
    def can_purchase_from_shop(self, state_logic: Optional[StateLogic], cost) -> Callable[[CollectionState], bool]:
        def can_purchase(state: CollectionState) -> bool:
            if not state_logic or cost < 20:
                return True
            elif (cost >= 20 and cost < 50):
                return state_logic.is_game_phase(state, 1)
            elif (cost >= 50 and cost < 100):
                return state_logic.is_game_phase(state, 2)
            else:
                return state_logic.is_game_phase(state, 3)
            
        return can_purchase


class Droppod(LocationData):
    def __init__(self, x: int, y: int, z: int, unlocked_by: str, state_logic: Optional[StateLogic],
            locationId: int, needs_power: Optional[bool] = False, gassed: Optional[bool] = False,
            radioactive: Optional[bool] = False):

        def get_region(gassed: bool, radioactive: bool) -> str:
            if radioactive:
                return "Radioactive Area"
            elif gassed:
                return "Gas Area"
            else:
                return "Overworld"

        def get_rule(unlocked_by: str, needs_power: bool) -> Callable[[CollectionState], bool]:
            #TODO handle power

            def logic_rule(state: CollectionState):
                return state_logic and state_logic.can_produce(state, unlocked_by)

            return logic_rule

        super().__init__(get_region(gassed, radioactive), f"Crash Site ({x}, {y}, {z})", locationId,
                rule = get_rule(unlocked_by, needs_power))


class Locations():
    game_logic: Optional[GameLogic]
    state_logic: Optional[StateLogic]
    items: Optional[Items]

    hub_location_start: ClassVar[int] = 1338000
    max_tiers: ClassVar[int] = 10
    max_milestones: ClassVar[int] = 5
    max_slots: ClassVar[int] = 10

    def __init__(self, game_logic: Optional[GameLogic] = None,
                 state_logic: Optional[StateLogic] = None, items: Optional[Items] = None):
        self.game_logic = game_logic
        self.state_logic = state_logic
        self.items = items

    def get_base_location_table(self) -> List[LocationData]:
        return [
            # Hardcoded locations, like pickups on the map
            #Droppod(0, 0, 0, "Motor", self.state_logic, 1337605)),
            #Droppod(0, 0, 0, "Motor", self.state_logic, 1337605)),
            #Droppod(0, 0, 0, "Motor", self.state_logic, 1337605)),

            MamSlot("Alien Organisms", "Inflated Pocket Dimension", 1338500),
            MamSlot("Alien Organisms", "Hostile Organism Detection", 1338501),
            MamSlot("Alien Organisms", "Expanded Toolbelt", 1338502),
            MamSlot("Alien Organisms", "Bio-Organic Properties", 1338503),
            MamSlot("Alien Organisms", "Stinger Research", 1338504),
            MamSlot("Alien Organisms", "Hatcher Research", 1338505),
            MamSlot("Alien Organisms", "Hog Research", 1338506),
            MamSlot("Alien Organisms", "Spitter Research", 1338507),
            MamSlot("Alien Organisms", "Structural Analysis", 1338508),
            MamSlot("Alien Organisms", "Protein Inhaler", 1338509),
            MamSlot("Alien Organisms", "The Rebar Gun", 1338510),
            MamSlot("Caterium", "Caterium Electronics", 1338511),
            MamSlot("Caterium", "Bullet Guidance System", 1338512),
            MamSlot("Caterium", "High-Speed Connector", 1338513),
            MamSlot("Caterium", "Caterium", 1338514),
            MamSlot("Caterium", "Caterium Ingots", 1338515),
            MamSlot("Caterium", "Quickwire", 1338516),
            MamSlot("Caterium", "Power Switch", 1338517),
            MamSlot("Caterium", "Power Poles Mk.2", 1338518),
            MamSlot("Caterium", "AI Limiter", 1338519),
            MamSlot("Caterium", "Smart Splitter", 1338520),
            MamSlot("Caterium", "Programmable Splitter", 1338521),
            MamSlot("Caterium", "Supercomputer", 1338522),
            MamSlot("Caterium", "Zipline", 1338523),
            MamSlot("Caterium", "Geothermal Generator", 1338524),
            MamSlot("Caterium", "Priority Power Switch", 1338525),
            MamSlot("Caterium", "Stun Rebar", 1338526),
            MamSlot("Caterium", "Power Poles Mk.3", 1338527),
            MamSlot("Mycelia", "Therapeutic Inhaler", 1338528),
            MamSlot("Mycelia", "Expanded Toolbelt", 1338529),
            MamSlot("Mycelia", "Mycelia", 1338530),
            MamSlot("Mycelia", "Fabric", 1338531),
            MamSlot("Mycelia", "Medical Properties", 1338532),
            MamSlot("Mycelia", "Toxic Cellular Modification", 1338533),
            MamSlot("Mycelia", "Vitamin Inhaler", 1338534),
            MamSlot("Mycelia", "Parachute", 1338535),
            MamSlot("Mycelia", "Synthethic Polyester Fabric", 1338536),
            MamSlot("Nutrients", "Bacon Agaric", 1338537),
            MamSlot("Nutrients", "Beryl Nut", 1338538),
            MamSlot("Nutrients", "Paleberry", 1338539),
            MamSlot("Nutrients", "Nutritional Processor", 1338540),
            MamSlot("Nutrients", "Nutritional Inhaler", 1338541),
            MamSlot("Power Slugs", "Slug Scanning", 1338542),
            MamSlot("Power Slugs", "Blue Power Slugs", 1338543),
            MamSlot("Power Slugs", "Yellow Power Shards", 1338544),
            MamSlot("Power Slugs", "Purple Power Shards", 1338545),
            MamSlot("Power Slugs", "Overclock Production", 1338546),
            MamSlot("Quartz", "Crystal Oscillator", 1338547),
            MamSlot("Quartz", "Quartz Crystals", 1338548),
            MamSlot("Quartz", "Quartz", 1338549),
            MamSlot("Quartz", "Shatter Rebar", 1338550),
            MamSlot("Quartz", "Silica", 1338551),
            MamSlot("Quartz", "Explosive Resonance Application", 1338552),
            MamSlot("Quartz", "Blade Runners", 1338553),
            MamSlot("Quartz", "The Explorer", 1338554),
            MamSlot("Quartz", "Radio Signal Scanning", 1338555),
            MamSlot("Quartz", "Inflated Pocket Dimension", 1338556),
            MamSlot("Quartz", "Radar Technology", 1338557),
            MamSlot("Sulfur", "The Nobelisk Detonator", 1338558),
            MamSlot("Sulfur", "Smokeless Powder", 1338559),
            MamSlot("Sulfur", "Sulfur", 1338560),
            MamSlot("Sulfur", "Inflated Pocket Dimension", 1338561),
            MamSlot("Sulfur", "The Rifle", 1338562),
            MamSlot("Sulfur", "Compacted Coal", 1338563),
            MamSlot("Sulfur", "Black Powder", 1338564),
            MamSlot("Sulfur", "Explosive Rebar", 1338565),
            MamSlot("Sulfur", "Cluster Nobelisk", 1338566),
            MamSlot("Sulfur", "Experimental Power Generation", 1338567),
            MamSlot("Sulfur", "Turbo Rifle Ammo", 1338568),
            MamSlot("Sulfur", "Turbo Fuel", 1338569),
            MamSlot("Sulfur", "Expanded Toolbelt", 1338570),
            MamSlot("Sulfur", "Nuclear Deterrent Development", 1338571),
            ShopSlot(self.state_logic, 1, 3, 1338700),
            ShopSlot(self.state_logic, 2, 3, 1338701),
            ShopSlot(self.state_logic, 3, 5, 1338702),
            ShopSlot(self.state_logic, 4, 5, 1338703),
            ShopSlot(self.state_logic, 5, 10, 1338704),
            ShopSlot(self.state_logic, 6, 10, 1338705),
            ShopSlot(self.state_logic, 7, 20, 1338706),
            ShopSlot(self.state_logic, 8, 20, 1338707),
            ShopSlot(self.state_logic, 9, 50, 1338708),
            ShopSlot(self.state_logic, 10, 50, 1338709)
        ]

    def get_all_location_ids_by_name(cls) -> Dict[str, int]:
        location_table = cls.get_base_location_table()

        # All possible locations
        hub_location_id = cls.hub_location_start
        for tier in range(1, cls.max_tiers + 1):
            for milestone in range(1, cls.max_milestones + 1):
                for slot in range(1, cls.max_slots + 1):
                    location_table.append(HubSlot(tier, milestone, slot, hub_location_id))
                    hub_location_id += 1

        location_table.append(LocationData("Overworld", "UpperBound", 1338999))

        return {location.name: location.code for location in location_table}

    def get_locations(self) -> List[LocationData]:
        if not self.game_logic or not self.state_logic or not self.items:
            raise Exception("Locations need to be initialized with logic and items before using this method")

        location_table = self.get_base_location_table()

        # Only used locations
        hub_location_id = self.hub_location_start
        for tier in range(1, self.max_tiers + 1):
            for milestone in range(1, self.max_milestones + 1):
                for slot in range(1, self.max_slots + 1):
                    if tier <= len(self.game_logic.hub_layout) \
                            and milestone <= len(self.game_logic.hub_layout[tier - 1]) \
                            and slot <= self.game_logic.slots_per_milestone:
                        location_table.append(HubSlot(tier, milestone, slot, hub_location_id))

                    hub_location_id += 1

        location_table.extend(self.get_logical_event_locations())

        return location_table


    def get_logical_event_locations(self) -> List[LocationData]:
        location_table: List[LocationData] = []

        # for performance plan is to upfront calculated everything we need
        # and than create one massive state.has_all for each logical gate (hub tiers, elevator tiers)

        location_table.extend(
            ElevatorTier(index, self.state_logic, self.game_logic) 
            for index, parts in enumerate(self.game_logic.space_elevator_tiers))
        location_table.extend(
            part 
            for part_name, recipes in self.game_logic.recipes.items() 
            for part in Part.get_parts(self.state_logic, recipes, part_name, self.items))
        location_table.extend(
            EventBuilding(self.game_logic, self.state_logic, name, building) 
            for name, building in self.game_logic.buildings.items())
        location_table.extend(
            PowerInfrastructure(self.game_logic, self.state_logic, power_level, recipes) 
            for power_level, recipes in self.game_logic.requirement_per_powerlevel.items())

        return location_table
# THIS IS AN AUTO-GENERATED FILE. DO NOT MODIFY.
# data_gen_templates/rules.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from typing import Tuple
from BaseClasses import CollectionState
from collections.abc import Callable, Mapping, MutableMapping
from . import Hm, items, locations, species
from ..options import PokemonPlatinumOptions

Rule = Callable[[CollectionState], bool]

def always_true(*args, **kwargs) -> bool:
    return True

def create_hm_badge_rule(hm: Hm, player: int) -> Rule:
    badge_item = hm.badge_item()
    if badge_item is not None:
        def hm_badge_rule(state: CollectionState) -> bool:
            return state.has(badge_item, player)
    else:
        def hm_badge_rule(state: CollectionState) -> bool:
            return True
    return hm_badge_rule

class Rules:
    exit_rules: Mapping[Tuple[str, str], Rule]
    location_rules: Mapping[str, Rule]
    encounter_type_rules: Mapping[str, Rule]
    location_type_rules: Mapping[str, Rule]
    common_rules: MutableMapping[str, Callable]
    opts: PokemonPlatinumOptions
    
    def __init__(self, player: int, common_rules: MutableMapping[str, Callable], opts: PokemonPlatinumOptions):
        self.player = player
        self.opts = opts
        self.common_rules = common_rules
        self.common_rules.update({ hm.name.lower():self.create_hm_rule(hm, player) for hm in Hm })
        def regional_mons(n: int) -> Rule:
            mons = [f"mon_{spec}" for spec in species.regional_mons]
            def rule(state: CollectionState) -> bool:
                return state.has_from_list_unique(mons, player, n)
            return rule
        def mons(n: int) -> Rule:
            mons = [f"mon_{spec}" for spec in species.species.keys()]
            def rule(state: CollectionState) -> bool:
                return state.has_from_list_unique(mons, player, n)
            return rule
        def badges(n: int) -> Rule:
            badges = [items.items[loc.original_item].label
                for loc in locations.locations.values() if loc.type == "badge"]
            def rule(state: CollectionState) -> bool:
                return state.has_from_list_unique(badges, player, n)
            return rule
        self.common_rules["regional_mons"] = regional_mons
        self.common_rules["mons"] = mons
        self.common_rules["badges"] = badges

    def fill_rules(self):
        self.common_rules.update({
            "national_dex": (lambda state : state.has("Upgradable Pokédex", self.player, 3)),
            "dowsingmachine_if_opt": (lambda state : state.has_all(["DOWSING MACHINE", "Pokétch"], self.player)) if self.opts.dowsing_machine_logic.value != 0 else always_true,
            "defog_if_opt": (self.common_rules["defog"]) if self.opts.visibility_hm_logic.value != 0 else always_true,
            "flash_if_opt": (self.common_rules["flash"]) if self.opts.visibility_hm_logic.value != 0 else always_true,
            "poketch_req": (lambda state : state.has_all(["Coupon 1", "Coupon 2", "Parcel", "Coupon 3"], self.player)),
        })
        self.exit_rules = {
            ("valor_lakefront", "lake_valor_drained"): (lambda state : state.has("event_lake_explosion", self.player)),
            ("valor_lakefront", "route_222"): (lambda state : state.has("event_distortion_world", self.player)) if self.opts.early_sunyshore.value == 0 else always_true,
            ("valor_lakefront", "lake_valor"): (lambda state : state.has("event_distortion_world", self.player)),
            ("verity_lakefront", "lake_verity"): (lambda state : state.has("event_lake_valor_defeat_saturn", self.player)),
            ("acuity_lakefront", "lake_acuity"): (lambda state : state.has("event_lake_verity_defeat_mars", self.player) and self.common_rules["rock_climb"](state)),
            ("acuity_lakefront", "lake_acuity_low_water"): (self.common_rules["rock_climb"]),
            ("route_219", "route_220"): (self.common_rules["surf"]),
            ("route_221", "pal_park_lobby"): (self.common_rules["national_dex"]),
            ("jubilife_city", "route_203"): (self.common_rules["poketch_req"]) if self.opts.parcel_coupons_route_203.value != 0 else always_true,
            ("jubilife_city", "jubilife_tv_1f"): (lambda state : state.has("event_coal_badge", self.player)),
            ("oreburgh_gate_1f", "oreburgh_gate_b1f"): (self.common_rules["rock_smash"]),
            ("route_207_south", "route_207"): (lambda state : state.has("Bicycle", self.player)),
            ("ravaged_path", "route_204_north"): (self.common_rules["rock_smash"]),
            ("floaroma_town", "route_205_south"): (lambda state : state.has("Works Key", self.player) or self.common_rules["surf"](state)),
            ("route_205_south", "fuego_ironworks_outside"): (self.common_rules["surf"]),
            ("route_205_south", "eterna_forest_outside"): (self.common_rules["cut"]),
            ("route_205_north", "eterna_forest_outside"): (self.common_rules["cut"]),
            ("eterna_forest", "old_chateau"): (self.common_rules["cut"]),
            ("eterna_city", "team_galactic_eterna_building_1f"): (self.common_rules["cut"]),
            ("mt_coronet_1f_north_room_1_left", "mt_coronet_1f_north_room_1_middle"): (self.common_rules["rock_smash"]),
            ("mt_coronet_1f_north_room_1_middle", "mt_coronet_1f_north_room_1_left"): (lambda state : self.common_rules["strength"](state) or self.common_rules["rock_smash"](state)),
            ("mt_coronet_1f_north_room_1_middle", "mt_coronet_1f_north_room_1_right"): (self.common_rules["strength"]),
            ("mt_coronet_1f_north_room_1_right", "mt_coronet_1f_north_room_1_middle"): (self.common_rules["strength"]),
            ("mt_coronet_1f_north_room_1_right", "mt_coronet_1f_north_room_1_top"): (self.common_rules["strength"]),
            ("mt_coronet_1f_north_room_1_top", "mt_coronet_1f_north_room_1_right"): (self.common_rules["strength"]),
            ("mt_coronet_1f_north_room_1_top", "mt_coronet_b1f"): (lambda state : self.common_rules["fly"](state) and self.common_rules["defog_if_opt"](state)) if self.opts.north_sinnoh_fly.value != 0 else (self.common_rules["defog_if_opt"]),
            ("mt_coronet_1f_north_room_1_bottom", "mt_coronet_1f_north_room_1_right"): (self.common_rules["strength"]),
            ("route_206_cycling_road_north_gate", "cycling_road"): (lambda state : state.has("Bicycle", self.player)),
            ("route_206_cycling_road_south_gate", "cycling_road"): (lambda state : state.has("Bicycle", self.player)),
            ("route_206", "route_206_upper"): (self.common_rules["cut"]),
            ("route_206_upper", "wayward_cave_1f"): (self.common_rules["flash_if_opt"]),
            ("mt_coronet_1f_south", "mt_coronet_2f_right"): (lambda state : self.common_rules["rock_climb"](state) and self.common_rules["surf"](state)),
            ("mt_coronet_2f_right", "mt_coronet_2f_left"): (self.common_rules["strength"]),
            ("route_209_lost_tower_2f", "route_209_lost_tower_3f"): (self.common_rules["defog_if_opt"]),
            ("maniac_tunnel", "solaceon_ruins_maniac_tunnel_room"): (lambda state : state.has("event_solaceon_ruins", self.player)) if self.opts.unown_option.value == self.opts.unown_option.option_vanilla else (lambda state : state.has("Unown File", self.player, 26)) if self.opts.unown_option.value == self.opts.unown_option.option_item else always_true,
            ("route_210_south", "route_210_south_upper"): (lambda state : state.has("SecretPotion", self.player)),
            ("route_210_south_upper", "route_210_south"): (lambda state : state.has("SecretPotion", self.player)),
            ("route_210_south_upper", "route_210_north"): (self.common_rules["defog_if_opt"]),
            ("route_210_north", "route_210_grandma_wilma_house"): (self.common_rules["rock_climb"]),
            ("celestic_town", "route_210_north"): (self.common_rules["defog_if_opt"]),
            ("galactic_hq_wo_key", "veilstone_city_galactic_warehouse"): (lambda state : state.has_any(["Storage Key", "event_lake_acuity_meet_jupiter"], self.player)),
            ("veilstone_city_galactic_warehouse", "galactic_hq_wo_key"): (lambda state : state.has_any(["Storage Key", "event_lake_acuity_meet_jupiter"], self.player)),
            ("veilstone_city", "galactic_hq_w_key"): (lambda state : state.has("Galactic Key", self.player)),
            ("route_214", "spring_path"): (lambda state : state.has("event_distortion_world", self.player)),
            ("route_214", "route_214_top"): (self.common_rules["surf"]) if self.opts.pastoria_barriers.value != 0 else always_true,
            ("sendoff_spring", "turnback_cave_entrance"): (self.common_rules["defog_if_opt"]),
            ("route_213", "grand_lake_route_213_northeast_house"): (self.common_rules["rock_climb"]),
            ("route_218", "route_218_gate_to_canalave_city"): (self.common_rules["surf"]),
            ("canalave_city", "fullmoon_island"): (lambda state : state.has("event_beat_cynthia", self.player) and self.common_rules["national_dex"](state)),
            ("mt_coronet_1f_tunnel_room", "mt_coronet_1f_tunnel_room_base"): (self.common_rules["rock_climb"]),
            ("mt_coronet_1f_tunnel_room_base", "mt_coronet_1f_tunnel_room"): (self.common_rules["rock_climb"]),
            ("mt_coronet_1f_north_room_2", "mt_coronet_b1f"): (self.common_rules["defog_if_opt"]),
            ("mt_coronet_outside_south", "mt_coronet_outside_north_plat"): (self.common_rules["rock_climb"]),
            ("mt_coronet_outside_south", "mt_coronet_outside_south_entrance"): (self.common_rules["rock_climb"]),
            ("mt_coronet_outside_north_plat", "mt_coronet_outside_south"): (self.common_rules["rock_climb"]),
            ("mt_coronet_outside_south_entrance", "mt_coronet_outside_south"): (self.common_rules["rock_climb"]),
            ("mt_coronet_4f_rooms_1_and_2_lower", "mt_coronet_4f_rooms_1_and_2"): (self.common_rules["rock_climb"]),
            ("mt_coronet_4f_rooms_1_and_2", "mt_coronet_4f_rooms_1_and_2_lower"): (self.common_rules["rock_climb"]),
            ("mt_coronet_2f_left", "mt_coronet_3f"): (lambda state : state.has("event_galactic_hq_defeat_cyrus", self.player)),
            ("snowpoint_city", "fight_area"): (lambda state : state.has_any(["event_beat_cynthia", "S.S. Ticket"], self.player)),
            ("snowpoint_city", "snowpoint_temple_1f"): (lambda state : state.has("event_beat_cynthia", self.player) and self.common_rules["national_dex"](state)),
            ("victory_road_1f", "victory_road_1f_room_1"): (lambda state : state.has("event_beat_cynthia", self.player) and self.common_rules["national_dex"](state)),
            ("route_223", "pokemon_league_south_south"): (self.common_rules["surf"]),
            ("pokemon_league_south_south", "pokemon_league_south"): (lambda state : self.common_rules["surf"](state) and self.common_rules["waterfall"](state)),
            ("pokemon_league_north_pokecenter_1f", "pokemon_league_elevator_to_aaron_room"): (self.common_rules["badges"](8)),
            ("victory_road_1f_entrance", "victory_road_2f_entrance"): (self.common_rules["rock_climb"]),
            ("victory_road_2f_entrance", "victory_road_2f"): (lambda state : self.common_rules["strength"](state) and self.common_rules["rock_smash"](state)),
            ("pastoria_city_observatory_gate_1f", "virt_great_marsh"): (lambda state : state.has("Marsh Pass", self.player)) if self.opts.marsh_pass.value != 0 else always_true,
            ("route_212_north_top", "route_212_north"): (self.common_rules["surf"]) if self.opts.pastoria_barriers.value != 0 else always_true,
            ("route_212_north", "route_212_north_top"): (self.common_rules["surf"]) if self.opts.pastoria_barriers.value != 0 else always_true,
            ("route_214_top", "route_214"): (self.common_rules["surf"]) if self.opts.pastoria_barriers.value != 0 else always_true,
            ("fight_area", "route_225_gate_to_fight_area"): (self.common_rules["national_dex"]),
            ("fight_area", "route_230"): (self.common_rules["national_dex"]),
            ("route_230", "route_229"): (self.common_rules["surf"]),
            ("route_230", "fight_area"): (lambda state : self.common_rules["surf"](state) and self.common_rules["national_dex"](state)),
            ("route_228", "route_228_rock_peak_ruins"): (lambda state : state.has("Bicycle", self.player) or self.common_rules["fly"](state)),
            ("route_226_east", "route_226_mid"): (lambda state : self.common_rules["rock_climb"](state) and self.common_rules["surf"](state)),
            ("route_226_mid", "route_226_east"): (self.common_rules["surf"]),
            ("route_226_west", "route_226_mid"): (self.common_rules["rock_climb"]),
            ("route_227_lower", "route_227"): (lambda state : state.has("Bicycle", self.player)),
            ("stark_mountain_room_1_entrance", "stark_mountain_room_1"): (self.common_rules["strength"]),
            ("stark_mountain_room_1", "stark_mountain_room_2"): (self.common_rules["rock_smash"]),
            ("ravaged_path", "ravaged_path_old_rod"): (self.common_rules["rock_smash"]),
            ("ravaged_path", "ravaged_path_good_rod"): (self.common_rules["rock_smash"]),
            ("ravaged_path", "ravaged_path_super_rod"): (self.common_rules["rock_smash"]),
            ("ravaged_path", "ravaged_path_surf"): (self.common_rules["rock_smash"]),
            ("route_218", "route_218_land"): (self.common_rules["surf"]),
            ("route_230", "route_230_land"): (self.common_rules["surf"]),
        }
        self.location_rules = {
            "Twinleaf Town - Hidden (Odd Keystone)": (self.common_rules["surf"]),
            "Lake Verity - Overworld (TM38) 1": (self.common_rules["surf"]),
            "Pokemon Research Lab - National Pokédex (From Oak)": (self.common_rules["regional_mons"](self.opts.regional_dex_goal.value)),
            "Pokemon Research Lab - Poké Radar (From Rowan)": (self.common_rules["regional_mons"](self.opts.regional_dex_goal.value)),
            "Trainers' School - Town Map (From Parcel)": (lambda state : state.has("Parcel", self.player)),
            "Jubilife City - Coupon 1 (From Poketch Campaign Clown)": (lambda state : state.has("Parcel", self.player)),
            "Jubilife City - Coupon 2 (From Poketch Campaign Clown)": (lambda state : state.has("Parcel", self.player)),
            "Jubilife City - Coupon 3 (From Poketch Campaign Clown)": (lambda state : state.has("Parcel", self.player)),
            "Jubilife City - Poketch": (self.common_rules["poketch_req"]),
            "Jubilife City - Calculator App": (self.common_rules["poketch_req"]),
            "Jubilife City - Pedometer App": (self.common_rules["poketch_req"]),
            "Jubilife City - Party Status App": (self.common_rules["poketch_req"]),
            "Oreburgh Gate - Overworld (TM31)": (lambda state : state.has("Bicycle", self.player) or self.common_rules["surf"](state)),
            "Oreburgh Gate - Overworld (TM01)": (lambda state : self.common_rules["strength"](state) and self.common_rules["surf"](state)),
            "Oreburgh Gate - Overworld (Earth Plate)": (lambda state : self.common_rules["strength"](state) and self.common_rules["surf"](state)),
            "Oreburgh City - Heal Ball (Gift in North House)": (lambda state : state.has("mon_geodude", self.player)),
            "Jubilife City - Fashion Case (From Reporter after Defeating Grunts)": (lambda state : state.has("event_coal_badge", self.player)),
            "Route 204 - Overworld (Sea Incense)": (self.common_rules["surf"]),
            "Route 204 - Overworld (HP Up)": (self.common_rules["surf"]),
            "Ravaged Path - Overworld (TM39)": (self.common_rules["rock_smash"]),
            "Ravaged Path - Overworld (TM03)": (lambda state : self.common_rules["surf"](state) and self.common_rules["rock_smash"](state)),
            "Ravaged Path - Overworld (Luck Incense)": (lambda state : self.common_rules["surf"](state) and self.common_rules["rock_smash"](state)),
            "Route 204 North - TM78 (Gift)": (self.common_rules["cut"]),
            "Valley Windworks - Overworld (TM24)": (self.common_rules["surf"]),
            "Valley Windworks - Overworld (Electirizer)": (self.common_rules["surf"]),
            "Valley Windworks - Hidden (Max Elixir)": (self.common_rules["surf"]),
            "Eterna Forest - Hidden (Insect Plate)": (self.common_rules["cut"]),
            "Eterna Forest - Overworld (Ether)": (self.common_rules["cut"]),
            "Eterna City - Overworld (TM46)": (self.common_rules["cut"]),
            "Cycle Shop - Bicycle": (lambda state : state.has("event_eterna_defeat_team_galactic", self.player)),
            "Eterna City - Hidden (Moon Stone)": (self.common_rules["surf"]),
            "Eterna City - Up-Grade (From Oak)": (lambda state : state.has("event_met_oak_pal_park", self.player)),
            "Eterna City - Exp. Share (From Rowan's Assistant)": (self.common_rules["mons"](35)),
            "Route 211 - Overworld (TM12)": (self.common_rules["rock_smash"]),
            "Mt. Coronet - Overworld (Rare Candy)": (self.common_rules["rock_smash"]),
            "Mt. Coronet - Overworld (TM69)": (self.common_rules["strength"]),
            "Wayward Cave - Overworld (TM32)": (self.common_rules["rock_smash"]),
            "Wayward Cave - Overworld (Revive)": (self.common_rules["rock_smash"]),
            "Wayward Cave - Overworld (Escape Rope)": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden (Yellow Shard)": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden (Great Ball)": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden (Green Shard)": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden (Super Potion)": (self.common_rules["rock_smash"]),
            "Wayward Cave - Hidden (Blue Shard)": (self.common_rules["rock_smash"]),
            "Wayward Cave - Overworld (TM26)": (lambda state : state.has("Bicycle", self.player)),
            "Wayward Cave - Overworld (Grip Claw)": (lambda state : state.has("Bicycle", self.player)),
            "Wayward Cave - Overworld (Max Ether)": (lambda state : state.has("Bicycle", self.player)),
            "Wayward Cave - Overworld (Rare Candy)": (lambda state : state.has("Bicycle", self.player)),
            "Wayward Cave - Hidden (Stardust)": (lambda state : state.has("Bicycle", self.player)),
            "Route 207 - Overworld (Iron)": (self.common_rules["rock_climb"]),
            "Mt. Coronet - Overworld (Protein)": (self.common_rules["surf"]),
            "Mt. Coronet - Overworld (Dawn Stone)": (self.common_rules["surf"]),
            "Route 208 - Hidden (Star Piece)": (lambda state : self.common_rules["rock_climb"](state) and self.common_rules["rock_smash"](state)),
            "Route 208 - Overworld (Carbos)": (lambda state : self.common_rules["surf"](state) and self.common_rules["waterfall"](state)),
            "Route 208 - Overworld (Ether)": (self.common_rules["rock_smash"]),
            "Route 209 - Overworld (TM19)": (self.common_rules["surf"]),
            "Route 209 - Overworld (Calcium)": (lambda state : state.has("Bicycle", self.player)),
            "Route 209 - Overworld (TM47)": (self.common_rules["cut"]),
            "Route 209 Lost Tower - Cleanse Tag (From NPC At Top)": (self.common_rules["defog"]),
            "Route 209 Lost Tower - Spell Tag (From NPC At Top)": (self.common_rules["defog"]),
            "Solaceon Town - Pokémon History App": (self.common_rules["regional_mons"](50)),
            "Solaceon Ruins - Green Shard (From NPC)": (lambda state : state.has("HM05 Defog", self.player)),
            "Route 210 - Overworld (Super Repel)": (lambda state : state.has("Bicycle", self.player)),
            "Route 210 - Overworld (TM30)": (lambda state : state.has("Bicycle", self.player) and self.common_rules["rock_smash"](state)),
            "Route 210 - Hidden (Shiny Stone)": (self.common_rules["rock_climb"]),
            "Route 210 - Hidden (Meadow Plate)": (lambda state : self.common_rules["surf"](state) and self.common_rules["waterfall"](state)),
            "Route 210 - Overworld (Wave Incense)": (lambda state : self.common_rules["surf"](state) and self.common_rules["waterfall"](state)),
            "Route 210 - Overworld (Zinc)": (self.common_rules["rock_climb"]),
            "Celestic Town Cave - HM03 (From Cynthia's Grandmother)": (lambda state : state.has("Old Charm", self.player)),
            "Celestic Town - Overworld (Dragon Fang)": (lambda state : state.has("Old Charm", self.player)),
            "Celestic Town - Hidden (King’s Rock)": (lambda state : state.has("Old Charm", self.player)),
            "Route 211 - Hidden (Calcium)": (lambda state : self.common_rules["rock_climb"](state) and self.common_rules["rock_smash"](state)),
            "Route 211 - Overworld (TM29)": (lambda state : self.common_rules["rock_climb"](state) and self.common_rules["rock_smash"](state)),
            "Route 215 - Overworld (Fist Plate)": (self.common_rules["cut"]),
            "Route 215 - Overworld (TM34)": (self.common_rules["cut"]),
            "Veilstone City - Overworld (Full Incense)": (self.common_rules["rock_climb"]),
            "Galactic HQ - Overworld (TM21)": (lambda state : state.has("Galactic Key", self.player)),
            "Route 214 - Overworld (Rare Candy)": (self.common_rules["surf"]),
            "Valor Lakefront - SecretPotion (From Cynthia)": (lambda state : state.has("event_fen_badge", self.player)),
            "Valor Lakefront - Hidden (Sun Stone)": (self.common_rules["rock_climb"]),
            "Valor Lakefront - Overworld (TM85)": (self.common_rules["rock_climb"]),
            "Valor Lakefront - Overworld (Iron)": (self.common_rules["rock_climb"]),
            "Valor Lakefront - White Flute (After Returning Suite Key)": (lambda state : state.has("Suite Key", self.player)),
            "Route 213 - Hidden (Hyper Potion)": (self.common_rules["rock_smash"]),
            "Route 213 - Hidden (Suite Key)": (self.common_rules["dowsingmachine_if_opt"]),
            "Route 213 - Overworld (Max Revive)": (self.common_rules["surf"]),
            "Route 213 - Overworld (Protein)": (self.common_rules["rock_climb"]),
            "Route 213 - Hidden (HP Up)": (self.common_rules["rock_climb"]),
            "Route 213 - Hidden (Big Pearl)": (self.common_rules["surf"]),
            "Route 213 - Hidden (Big Pearl) 1": (self.common_rules["surf"]),
            "Route 213 - Overworld (Water Stone)": (self.common_rules["surf"]),
            "Route 213 - Overworld (TM05)": (self.common_rules["rock_climb"]),
            "Route 213 - Overworld (TM40)": (self.common_rules["rock_smash"]),
            "Pastoria City - Overworld (Mystic Water)": (self.common_rules["surf"]),
            "Route 212 - Overworld (TM84)": (self.common_rules["surf"]),
            "Route 212 - Hidden (Max Ether)": (self.common_rules["surf"]),
            "Route 212 - Overworld (Hyper Potion)": (self.common_rules["cut"]),
            "Route 212 - Overworld (Zinc)": (self.common_rules["cut"]),
            "Route 212 - Overworld (TM11)": (lambda state : self.common_rules["surf"](state) or self.common_rules["cut"](state)),
            "Route 212 - Overworld (Rose Incense)": (self.common_rules["surf"]),
            "Route 212 - Overworld (Iron)": (self.common_rules["surf"]),
            "Route 212 - Hidden (Big Mushroom)": (lambda state : state.has("Bicycle", self.player) and self.common_rules["cut"](state)),
            "Route 212 - Overworld (TM62)": (lambda state : state.has_all(["Bag", "Bicycle"], self.player)) if self.opts.pastoria_barriers.value != 0 else (lambda state : state.has("Bicycle", self.player)),
            "Route 218 - Overworld (Rare Candy)": (self.common_rules["surf"]),
            "Route 218 - Overworld (Hyper Potion)": (self.common_rules["surf"]),
            "Canalave City - Overworld (TM89)": (self.common_rules["surf"]),
            "Iron Island - Metal Coat (From Byron)": (self.common_rules["national_dex"]),
            "Mt. Coronet - Hidden (Stardust) 2": (self.common_rules["rock_smash"]),
            "Mt. Coronet - Hidden (Heal Powder) 1": (self.common_rules["rock_smash"]),
            "Mt. Coronet - Hidden (Green Shard)": (lambda state : self.common_rules["rock_climb"](state) and self.common_rules["rock_smash"](state)),
            "Mt. Coronet - Hidden (Green Shard) 1": (self.common_rules["rock_climb"]),
            "Mt. Coronet - Hidden (Rare Candy)": (self.common_rules["rock_climb"]),
            "Mt. Coronet - Overworld (Ultra Ball)": (self.common_rules["rock_smash"]),
            "Mt. Coronet - Overworld (Soft Sand)": (lambda state : self.common_rules["strength"](state) and self.common_rules["rock_smash"](state)),
            "Mt. Coronet - Hidden (Blue Shard) 1": (self.common_rules["rock_smash"]),
            "Mt. Coronet - Overworld (Light Clay)": (self.common_rules["surf"]),
            "Mt. Coronet - Overworld (Max Elixir)": (lambda state : self.common_rules["surf"](state) or self.common_rules["rock_smash"](state)),
            "Mt. Coronet - Overworld (Revive)": (self.common_rules["strength"]),
            "Mt. Coronet - Overworld (Full Restore)": (self.common_rules["rock_smash"]),
            "Mt. Coronet - Hidden (Blue Shard)": (self.common_rules["rock_smash"]),
            "Mt. Coronet - Hidden (Sun Stone)": (self.common_rules["rock_smash"]),
            "Mt. Coronet - Hidden (Heal Powder)": (self.common_rules["rock_smash"]),
            "Mt. Coronet - Hidden (Yellow Shard)": (self.common_rules["rock_smash"]),
            "Mt. Coronet - Overworld (Adamant Orb)": (lambda state : self.common_rules["surf"](state) and self.common_rules["waterfall"](state)),
            "Mt. Coronet - Overworld (Lustrous Orb)": (lambda state : self.common_rules["surf"](state) and self.common_rules["waterfall"](state)),
            "Mt. Coronet - Hidden (Stone Plate)": (lambda state : self.common_rules["surf"](state) and self.common_rules["waterfall"](state)),
            "Route 216 - Overworld (TM13)": (self.common_rules["rock_climb"]),
            "Route 216 - Overworld (Max Potion)": (self.common_rules["rock_climb"]),
            "Route 216 - Overworld (HP Up)": (self.common_rules["rock_climb"]),
            "Route 216 - Overworld (Mental Herb)": (self.common_rules["rock_climb"]),
            "Route 217 - Icicle Plate (From Hiker After Sharing HM08)": (lambda state : state.has("HM08 Rock Climb", self.player)),
            "Acuity Lakefront - Overworld (Reaper Cloth)": (self.common_rules["rock_climb"]),
            "Snowpoint Temple - Overworld (Full Heal)": (self.common_rules["strength"]),
            "Route 222 - Hidden (Full Restore)": (lambda state : self.common_rules["surf"](state) or self.common_rules["rock_smash"](state)),
            "Route 222 - Overworld (Carbos)": (self.common_rules["cut"]),
            "Route 222 - Overworld (Quick Ball)": (lambda state : self.common_rules["surf"](state) or self.common_rules["rock_smash"](state)),
            "Route 222 - Hidden (TinyMushroom)": (lambda state : self.common_rules["surf"](state) or self.common_rules["rock_smash"](state)),
            "Route 222 - Hidden (Big Mushroom)": (self.common_rules["surf"]),
            "Sunyshore City - HM07 (From Jasmine)": (lambda state : state.has("event_beacon_badge", self.player)),
            "Pokétch Company - Memo Pad App": (lambda state : state.has_all(["Coupon 1", "Coupon 2", "Coupon 3", "Parcel"], self.player) and self.common_rules["badges"](1)(state)),
            "Pokétch Company - Marking Map App": (lambda state : state.has_all(["Coupon 1", "Coupon 2", "Coupon 3", "Parcel"], self.player) and self.common_rules["badges"](3)(state)),
            "Pokétch Company - Link Searcher App": (lambda state : state.has_all(["Coupon 1", "Coupon 2", "Coupon 3", "Parcel"], self.player) and self.common_rules["badges"](5)(state)),
            "Pokétch Company - Move Tester App": (lambda state : state.has_all(["Coupon 1", "Coupon 2", "Coupon 3", "Parcel"], self.player) and self.common_rules["badges"](7)(state)),
            "Route 223 - Overworld (TM18)": (self.common_rules["surf"]),
            "Route 223 - Overworld (Ultra Ball)": (self.common_rules["surf"]),
            "Route 223 - Overworld (Dive Ball)": (self.common_rules["surf"]),
            "Route 223 - Overworld (Rare Candy)": (self.common_rules["surf"]),
            "Route 223 - Hidden (Heart Scale)": (self.common_rules["surf"]),
            "Route 223 - Hidden (Heart Scale) 1": (self.common_rules["surf"]),
            "Victory Road - Overworld (TM71)": (lambda state : state.has("Bicycle", self.player)),
            "Victory Road - Overworld (Full Restore)": (lambda state : state.has("Bicycle", self.player)),
            "Victory Road - Overworld (Max Elixir)": (lambda state : state.has("Bicycle", self.player)),
            "Victory Road - Overworld (TM41)": (self.common_rules["rock_climb"]),
            "Victory Road - Hidden (Nugget)": (self.common_rules["rock_climb"]),
            "Route 210 - Old Charm (From Cynthia)": (lambda state : state.has("SecretPotion", self.player)),
            "Fight Area - Super Rod (From Fisherman)": (self.common_rules["national_dex"]),
            "Route 230 - Overworld (Rare Candy)": (lambda state : self.common_rules["surf"](state) and self.common_rules["rock_smash"](state)),
            "Route 230 - Hidden (Water Stone)": (lambda state : self.common_rules["surf"](state) and self.common_rules["rock_smash"](state)),
            "Route 230 - Overworld (Blue Shard)": (lambda state : self.common_rules["surf"](state) and self.common_rules["rock_smash"](state)),
            "Route 230 - Hidden (Ultra Ball)": (lambda state : self.common_rules["surf"](state) and self.common_rules["rock_smash"](state)),
            "Route 229 - Overworld (Reaper Cloth)": (self.common_rules["cut"]),
            "Route 229 - Overworld (Protein)": (self.common_rules["cut"]),
            "Route 229 - Hidden (Thunderstone)": (lambda state : self.common_rules["surf"](state) and self.common_rules["cut"](state)),
            "Resort Area - Overworld (Nugget)": (self.common_rules["surf"]),
            "Route 228 - Overworld (Protector)": (lambda state : state.has("Bicycle", self.player) or self.common_rules["fly"](state)),
            "Route 228 - Overworld (Shed Shell)": (self.common_rules["rock_smash"]),
            "Route 228 - Overworld (Shiny Stone)": (lambda state : state.has("Bicycle", self.player)),
            "Route 228 - Hidden (Calcium)": (lambda state : state.has("Bicycle", self.player)),
            "Route 228 - Hidden (PP Max)": (lambda state : state.has("Bicycle", self.player)),
            "Route 227 - Hidden (Rare Candy)": (self.common_rules["surf"]),
            "Route 226 - Hidden (Heart Scale)": (self.common_rules["surf"]),
            "Survival Area - Overworld (Red Shard)": (self.common_rules["rock_climb"]),
            "Route 225 - Overworld (Razor Fang)": (self.common_rules["rock_climb"]),
            "Route 225 - Overworld (Rare Candy)": (self.common_rules["cut"]),
            "Route 225 - Overworld (Lax Incense)": (self.common_rules["cut"]),
            "Route 225 - Overworld (Dubious Disc)": (self.common_rules["surf"]),
            "Route 225 - Overworld (Dawn Stone)": (self.common_rules["rock_climb"]),
            "Route 227 - Hidden (Max Repel)": (self.common_rules["rock_climb"]),
            "Route 227 - Overworld (Charcoal)": (self.common_rules["rock_climb"]),
            "Stark Mountain - Overworld (Life Orb)": (self.common_rules["rock_climb"]),
            "Stark Mountain - Overworld (Full Restore)": (self.common_rules["rock_smash"]),
            "Stark Mountain - Hidden (Star Piece)": (self.common_rules["rock_smash"]),
            "Stark Mountain - Overworld (Ultra Ball)": (self.common_rules["rock_climb"]),
            "Stark Mountain - Hidden (Ultra Ball)": (self.common_rules["rock_climb"]),
            "Stark Mountain - Overworld (Max Elixir) 1": (self.common_rules["rock_climb"]),
            "Stark Mountain - Overworld (Nugget)": (self.common_rules["rock_climb"]),
            "event_lake_explosion": (lambda state : state.has_all(["HM04 Strength", "event_mine_badge"], self.player)),
        }
        self.location_type_rules = {
            "hidden": (self.common_rules["dowsingmachine_if_opt"]),
            "uunown": (self.common_rules["dowsingmachine_if_opt"]),
        }
        self.encounter_type_rules = {
            "surf": (self.common_rules["surf"]),
            "good_rod": (lambda state : state.has_all(["Bag", "Good Rod"], self.player)),
            "super_rod": (lambda state : state.has_all(["Super Rod", "Bag"], self.player)),
            "old_rod": (lambda state : state.has_all(["Bag", "Old Rod"], self.player)),
        }

    def create_hm_rule(self, hm: Hm, player: int) -> Rule:
        mons = set()
        item_evols = []
        for name, spec in species.species.items():
            if hm not in spec.hms:
                continue
            mons.add(f"mon_{name}")
            while spec.pre_evolution:
                new_spec = species.species[spec.pre_evolution.species]
                if hm in new_spec.hms:
                    break
                if spec.pre_evolution.item:
                    item_evols.append([f"mon_{spec.pre_evolution.species}", spec.pre_evolution.item])
                else:
                    mons.add(f"mon_{spec.pre_evolution.species}")
                spec = new_spec
        bag = items.items["bag"].label
        def hm_rule(state: CollectionState) -> bool:
            if not (state.has_all([hm, bag], player) and self.common_rules[f"{hm.name.lower()}_badge"](state)):
                return False
            if state.has_any(mons, player):
                return True
            for item_evol in item_evols:
                if state.has_all(item_evol, player):
                    return True
            return False

        return hm_rule

import asyncio
import time
import traceback
from dataclasses import dataclass
from math import ceil
from typing import Any, Dict, Optional
from copy import deepcopy
import dolphin_memory_engine

import Utils
from BaseClasses import ItemClassification
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus
from worlds.shadow_the_hedgehog.Options import WeaponsanityHold
from . import Levels, Items, Locations, Junk, Utils as ShadowUtils, Weapons
from .Levels import *
from .Locations import GetStageInformation, GetAlignmentsForStage, \
    GetStageEnemysanityInformation, MissionClearLocations

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a ROM for Shadow The Hedgehog. Currently {1}. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure Shadow The Hedgehog is running."
)

CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."

SHADOW_THE_HEDGEHOG_GAME_ID = "GUPE8P"
SHADOW_THE_HEDGEHOG_GAME_ID_RELOADED = "GUPR8P"

valid_game_bytes = [
    bytes(SHADOW_THE_HEDGEHOG_GAME_ID, "utf-8"),
    bytes(SHADOW_THE_HEDGEHOG_GAME_ID_RELOADED, "utf-8")
]

class ShTHCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_dolphin(self):
        """Prints the current Dolphin status to the client."""
        if isinstance(self.ctx, ShTHContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


@dataclass
class StageAlignmentAddress:
    stageId: int
    alignmentId: int
    tally_address: int | None
    #addressSize: int
    #searchIndex: int | None
    #totalSearchIndex: int | None

class SAVE_STRUCTURE_DETAILS:
    LevelClears = 4
    # Repeat Dark for Normal and Hero
    AlignmentClear = 1
    AlignmentUnknown1 = 3
    AlignmentMissionRank = 4
    AlignmentTimeMinutes = 4
    AlignmentTimeSeconds = 1
    AlignmentTimeMilliseconds = 1
    AlignmentUnknown2 = 6
    AlignmentScore = 4

    Keys = 20  # 4 Bytes for each Key ID?

    AlignmentOrder = ["Dark", "Neutral", "Hero"]

    Size = 4 + (24 * 3) + 20

westopolis_save_info_base_address = 0x80576BE0

CHECKPOINT_MAX_FLAG_ADDRESS = 0x80575FBF
CHECKPOINT_FLAGS = [0x80575FFC, 0x80576018, 0x80576034, 0x80576050,
                    0x8057606C, 0x80576088, 0x805760A4, 0x805760C0]

is_paused_address = 0x805EE1DC

CURRENT_STAGE_BASE_KEYSANITY_ADDRESS = 0x8057fb80
KEY_IDENTIFIER_BY_STAGE = \
{
    STAGE_WESTOPOLIS:       [0x3F, 0x40, 0x3C, 0x3D, 0x3E], #Ordered
    STAGE_DIGITAL_CIRCUIT:  [0x3C, 0x40, 0x3D, 0x3E, 0x3F], #Ordered
    STAGE_GLYPHIC_CANYON:   [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered
    STAGE_LETHAL_HIGHWAY:   [0x3F, 0x3C, 0x3E, 0x3D, 0x40], #Ordered
    STAGE_CRYPTIC_CASTLE:   [0x3E, 0x3D, 0x3C, 0x40, 0x3F], #Ordered, dark then neutral
    STAGE_PRISON_ISLAND:    [0x3D, 0x3C, 0x3E, 0x3F, 0x40], #Ordered
    STAGE_CIRCUS_PARK:      [0x40, 0x3C, 0x3D, 0x3E, 0x3F], #Ordered
    STAGE_CENTRAL_CITY:     [0x3E, 0x3C, 0x3F, 0x3D, 0x40], #Ordered, by dark mission
    STAGE_THE_DOOM:         [0xC9, 0xCA, 0xCB, 0xCC, 0x05], #Ordered
    STAGE_SKY_TROOPS:       [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered
    STAGE_MAD_MATRIX:       [0x3C, 0x40, 0x3E, 0x3F, 0x3D], #Ordered - C/Y/G/R/R
    STAGE_DEATH_RUINS:      [0x01, 0x02, 0x03, 0x04, 0x05], #Ordered
    STAGE_THE_ARK:          [0x04, 0x01, 0x02, 0x05, 0x03], #Ordered
    STAGE_AIR_FLEET:        [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered
    STAGE_IRON_JUNGLE:      [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered checkpoint order
    STAGE_SPACE_GADGET:     [0x04, 0x01, 0x02, 0x03, 0x05], #Ordered Dark first
    STAGE_LOST_IMPACT:      [0x03, 0x04, 0x05, 0x01, 0x02], #Ordered
    STAGE_GUN_FORTRESS:     [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered
    STAGE_BLACK_COMET:      [0x60, 0x5F, 0x61, 0x62, 0x63], #Ordered
    STAGE_LAVA_SHELTER:     [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered, dark first
    STAGE_COSMIC_FALL:      [0x03, 0x04, 0x05, 0x01, 0x02], #Ordered
    STAGE_FINAL_HAUNT:      [0x5F, 0x60, 0x61, 0x62, 0x63], #Ordered
}

#STAGE_TO_UNLOCK_ADDRESS = \
#{
#    STAGE_WESTOPOLIS: 0x80576BE0,
#    STAGE_DIGITAL_CIRCUIT: 0x80576BE0 + (1 * SAVE_STRUCTURE_DETAILS.Size),
#    STAGE_GLYPHIC_CANYON: 0x80576BE0 + (2 * SAVE_STRUCTURE_DETAILS.Size)
#}

#STAGE_CLEAR_ADDRESSES = \
#    {
#        (STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_DARK) : 0x80576BE0 + 4,
#        (STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_NEUTRAL): 0x80576BE0 + 4+(1*24),
#        (STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_HERO): 0x80576BE0 + 4+(2*24),#
#
#        (STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_DARK): 0x80576BE0 + (SAVE_STRUCTURE_DETAILS.Size * 1) + 4,
#        (STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_HERO): 0x80576BE0 + (SAVE_STRUCTURE_DETAILS.Size * 1) + 4 + (2 * 24),#
#
 #       (STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_DARK): 0x80576BE0 + (SAVE_STRUCTURE_DETAILS.Size * 2) + 4 + (2 * 24),
#        (STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_NEUTRAL): 0x80576BE0 + (SAVE_STRUCTURE_DETAILS.Size * 2) + 4 + (2 * 24),
#        (STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_HERO): 0x80576BE0 + (SAVE_STRUCTURE_DETAILS.Size * 2) + 4 + (2 * 24),
#    }

DARK_GAUGE_ADDRESS = 0x805766D4
HERO_GAUGE_ADDRESS = 0x805766C8
RINGS_ADDRESS = 0x8057670C

SPECIAL_WEAPONS_ADDRESS = 0x80578068
CURRENT_WEAPON_ID_ADDRESS = 0x805766F8
CURRENT_AMMO_ADDRESS = 0x80576700

def GetStageUnlockAddresses():
    unlock_addresses = {}

    for stage in Levels.ALL_STAGES:
        unlock_addresses[stage] = (westopolis_save_info_base_address +
                                                   (SAVE_STRUCTURE_DETAILS.Size * Levels.ALL_STAGES.index(stage)))

    return unlock_addresses

def GetKeysanityAddresses():
    unlock_addresses = []

    for i in range(0, 5):
        unlock_addresses.append(CURRENT_STAGE_BASE_KEYSANITY_ADDRESS + (i*0x4))

    return unlock_addresses

def GetStageClearAddresses():
    westopolis_save_info_base_address = 0x80576BE0

    clear_addresses = {}

    for stage in Levels.ALL_STAGES:
        stage_alignments = GetAlignmentsForStage(stage)
        for alignment in stage_alignments:
            clear_addresses[(stage, alignment)] = (westopolis_save_info_base_address +
                                                   (SAVE_STRUCTURE_DETAILS.Size * Levels.ALL_STAGES.index(stage)) + (alignment * 24)) + 4

    return clear_addresses


def writeBytes(addr, data):
    dolphin_memory_engine.write_bytes(addr, data)

ADDRESS_ALIEN_COUNT = 0x8057FB54
#ADDRESS_ALIEN_COUNT_BUT = 0x8057FB55
ADDRESS_SOLIDER_COUNT = 0x8057FB4C
ADDRESS_EGG_COUNT = 0x8057FB50

#ADDRESS_SEARCH_STANDARD = 0x8052B74C
#ADDRESS_MISSION_HERO_POINTER = 0x80575F04
#ADDRESS_MISSION_DARK_POINTER = 0x805F0E44

ADDRESS_MISSION_MANAGER = 0x80575EF8


ADDRESS_LAST_STORY_OPTION = 0x80578020
ADDRESS_WEAPONS_BYTES = 0x80578068
ADDRESS_LAST_CUTSCENE = 0x805EF2A0
ADDRESS_EXPERT_MODE_UNLOCK = 0x80578021
CUTSCENE_BUFFER = 0x805F7A2A
ADDRESS_MISSION_ALIGNMENT = 0x80575F1F


DEFAULT_SEARCH_INDEX = (16 * 6) + 8
SECONDARY_SEARCH_INDEX = (16 * 16) + 8
CC_HERO_INDEX = (30 * 16) + 4
PI_TD_HERO_INDEX = (16 * 6) + 4
DEFAULT_TOTAL_INDEX_HERO = (16 * 5) + 4
DEFAULT_TOTAL_INDEX = (16 * 5) + 8


StageAlignmentAddresses = [
    StageAlignmentAddress(STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_SOLIDER_COUNT),
    StageAlignmentAddress(STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_ALIEN_COUNT),

    StageAlignmentAddress(STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_DARK, None),

    StageAlignmentAddress(STAGE_LETHAL_HIGHWAY, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_DARK, None),
    StageAlignmentAddress(STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_ALIEN_COUNT),
    StageAlignmentAddress(STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_HERO, None),
    StageAlignmentAddress(STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_DARK, None),

    StageAlignmentAddress(STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_SOLIDER_COUNT),
    StageAlignmentAddress(STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_SOLIDER_COUNT),

    StageAlignmentAddress(STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_DARK, None),
    StageAlignmentAddress(STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_SOLIDER_COUNT),
    StageAlignmentAddress(STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_DARK, None),
    StageAlignmentAddress(STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_DARK, None),
    StageAlignmentAddress(STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_DEATH_RUINS, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_ALIEN_COUNT),

    StageAlignmentAddress(STAGE_THE_ARK, Levels.MISSION_ALIGNMENT_DARK, None),

    StageAlignmentAddress(STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_DARK, None),
    StageAlignmentAddress(STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_ALIEN_COUNT),

    StageAlignmentAddress(STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_SOLIDER_COUNT,),
    StageAlignmentAddress(STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_DARK, None),

    StageAlignmentAddress(STAGE_LOST_IMPACT, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_ALIEN_COUNT),

    StageAlignmentAddress(STAGE_GUN_FORTRESS, Levels.MISSION_ALIGNMENT_DARK, None),

    StageAlignmentAddress(STAGE_BLACK_COMET, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_SOLIDER_COUNT),

    StageAlignmentAddress(STAGE_LAVA_SHELTER, Levels.MISSION_ALIGNMENT_DARK, None),

    StageAlignmentAddress(STAGE_COSMIC_FALL, Levels.MISSION_ALIGNMENT_HERO, None),

    StageAlignmentAddress(STAGE_FINAL_HAUNT, Levels.MISSION_ALIGNMENT_DARK, None)
]

@dataclass
class CharacterAddress:
    name: str
    met_address: int

CharacterAddresses = [
    CharacterAddress("Sonic", 0x8057D77B),
    CharacterAddress("Tails", 0x8057D77F),
    CharacterAddress("Knuckles", 0x8057D783),
    CharacterAddress("Amy", 0x8057D787),
    CharacterAddress("Eggman", 0x8057D7A3),
    CharacterAddress("Rouge", 0x8057D78B),
    CharacterAddress("Omega", 0x8057D78F),
    CharacterAddress("Doom", 0x8057D7A7),
    CharacterAddress("Espio", 0x8057D797),
    CharacterAddress("Charmy", 0x8057D79F),
    CharacterAddress("Vector", 0x8057D793),
    CharacterAddress("Maria", 0x8057D79B),
]

def GetStageAlignmentAddress(stage_id, alignment_id):
    i = [ n for n in StageAlignmentAddresses if n.stageId == stage_id and n.alignmentId == alignment_id]
    if len(i) == 0:
        return None
    return i[0]


class ShTHContext(CommonContext):
    command_processor = ShTHCommandProcessor
    game = "Shadow The Hedgehog"
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.dolphin_sync_task: Optional[asyncio.Task] = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.awaiting_server = True
        self.last_rcvd_index = -1
        self.has_send_death = False
        self.available_levels = []

        self.items_to_handle = []
        self.handled = []
        self.level_state = {}
        self.characters_met = []
        self.checkpoint_snapshots = []
        self.lives = 0
        self.objective_sanity = False
        self.objective_percentage = 100
        self.objective_item_percentage = 100
        self.checkpoint_sanity = False
        self.character_sanity = False
        #self.checked_locations = []
        self.required_mission_tokens = 0
        self.required_hero_tokens = 0
        self.required_dark_tokens = 0
        self.required_final_tokens = 0
        self.required_objective_tokens = 0
        self.requires_emeralds = True
        self.key_sanity = False
        self.enemy_sanity = False
        self.enemy_objective_sanity = False
        self.weapon_sanity_unlock = False
        self.weapon_sanity_hold_option = 0
        self.vehicle_logic = False
        self.level_buffer = None
        self.ring_link = False
        self.auto_clear_missions = False

        self.hero_gauge_buffer = 0
        self.dark_gauge_buffer = 0
        self.junk_delay = 0

        self.tokens = []
        self.emeralds = []
        self.restart = False

        self.game_tags = []
        self.previous_rings = None
        self.ring_link_rings = 0
        self.instance_id = time.time()

        # Name of the current stage as read from the game's memory. Sent to trackers whenever its value changes to
        # facilitate automatically switching to the map of the current stage.
        self.current_stage_name: str = ""

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        self.current_stage_name = ""
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, username_requested: bool = True, password_requested: bool = False,
                          expectedUsername: str | None = None):
        if username_requested and not self.auth:
            await super(ShTHContext, self).get_username()
            if expectedUsername is not None and self.username != expectedUsername:
                self.auth = None
        if password_requested and not self.password:
            await super(ShTHContext, self).server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info("Awaiting connection to Dolphin to get player information")
            return
        logger.info("Auth complete, connecting")
        await self.send_connect()

    def restoreState(self):
        (mission_clear_locations, mission_locations, end_location, enemy_locations, \
            checkpointsanity_locations, charactersanity_locations,
         token_locations, keysanity_locations, weaponsanity_locations) = Locations.GetAllLocationInfo()

        if self.character_sanity:
            characters = []
            for character in CharacterAddresses:
                characterName = character.name
                charLocation = [char for char in charactersanity_locations if char.other == characterName]
                if len(charLocation) > 0:
                    characters.append(charLocation[0])

            already_checked_chars = [ c for c in characters if c.locationId in self.checked_locations ]
            for char in already_checked_chars:
                self.characters_met.append(char.other)




    def on_package(self, cmd: str, args: dict):
        print("on_package", cmd, args)
        if cmd == "Connected":
            slot_data = args["slot_data"]

            if "check_level" in slot_data:
                self.level_buffer = slot_data["check_level"]

            if "objective_sanity" in slot_data:
                self.objective_sanity = slot_data["objective_sanity"]

            if "objective_percentage" in slot_data:
                self.objective_percentage = slot_data["objective_percentage"]

            if "objective_item_percentage" in slot_data:
                self.objective_item_percentage = slot_data["objective_item_percentage"]

            if "checkpoint_sanity" in slot_data:
                self.checkpoint_sanity = slot_data["checkpoint_sanity"]

            if "character_sanity" in slot_data:
                self.character_sanity = slot_data["character_sanity"]

            if "key_sanity" in slot_data:
                self.key_sanity = slot_data["key_sanity"]

            if "required_mission_tokens" in slot_data:
                self.required_mission_tokens = slot_data["required_mission_tokens"]

            if "required_hero_tokens" in slot_data:
                self.required_hero_tokens = slot_data["required_hero_tokens"]

            if "required_dark_tokens" in slot_data:
                self.required_dark_tokens = slot_data["required_dark_tokens"]

            if "required_final_tokens" in slot_data:
                self.required_final_tokens = slot_data["required_final_tokens"]

            if "required_objective_tokens" in slot_data:
                self.required_objective_tokens = slot_data["required_objective_tokens"]

            if "requires_emeralds" in slot_data:
                self.requires_emeralds = slot_data["requires_emeralds"]

            if "enemy_sanity" in slot_data:
                self.enemy_sanity = slot_data["enemy_sanity"]

            if "enemy_objective_sanity" in slot_data:
                self.enemy_objective_sanity = slot_data["enemy_objective_sanity"]

            if "weapon_sanity_hold" in slot_data:
                self.weapon_sanity_hold_option = slot_data["weapon_sanity_hold"]

            if "weapon_sanity_unlock" in slot_data:
                self.weapon_sanity_unlock = slot_data["weapon_sanity_unlock"]

            if "vehicle_logic" in slot_data:
                self.vehicle_logic = slot_data["vehicle_logic"]

            if "ring_link" in slot_data:
                self.ring_link = slot_data["ring_link"]

            if "auto_clear_missions" in slot_data:
                self.auto_clear_missions = slot_data["auto_clear_missions"]

            self.restoreState()
            self.awaiting_server = False

            #self.items_received_2 = []
            #self.last_rcvd_index = -1
            #self.update_salvage_locations_map()
            #if "death_link" in args["slot_data"]:
            #    Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
            # Request the connected slot's dictionary (used as a set) of visited stages.
            #visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            #Utils.async_start(self.send_msgs([{"cmd": "Get", "keys": [visited_stages_key]}]))
        elif cmd == "ReceivedItems":
            print(args)
            if args["index"] >= self.last_rcvd_index:
                self.last_rcvd_index = args["index"]
                for item in args["items"]:
                    print("add item to handle", item)
                    self.items_to_handle.append((item, self.last_rcvd_index))
                    self.last_rcvd_index += 1
            self.items_to_handle.sort(key=lambda v: v[1])
            print(self.items_to_handle)
        elif cmd == "Retrieved":
            pass
        elif cmd == "Bounced":
            if "tags" in args:
                related_tags = args["tags"]
                if "RingLink" in related_tags:
                    handle_received_rings(self, args["data"])

            print(cmd, args)
            pass
            #requested_keys_dict = args["keys"]
            # Read the connected slot's dictionary (used as a set) of visited stages.
            #if self.slot is not None:
            #    visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            #    if visited_stages_key in requested_keys_dict:
            #        visited_stages = requested_keys_dict[visited_stages_key]
            #        # If it has not been set before, the value in the response will be None
            #       visited_stage_names = set() if visited_stages is None else set(visited_stages.keys())
            #        # If the current stage name is not in the set, send a message to update the dictionary on the
            #        # server.
            #        current_stage_name = self.current_stage_name
            #        if current_stage_name and current_stage_name not in visited_stage_names:
            #            visited_stage_names.add(current_stage_name)
            #            Utils.async_start(self.update_visited_stages(current_stage_name))
            #        self.visited_stage_names = visited_stage_names
        #Utils.async_start(self.process_shth_data(cmd, args))

    def on_deathlink(self, data: Dict[str, Any]):
        super().on_deathlink(data)
        #_give_death(self)

    def run_gui(self):
        from kvui import GameManager

        class ShTHManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago Shadow The Hedgehog"

        self.ui = ShTHManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def check_save_loaded(ctx):

    # Check a save is loaded. Write to static memory address with seed info
    # Determine save is invalid if seed isn't blank
    # Throw exception if save is not configured
    # If first load, set the memory to whether it can go in the save-data

    loaded = True
    mission_clear_locations, mission_locations, end_location, enemy_locations,\
        checkpointsanity_locations, charactersanity_locations,\
        token_locations, keysanity_locations, weaponsanity_locations = Locations.GetAllLocationInfo()

    # TODO: Check for newly obtained instead of all

    if loaded and len(ctx.level_state.keys()) == 0:
        pass

        per_stage = {}
        cleared_missions = []

        messages = []
        for stage_clear_address in GetStageClearAddresses().items():
            stage, alignment = stage_clear_address[0]
            clear_address = stage_clear_address[1]

            if stage not in ctx.available_levels:
                continue

            if not is_mission_completable(ctx, stage, alignment):
                continue

            current_bytes = dolphin_memory_engine.read_bytes(clear_address, 1)
            current_status = int.from_bytes(current_bytes, byteorder='big')

            if current_status == 1:
                cleared_missions.append((stage,alignment))
                if stage not in per_stage:
                    per_stage[stage] = []
                per_stage[stage].append(alignment)

                clear_location = [m for m in mission_clear_locations if m.stageId == stage
                                  and m.alignmentId == alignment and m.locationId not in ctx.checked_locations]

                associated_token_locations = [t for t in token_locations if t.alignmentId ==
                                              alignment and t.stageId == stage and t.locationId not in ctx.checked_locations]

                if len(associated_token_locations) > 0:
                    messages.extend([ a.locationId for a in associated_token_locations])

                if len(clear_location) == 1:
                    messages.append(clear_location[0].locationId)

        # decide settings for goal

        set_last_way = True

        if ctx.requires_emeralds:
            if len(ctx.emeralds) != 7:
                set_last_way = False

        if ctx.required_mission_tokens > 0:
            if len([ t for t in ctx.tokens if
                     t[1].name == Items.Progression.StandardMissionToken]) < ctx.required_mission_tokens:
                set_last_way = False

        if ctx.required_dark_tokens > 0:
            if len([t for t in ctx.tokens if
                    t[1].name == Items.Progression.StandardDarkToken]) < ctx.required_dark_tokens:
                set_last_way = False

        if ctx.required_hero_tokens > 0:
            if len([t for t in ctx.tokens if
                    t[1].name == Items.Progression.StandardHeroToken]) < ctx.required_hero_tokens:
                set_last_way = False

        if ctx.required_objective_tokens > 0:
            if len([t for t in ctx.tokens if
                    t[1].name == Items.Progression.ObjectiveToken]) < ctx.required_objective_tokens:
                set_last_way = False

        if ctx.required_final_tokens > 0:
            if len([t for t in ctx.tokens if
                    t[1].name == Items.Progression.FinalToken]) < ctx.required_final_tokens:
                set_last_way = False

        if set_last_way:
            set_to = 1
            set_last_way_bytes = set_to.to_bytes(1, byteorder='big')
            writeBytes(ADDRESS_LAST_STORY_OPTION, set_last_way_bytes)

            # Review
            for cutscene in range(0, 16):
                buffer_address_cutscene = CUTSCENE_BUFFER + (8 * cutscene)
                to_write = 0
                set_blank = to_write.to_bytes(4, byteorder='big')
                writeBytes(buffer_address_cutscene, set_blank)


        else:
            pass
            # TODO: Make it as to not write this constantly
            #set_to = 0
            #set_last_way_bytes = set_to.to_bytes(1, byteorder='big')
            #writeBytes(ADDRESS_LAST_STORY_OPTION, set_last_way_bytes)

        finished = False

        # TODO: Write 0s to cutscene chain to allow them to be skipped
        # Mainly for final story
        # If possible, work out how to kick the player out after TLW
        # Or don't let it finish, etc.

        last_cutscene_data = dolphin_memory_engine.read_bytes(ADDRESS_LAST_CUTSCENE, 4)
        last_cutscene_id = int.from_bytes(last_cutscene_data, byteorder='big')
        # Full CGI Cutscenes seem to go to  809F1300, which includes 8201!
        # 926 Is the moment Super Shadow is successful
        if last_cutscene_id in (926, 8201, 8202, 8203, 8204):
            finished = True

        if len(messages) > 0:
            unsent_messages = [ message for message in messages if message not in ctx.checked_locations]
            #ctx.locations_checked = messages
            message = [{"cmd": 'LocationChecks', "locations": unsent_messages}]
            await ctx.send_msgs(message)
            #ctx.locations_checked.extend(messages)

        if finished and not ctx.finished_game:
            ctx.finished_game = True
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL,
            }])

        # Check for mission completes

    return loaded


def HandleLocationAutoclears():
    location_dict = Locations.GetLocationInfoDict()
    all_locations = location_dict.values()
    level_clears = [ a for a in all_locations if a.location_type == Locations.LOCATION_TYPE_MISSION_CLEAR]
    space_gadget_hero = [ a for a in level_clears if a.stageId == STAGE_SPACE_GADGET
                             and a.alignmentId == MISSION_ALIGNMENT_HERO][0]

    space_gadget_neutral = [a for a in level_clears if a.stageId == STAGE_SPACE_GADGET
                         and a.alignmentId == MISSION_ALIGNMENT_NEUTRAL][0]

    cosmic_fall_hero = [a for a in level_clears if a.stageId == STAGE_COSMIC_FALL
                         and a.alignmentId == MISSION_ALIGNMENT_HERO][0]

    cosmic_fall_dark = [a for a in level_clears if a.stageId == STAGE_COSMIC_FALL
                         and a.alignmentId == MISSION_ALIGNMENT_DARK][0]

    digital_circuit_dark = [a for a in level_clears if a.stageId == STAGE_DIGITAL_CIRCUIT
                        and a.alignmentId == MISSION_ALIGNMENT_DARK][0]

    digital_circuit_hero = [a for a in level_clears if a.stageId == STAGE_DIGITAL_CIRCUIT
                        and a.alignmentId == MISSION_ALIGNMENT_HERO][0]

    return {
        space_gadget_neutral.locationId: space_gadget_hero,
        cosmic_fall_dark.locationId: cosmic_fall_hero,
        digital_circuit_hero.locationId: digital_circuit_dark
    }


# By handling in this function, all handling is auto-handled with stage access, etc as well!

def is_mission_completable(ctx, stage, alignment):
    relevant_clears = [ mc for mc in MissionClearLocations if mc.alignmentId == alignment and mc.stageId == stage]
    info = Items.GetItemLookupDict()

    if len(relevant_clears) == 0:
        return False
    clear = relevant_clears[0]

    if clear.requirement_count is None or not ctx.objective_sanity:
        return True

    required_count = ShadowUtils.getRequiredCount(clear.requirement_count, ctx.objective_item_percentage, round_method=ceil)

    i = [item for item in ctx.items_received if item.item in info and \
         info[item.item].stageId == stage and info[item.item].type == "level_object"
         and info[item.item].alignmentId == alignment]

    if len(i) >= required_count:
        return True

    return False

def complete_completable_levels(ctx):
    location_dict = Locations.GetLocationInfoDict()
    remaining_locations = ctx.missing_locations

    new_clears = []
    uncleared_stages = [ location_dict[l] for l in remaining_locations
                         if location_dict[l].location_type == Locations.LOCATION_TYPE_MISSION_CLEAR ]
                         #and location_dict[l].stageId == stageId and location_dict[l].alignmentId == alignmentId]
    for mission in uncleared_stages:

        if mission.stageId not in ctx.available_levels:
            continue

        completable = is_mission_completable(ctx, mission.stageId, mission.alignmentId)
        if not completable:
            continue

        # Check if mission is available
        # Check if mission is clearable

        mission_complete_locations = [ l for l in location_dict.values() if l.stageId == mission.stageId and
                               l.location_type == Locations.LOCATION_TYPE_MISSION_CLEAR
                               and l.locationId in ctx.checked_locations ]

        other_locations = [ l for l in remaining_locations if location_dict[l].stageId == mission.stageId and
                            location_dict[l].location_type != Locations.LOCATION_TYPE_MISSION_CLEAR and
                            location_dict[l].location_type != Locations.LOCATION_TYPE_TOKEN
                            ]

        if len(mission_complete_locations) > 0 and len(other_locations) == 0:
            new_clears.append(mission.locationId)
            # Mark as completed!
            pass

        auto_clears = HandleLocationAutoclears()
        if mission.locationId in auto_clears and auto_clears[mission.locationId].locationId in ctx.checked_locations:
            new_clears.append(mission.locationId)

    token_clears = []
    for clear in new_clears:
        clear_data = location_dict[clear]
        token_locations = [l for l in remaining_locations if location_dict[l].stageId == clear_data.stageId and \
                            clear_data.alignmentId == location_dict[l].alignmentId and
                           location_dict[l].location_type == Locations.LOCATION_TYPE_TOKEN ]
        token_clears.extend(token_locations)

    new_clears.extend(token_clears)
    return new_clears



# When not in a level, check the level
async def check_level_status(ctx):

    # If in a level, return the level ID

    # Sync level unlocked status
    # Add available levels to save-data

    # Check mission clears and keys and clear checks from those not known to the server
    info = Items.GetItemLookupDict()
    i = [
        unlock for unlock in ctx.items_to_handle if unlock[0].item in info
                                                    and info[unlock[0].item].type == "level_unlock"
         ]

    levels_to_unlock = [ info[level[0].item].stageId for level in i ]
    ctx.available_levels.extend(levels_to_unlock)

    item_behaviour_changed = False

    remove = []
    for ix in i:
        item_behaviour_changed = True
        ctx.handled.append(ix)
        remove.append(ix)

    for r in remove:
        ctx.items_to_handle.remove(r)

    # Set working address to set accessibility to levels
    # This data should save when the game is saved
    # Consider locking levels the player does not have access to

    #if 100 not in ctx.available_levels:
    #    ctx.available_levels.append(100)

    if item_behaviour_changed:
        for level in LEVEL_ID_TO_LEVEL.keys():
            if level in ctx.available_levels:
                new_count = 1
            else:
                new_count = 0

            address = GetStageUnlockAddresses()[level]
            current_value_bytes = dolphin_memory_engine.read_bytes(address, 4)
            current_value = int.from_bytes(current_value_bytes, byteorder='big')

            if ctx.level_buffer is not None and ctx.level_buffer == level:
                if current_value != 0:
                    continue

            if current_value != new_count:
                new_bytes = new_count.to_bytes(4, byteorder='big')
                writeBytes(address, new_bytes)

    found_emerald_items = [
        unlock for unlock in ctx.items_to_handle if unlock[0].item in info
                                                    and info[unlock[0].item].type == "emerald"
    ]

    remove = []
    for ix in found_emerald_items:
        item_no = ix[0].item
        if item_no not in ctx.emeralds:
            ctx.emeralds.append(item_no)
        ctx.handled.append(ix)
        remove.append(ix)

    for r in remove:
        ctx.items_to_handle.remove(r)

    found_token_items = [
        unlock for unlock in ctx.items_to_handle if unlock[0].item in info
                                                    and info[unlock[0].item].type == "Token"
    ]

    remove = []
    for ix in found_token_items:
        item_no = ix[0].item
        ctx.tokens.append((item_no, info[ix[0].item]))
        ctx.handled.append(ix)
        remove.append(ix)

    for r in remove:
        ctx.items_to_handle.remove(r)

    # need to handle receiving stage items here too

    force_retry = item_behaviour_changed

    ADDRESS_IN_LEVEL = 0x8057D74A
    ADDRESS_CURRENT_LEVEL = 0x80584722

    ADDRESS_LOADING_MAYBE = 0x80570B26

    if True:
        in_level = dolphin_memory_engine.read_byte(ADDRESS_IN_LEVEL)
        if in_level == 255:
            # Reset the level state when not in a level
            if len(ctx.level_state) != 0 or force_retry:
                ctx.level_state = {}
                if ctx.auto_clear_missions:
                    new_messages = complete_completable_levels(ctx)
                else:
                    new_messages = []
                if len(new_messages) > 0:
                    message = [{"cmd": 'LocationChecks', "locations": new_messages}]
                    await ctx.send_msgs(message)
                    check = [ l for l in HandleLocationAutoclears() if l in new_messages ]
                    if len(check) > 0:
                        ctx.level_state["temp"] = True

            return None
        else:

            loading_bytes = dolphin_memory_engine.read_bytes(ADDRESS_LOADING_MAYBE, 1)
            loading_value = int.from_bytes(loading_bytes, byteorder='big')

            if loading_value == 0:
                return None

            current_level_bytes = dolphin_memory_engine.read_bytes(ADDRESS_CURRENT_LEVEL, 2)
            current_level = int.from_bytes(current_level_bytes, byteorder='big')


            # Check if level has loaded

            #print(current_level)
            return current_level


COMPLETE_FLAG_OFF = 0
COMPLETE_FLAG_OFF_SET = 1
COMPLETE_FLAG_READY = 2
COMPLETE_FLAG_ON_SET = 3

async def disable_weapon(ctx):
    current_paused_data = dolphin_memory_engine.read_bytes(is_paused_address, 1)
    currently_paused = int.from_bytes(current_paused_data, byteorder='big') == 1
    
    if currently_paused:
        return
    
    current_dark_gauge_bytes = dolphin_memory_engine.read_bytes(DARK_GAUGE_ADDRESS, 4)
    current_dark_gauge = int.from_bytes(current_dark_gauge_bytes, byteorder="big")
    time.sleep(0.05)

    current_dark_gauge_bytes = dolphin_memory_engine.read_bytes(DARK_GAUGE_ADDRESS, 4)
    current_dark_gauge2 = int.from_bytes(current_dark_gauge_bytes, byteorder="big")

    current_hero_gauge_bytes = dolphin_memory_engine.read_bytes(HERO_GAUGE_ADDRESS, 4)
    current_hero_gauge = int.from_bytes(current_hero_gauge_bytes, byteorder="big")
    time.sleep(0.05)

    current_hero_gauge_bytes = dolphin_memory_engine.read_bytes(HERO_GAUGE_ADDRESS, 4)
    current_hero_gauge2 = int.from_bytes(current_hero_gauge_bytes, byteorder="big")

    print("add hero gauge:", ctx.hero_gauge_buffer, current_hero_gauge)
    ctx.hero_gauge_buffer += current_hero_gauge
    ctx.dark_gauge_buffer += current_dark_gauge

    ctx.junk_delay += 25

    new_bytes = int(0).to_bytes(4, byteorder='big')
    writeBytes(DARK_GAUGE_ADDRESS, new_bytes)

    new_bytes = int(0).to_bytes(4, byteorder='big')
    writeBytes(HERO_GAUGE_ADDRESS, new_bytes)

    # Sleep not preferable, required to ensure game processes end of dark/hero gauge in case of active power Shadow
    # Which would then not drop the weapon!

    if current_hero_gauge2 < current_hero_gauge or \
        current_dark_gauge2 < current_dark_gauge:
        time.sleep(0.5)

    new_bytes = int(0).to_bytes(4, byteorder='big')
    writeBytes(CURRENT_AMMO_ADDRESS, new_bytes)


async def check_weapons(ctx):
    info = Items.GetItemLookupDict()

    weapons_to_handle = [unlock for unlock in ctx.items_to_handle if unlock[0].item in info and \
         info[unlock[0].item].type == "Weapon"]

    newly_handled = []
    newly_handled.extend(weapons_to_handle)

    mission_clear_locations, mission_locations, end_location, enemysanity_locations, \
        checkpointsanity_locations, charactersanity_locations, \
        token_locations, keysanity_locations, weaponsanity_locations = Locations.GetAllLocationInfo()

    messages = []

    weapon_dict = Weapons.GetWeaponDict()
    special_weapons_info = Items.GetSpecialWeapons()
    if len(weapons_to_handle) > 0:
        special_weapons = [ info[unlock[0].item] for unlock in ctx.handled if unlock[0].item in info \
             and info[unlock[0].item].type == "Weapon" and
                    Weapons.WeaponAttributes.SPECIAL in weapon_dict[info[unlock[0].item].name].attributes ]

        special_weapons_new = [info[unlock[0].item] for unlock in weapons_to_handle if unlock[0].item in info \
                           and info[unlock[0].item].type == "Weapon" and
                           Weapons.WeaponAttributes.SPECIAL in weapon_dict[info[unlock[0].item].name].attributes]

        special_weapons.extend(special_weapons_new)

        weapon_value = [ 0,0,0,0,0,0,0,0,0,0,0 ]
        i = 0
        for special_weapon in special_weapons_info:
            matching = [ w for w in special_weapons if w.name == special_weapon.name or
                         w.name == "Weapon:"+special_weapon.name ]
            if len(matching) >= 1:
                weapon_value[i] = 1
            if len(matching) >= 2 and i+1 < len(weapon_value):
                weapon_value[i+1] = 1
            i += 2

        weapon_value.reverse()

        weapon_value_write = int("".join([ str(w) for w in weapon_value]),2)
        new_bytes = weapon_value_write.to_bytes(2, byteorder='big')
        writeBytes(SPECIAL_WEAPONS_ADDRESS, new_bytes)

        remove = []
        for r in newly_handled:
            ctx.handled.append(r)
            remove.append(r)

        for r in remove:
            ctx.items_to_handle.remove(r)

    if ctx.weapon_sanity_unlock or ctx.weapon_sanity_hold_option > 0:
        current_weapon_bytes = dolphin_memory_engine.read_bytes(CURRENT_WEAPON_ID_ADDRESS, 4)
        current_weapon_id = int.from_bytes(current_weapon_bytes, byteorder="big")

        weapon_dict = Weapons.GetWeaponDict()
        special_weapons_lower = []
        for special in special_weapons_info:
            if special.name in weapon_dict and Weapons.WeaponAttributes.SPECIAL in weapon_dict[special.name].attributes \
                    and special.name != "Shadow Rifle":
                special_weapons_lower.append(weapon_dict[special.name].game_id - 1)
                pass
            elif ("Weapon:" + special.name in weapon_dict and Weapons.WeaponAttributes.SPECIAL in
                  weapon_dict["Weapon:" + special.name].attributes and special.name != "Shadow Rifle"):
                special_weapons_lower.append(weapon_dict["Weapon:" + special.name].game_id - 1)
                pass

        if len([l for l in special_weapons_lower if l == current_weapon_id]) > 0:
            current_weapon_id = current_weapon_id + 1

        if ctx.weapon_sanity_unlock:
            allowed_weapons = [weapon_dict[info[unlock[0].item].name] for unlock in ctx.handled if unlock[0].item in info and \
                                 info[unlock[0].item].type == "Weapon"]

            allowed_weapons_by_id = {}
            for a in allowed_weapons:
                allowed_weapons_by_id[a.game_id] = a

            valid_weapon_ids = [ weapon.game_id for weapon in weapon_dict.values() ]
            if current_weapon_id == 0:
                current_weapon_id = None
            elif current_weapon_id not in valid_weapon_ids:
                logger.error("Unknown weapon held by player:"+str(current_weapon_id))
                current_weapon_id = None
            elif current_weapon_id not in allowed_weapons_by_id.keys():
                await disable_weapon(ctx)

                if ctx.weapon_sanity_hold_option == WeaponsanityHold.option_unlocked:
                    current_weapon_id = None

        if current_weapon_id is not None and ctx.weapon_sanity_hold_option in \
                (WeaponsanityHold.option_unlocked, WeaponsanityHold.option_on):
            weapon_dict = Weapons.GetWeaponDictById()

            current_weapon = weapon_dict[current_weapon_id]
            weapon_locations = [ l.locationId for l in weaponsanity_locations if l.other == current_weapon.name and \
                                 l.locationId not in ctx.handled ]
            messages.extend(weapon_locations)

            pass


    if len(messages) > 0:
        # ctx.locations_checked = messages
        message = [{"cmd": 'LocationChecks', "locations": messages}]
        await ctx.send_msgs(message)

def get_last_index_storage_location(ctx):
    if ctx.level_buffer is None:
        return None
    return [ l[1] for l in GetStageUnlockAddresses().items() if l[0] == ctx.level_buffer ][0]

def get_last_index(ctx):
    decided_last_index_address = get_last_index_storage_location(ctx)

    current_potential_bytes = dolphin_memory_engine.read_bytes(decided_last_index_address, 4)
    current_potential = int.from_bytes(current_potential_bytes[1:3], byteorder="big")

    return current_potential


def set_last_index(ctx, new_value):
    decided_last_index_address = get_last_index_storage_location(ctx)

    current_potential_bytes = list(dolphin_memory_engine.read_bytes(decided_last_index_address, 4))
    bytes_to_manip = list(new_value.to_bytes(2, byteorder="big"))
    current_potential_bytes[1] = bytes_to_manip[0]
    current_potential_bytes[2] = bytes_to_manip[1]
    potential_bytes = bytes(current_potential_bytes)
    writeBytes(decided_last_index_address, potential_bytes)


async def handle_ring_link(ctx, level, death):
    ring_link = False
    old_tags = ctx.game_tags.copy()
    if ctx.ring_link:
        if "RingLink" not in ctx.game_tags:
            ctx.game_tags.append("RingLink")
        ring_link = True
    else:
        ctx.game_tags = []
    if old_tags != ctx.game_tags and ctx.server and not ctx.server.socket.closed:
        await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.game_tags}])

    if level is None or not ring_link:
        ctx.previous_rings = None
        return

    difference = 0
    if not death:
        previous = ctx.previous_rings
        current_rings_bytes = dolphin_memory_engine.read_bytes(RINGS_ADDRESS, 4)
        current_rings = int.from_bytes(current_rings_bytes, byteorder="big")


        if current_rings == 0 and ctx.previous_rings is not None and ctx.previous_rings > 20:
            # count as death scenario rather
            pass
        elif ctx.previous_rings is None:
            ctx.previous_rings = current_rings
        else:
            ctx.previous_rings = current_rings
            difference = current_rings - previous
            if difference != 0:
                print("ring diff=", difference)

    if difference != 0:
        msg = {
            "cmd": "Bounce",
            "slots": [ctx.slot],
            "data": {
                "time":  time.time(),
                "source": ctx.instance_id,
                "amount": difference
            },
            "tags": ctx.game_tags
        }

        await ctx.send_msgs([msg])

def handle_received_rings(ctx, data):
    amount = data["amount"]
    source = data["source"]

    if source == ctx.instance_id:
        return

    ctx.ring_link_rings += amount
    ctx.previous_rings = None


async def check_junk(ctx, current_level):
    info = Items.GetItemLookupDict()

    if ctx.junk_delay > 0:
        ctx.junk_delay -= 1
        return

    last_index = get_last_index(ctx)

    filler = [(unlock,info[unlock[0].item]) for unlock in ctx.items_to_handle if unlock[0].item in info and \
        info[unlock[0].item].classification == ItemClassification.filler and unlock[1] > last_index ]

    latest_index = None

    if len(filler) > 0:
        latest_index = max([ u[0][1] for u in filler])

    filler_nothing = [ f for f in filler if f[1].name == Junk.NothingJunk]
    filler_gauge_dark = [ f for f in filler if f[1].type == "gauge" and f[1].alignmentId == MISSION_ALIGNMENT_DARK]
    filler_gauge_hero = [ f for f in filler if f[1].type == "gauge" and f[1].alignmentId == MISSION_ALIGNMENT_HERO]
    filler_rings = [ f for f in filler if f[1].type == "rings"]


    newly_handled = []
    newly_handled.extend([f[0] for f in filler_nothing])

    RING_LIMIT = 999
    GAUGE_LIMIT = 30000
    if (len(filler_rings) > 0 and current_level != Levels.STAGE_CIRCUS_PARK) or ctx.ring_link_rings != 0:
        current_rings_bytes = dolphin_memory_engine.read_bytes(RINGS_ADDRESS, 4)
        current_rings = int.from_bytes(current_rings_bytes, byteorder="big")
        rings_changed = False
        for ringJunk in filler_rings:
            if current_rings >= RING_LIMIT:
                break
            if current_rings + ringJunk[1].value >= RING_LIMIT:
                continue

            current_rings += ringJunk[1].value
            newly_handled.append(ringJunk[0])
            rings_changed = True

        if ctx.ring_link_rings != 0 and ctx.ring_link_rings is not None:
            rings_changed = True
            current_rings += ctx.ring_link_rings
            if current_rings < 0:
                current_rings = 0
            ctx.ring_link_rings = 0

        if rings_changed:
            new_bytes = current_rings.to_bytes(4, byteorder='big')
            writeBytes(RINGS_ADDRESS, new_bytes)

    if len(filler_gauge_hero) > 0:
        for gaugeJunk in filler_gauge_hero:
            print("add hero gauge:", ctx.hero_gauge_buffer, gaugeJunk[1].value)
            ctx.hero_gauge_buffer += gaugeJunk[1].value
            newly_handled.append(gaugeJunk[0])

    if ctx.hero_gauge_buffer > 0:

        current_hero_gauge_bytes = dolphin_memory_engine.read_bytes(HERO_GAUGE_ADDRESS, 4)
        current_hero_gauge = int.from_bytes(current_hero_gauge_bytes, byteorder="big")

        increase = GAUGE_LIMIT - current_hero_gauge
        if ctx.hero_gauge_buffer < increase:
            increase = ctx.hero_gauge_buffer

        if ctx.hero_gauge_buffer > 1000 and increase < 1000:
            print("gauge diff too small", ctx.hero_gauge_buffer, increase)
        else:
            print("gauge diff", ctx.hero_gauge_buffer, increase)
            ctx.hero_gauge_buffer -= increase

            new_hero_value = current_hero_gauge + increase
            print("new hero", new_hero_value)
            new_bytes = new_hero_value.to_bytes(4, byteorder='big')
            writeBytes(HERO_GAUGE_ADDRESS, new_bytes)

    if len(filler_gauge_dark) > 0:
        for gaugeJunk in filler_gauge_dark:
            ctx.dark_gauge_buffer += gaugeJunk[1].value
            newly_handled.append(gaugeJunk[0])

    if ctx.dark_gauge_buffer > 0:
        current_dark_gauge_bytes = dolphin_memory_engine.read_bytes(DARK_GAUGE_ADDRESS, 4)
        current_dark_gauge = int.from_bytes(current_dark_gauge_bytes, byteorder="big")

        increase = GAUGE_LIMIT - current_dark_gauge
        if ctx.dark_gauge_buffer < increase:
            increase = ctx.dark_gauge_buffer

        if ctx.dark_gauge_buffer > 1000 and increase < 1000:
            print("gauge diff too small", ctx.dark_gauge_buffer, increase)
        else:
            ctx.dark_gauge_buffer -= increase

            new_dark_value = current_dark_gauge + increase
            new_bytes = new_dark_value.to_bytes(4, byteorder='big')
            writeBytes(DARK_GAUGE_ADDRESS, new_bytes)

    remove = []
    for r in newly_handled:
        ctx.handled.append(r)
        remove.append(r)

    for r in remove:
        ctx.items_to_handle.remove(r)

    if latest_index is not None:
        set_last_index(ctx, latest_index)


async def update_level_behaviour(ctx, current_level, death):
    # based on the level
    # work out which addresses to use for checks for each mission objective
    # handle picked up keys as they picked up
    # handle enemy counters if checks are enabled
    # Set initial value (to level of value from server)
    # If higher than previous value, recognise as check and reduce by 1



    # Add handle for first load of level, when state is blank

    info = Items.GetItemLookupDict()
    mission_clear_locations, mission_locations, end_location, enemysanity_locations,\
        checkpointsanity_locations, charactersanity_locations,\
        token_locations, keysanity_locations, weaponsanity_locations = Locations.GetAllLocationInfo()

    handle_count = 0

    if death or ctx.restart:
        if len(ctx.checkpoint_snapshots) > 0 and not ctx.restart:
            last_snapshot = ctx.checkpoint_snapshots[-1][1]
            ctx.level_state = deepcopy(last_snapshot)
        else:
            ctx.level_state = {}
            pass
        ctx.restart = False

    await check_weapons(ctx)
    await check_junk(ctx, current_level)

    if len(ctx.level_state.keys()) == 0:
        ctx.level_state["active"] = True
        ctx.level_state["hero_count"] = 0
        ctx.level_state["hero_active"] = True
        ctx.level_state["dark_count"] = 0
        ctx.level_state["dark_active"] = True
        ctx.level_state["hero_completable"] = COMPLETE_FLAG_OFF
        ctx.level_state["dark_completable"] = COMPLETE_FLAG_OFF
        ctx.level_state["hero_progress"] = 0
        ctx.level_state["dark_progress"] = 0
        ctx.level_state["characters_set"] = False

        ctx.level_state["alien_progress"] = 0
        ctx.level_state["egg_progress"] = 0
        ctx.level_state["gun_progress"] = 0
        ctx.level_state["key_index"] = 0

        ctx.checkpoint_snapshots = []

        i = [unlock for unlock in ctx.handled if unlock[0].item in info and \
             info[unlock[0].item].stageId == current_level and info[unlock[0].item].type == "level_object"]

        group_by_alignment = {}
        for ix in i:
            item = info[ix[0].item]
            if item.alignmentId not in group_by_alignment:
                group_by_alignment[item.alignmentId] = []
            group_by_alignment[item.alignmentId].append(item)

        if ctx.level_state["hero_active"] and ctx.objective_sanity:
            if Levels.MISSION_ALIGNMENT_HERO in group_by_alignment:
                hero_count = len(group_by_alignment[Levels.MISSION_ALIGNMENT_HERO])
                handle_count += 1
            else:
                hero_count = 0

            ctx.level_state["hero_count"] = hero_count

        if ctx.level_state["dark_active"] and ctx.objective_sanity:
            if Levels.MISSION_ALIGNMENT_DARK in group_by_alignment:
                dark_count = len(group_by_alignment[Levels.MISSION_ALIGNMENT_DARK])
                handle_count += 1
            else:
                dark_count = 0
            ctx.level_state["dark_count"] = dark_count

    current_alignment = dolphin_memory_engine.read_byte(ADDRESS_MISSION_ALIGNMENT)

    i = [unlock for unlock in ctx.items_to_handle if unlock[0].item in info and \
         info[unlock[0].item].stageId == current_level and \
         #info[unlock[0].item].alignmentId == current_alignment and
         info[unlock[0].item].type == "level_object" ]

    remove = []
    for ix in i:
        if info[ix[0].item].alignmentId == Levels.MISSION_ALIGNMENT_DARK and ctx.objective_sanity:
            ctx.level_state["dark_count"] += 1
        elif info[ix[0].item].alignmentId == Levels.MISSION_ALIGNMENT_HERO and ctx.objective_sanity:
            ctx.level_state["hero_count"] += 1
        ctx.handled.append(ix)
        remove.append(ix)
        handle_count += 1

    for r in remove:
        ctx.items_to_handle.remove(r)

    #hero_address = None
    #dark_address = None
    dark_write = None
    hero_write = None


    hero_address_data = GetStageAlignmentAddress(current_level, Levels.MISSION_ALIGNMENT_HERO)
    dark_address_data = GetStageAlignmentAddress(current_level, Levels.MISSION_ALIGNMENT_DARK)

    hero_address = None
    hero_address_size = 4

    dark_address = None
    dark_address_size = 4

    hero_address_total = None
    dark_address_total = None

    hero_max_hit = False
    dark_max_hit = False

    alien_address_size = 4
    gun_address_size = 4
    egg_address_size = 4

    restore_hero = False
    restore_dark = False

    dark_default_tally_address = None
    dark_working_1_address_bytes = dolphin_memory_engine.read_bytes(ADDRESS_MISSION_MANAGER + 16, 4)
    dark_working_1_address = int.from_bytes(dark_working_1_address_bytes, byteorder="big")
    if dark_working_1_address != 0:
        dark_working_2_address_bytes = dolphin_memory_engine.read_bytes(dark_working_1_address + 12, 4)
        dark_working_2_address = int.from_bytes(dark_working_2_address_bytes, byteorder="big")
        if dark_working_2_address != 0:
            dark_address_total = dark_working_2_address + 8
            dark_default_tally_address = dark_address_total + 16

    hero_default_tally_address = None
    hero_working_1_address_bytes = dolphin_memory_engine.read_bytes(ADDRESS_MISSION_MANAGER + 32, 4)
    hero_working_1_address = int.from_bytes(hero_working_1_address_bytes, byteorder="big")
    if hero_working_1_address != 0:
        hero_working_2_address_bytes = dolphin_memory_engine.read_bytes(hero_working_1_address + 12, 4)
        hero_working_2_address = int.from_bytes(hero_working_2_address_bytes, byteorder="big")
        if hero_working_2_address != 0:
            hero_address_total = hero_working_2_address + 8
            hero_default_tally_address = hero_address_total + 16

    if hero_address_data is not None:
        if hero_address_data.tally_address is not None:
            hero_address = hero_address_data.tally_address
        else:
            hero_address = hero_default_tally_address

    if dark_address_data is not None:
        if dark_address_data.tally_address is not None:
            dark_address = dark_address_data.tally_address
        else:
            dark_address = dark_default_tally_address

    #if hero_address_data is not None and hero_address is not None:
    #    current_pointer = dolphin_memory_engine.read_bytes(hero_address, hero_address_size)
    #    mission_requirement_count = int.from_bytes(current_pointer, byteorder="big") + hero_address_data.searchIndex
    #    hero_address = mission_requirement_count

    #if dark_address_data is not None and dark_address_data.searchIndex is not None:
    #    current_pointer = dolphin_memory_engine.read_bytes(dark_address, dark_address_size)
    #    mission_requirement_count = int.from_bytes(current_pointer, byteorder="big") + dark_address_data.searchIndex
    #    dark_address = mission_requirement_count

    stageInfo = GetStageInformation(current_level)
    heroInfo = None
    stageInfoHero = [ s for s in stageInfo if s.alignmentId == Levels.MISSION_ALIGNMENT_HERO ]
    if len(stageInfoHero) > 0 and hero_address is not None:
        heroInfo = stageInfoHero[0]

    darkInfo = None
    stageInfoDark = [s for s in stageInfo if s.alignmentId == Levels.MISSION_ALIGNMENT_DARK]
    if len(stageInfoDark) > 0 and dark_address is not None:
        darkInfo = stageInfoDark[0]

    EnemyInfo = GetStageEnemysanityInformation(current_level)
    alienInfo = None
    stageInfoAlien = [s for s in EnemyInfo if s.enemyClass == Locations.ENEMY_CLASS_ALIEN]
    if len(stageInfoAlien) > 0:
        alienInfo = stageInfoAlien[0]
    gunInfo = None
    stageInfoGun = [s for s in EnemyInfo if s.enemyClass == Locations.ENEMY_CLASS_GUN]
    if len(stageInfoGun) > 0:
        gunInfo = stageInfoGun[0]
    eggInfo = None
    stageInfoEgg = [s for s in EnemyInfo if s.enemyClass == Locations.ENEMY_CLASS_EGG]
    if len(stageInfoEgg) > 0:
        eggInfo = stageInfoEgg[0]

    if heroInfo is not None and heroInfo.requirement_count is not None:
        hero_count = ctx.level_state["hero_count"]
        heroMax = heroInfo.requirement_count
        heroMaxAdjusted = ShadowUtils.getRequiredCount(heroMax, ctx.objective_item_percentage, round_method=ceil)
        hero_write = hero_count
        if ctx.objective_sanity:
            restore_hero = True

        hero_completable = ctx.level_state["hero_completable"]
        if hero_completable == COMPLETE_FLAG_OFF:
            set_max_up = True
            if ctx.objective_sanity:
                hero_count_max = heroMax + 2
                if ctx.level_state["hero_count"] > hero_count_max:
                    hero_count_max = ctx.level_state["hero_count"] + 2
            else:
                hero_count_max = heroMaxAdjusted
            ctx.level_state["hero_completable"] = COMPLETE_FLAG_OFF_SET
        elif hero_completable == COMPLETE_FLAG_READY:
            set_max_up = True
            hero_count_max = heroMaxAdjusted
            ctx.level_state["hero_completable"] = COMPLETE_FLAG_ON_SET
            handle_count = True
        else:
            set_max_up = False
            hero_count_max = 255

        if hero_count >= heroMaxAdjusted:
            hero_max_hit = True

        if set_max_up and hero_address_total is not None:
            new_count = hero_count_max
            new_bytes = new_count.to_bytes(hero_address_size, byteorder='big')
            writeBytes(hero_address_total, new_bytes)

        if handle_count > 0 and hero_write is not None and ctx.objective_sanity:
            new_count = hero_write
            new_bytes = new_count.to_bytes(hero_address_size, byteorder='big')
            writeBytes(hero_address, new_bytes)

    if darkInfo is not None and darkInfo.requirement_count is not None:
        dark_count = ctx.level_state["dark_count"]
        dark_write = dark_count
        darkMax = darkInfo.requirement_count
        darkMaxAdjusted = ShadowUtils.getRequiredCount(darkMax, ctx.objective_item_percentage, round_method=ceil)
        if ctx.objective_sanity:
            restore_dark = True
        dark_completable = ctx.level_state["dark_completable"]
        if dark_completable == COMPLETE_FLAG_OFF:
            set_max_up = True
            if ctx.objective_sanity:
                dark_count_max = darkMax + 2
                if ctx.level_state["dark_count"] > dark_count_max:
                    dark_count_max = ctx.level_state["dark_count"] + 2
            else:
                dark_count_max = darkMaxAdjusted
            ctx.level_state["dark_completable"] = COMPLETE_FLAG_OFF_SET
        elif dark_completable == COMPLETE_FLAG_READY:
            set_max_up = True
            dark_count_max = darkMaxAdjusted
            ctx.level_state["dark_completable"] = COMPLETE_FLAG_ON_SET
            handle_count = True
        else:
            set_max_up = False
            dark_count_max = 255

        if dark_count >= darkMaxAdjusted:
            dark_max_hit = True

        if set_max_up and dark_address_total is not None:
            #dark_total_address = dark_address - 16
            #if dark_address == ADDRESS_SOLIDER_COUNT:
            #
            #    current_pointer = dolphin_memory_engine.read_bytes(ADDRESS_MISSION_DARK_POINTER, dark_address_size)
            #    mission_requirement_count = (int.from_bytes(current_pointer, byteorder="big") +
            #                                 dark_address_data.totalSearchIndex)
            #    dark_total_address = mission_requirement_count
            #else:
            #    dark_total_address = dark_address - 16

            new_count = dark_count_max
            new_bytes = new_count.to_bytes(dark_address_size, byteorder='big')
            writeBytes(dark_address_total, new_bytes)

        if handle_count > 0 and dark_write is not None and ctx.objective_sanity:
            new_count = dark_write
            new_bytes = new_count.to_bytes(dark_address_size, byteorder='big')
            writeBytes(dark_address, new_bytes)

    ## Handle new events

    expected_hero_value = hero_write
    expected_dark_value = dark_write

    hero_progress = False
    dark_progress = False

    alien_progress = False
    gun_progress = False
    egg_progress = False

    enemysanity = ctx.enemy_sanity
    objective_enemysanity = ctx.enemy_objective_sanity

    if hero_address is not None:
        current_bytes = dolphin_memory_engine.read_bytes(hero_address, hero_address_size)
        current_count = int.from_bytes(current_bytes, byteorder='big')

        if expected_hero_value is not None and current_count > expected_hero_value:
            print("hero count increased --", current_count, expected_hero_value)
            valid_compare_count = heroInfo.requirement_count + 2
            if ctx.level_state["hero_progress"] > heroInfo.requirement_count:
                valid_compare_count = ctx.level_state["hero_progress"] + 2
            if current_count > valid_compare_count:
                print("invalid value read for hero count:", current_count)
            new_count = (current_count - expected_hero_value)
            ctx.level_state["hero_progress"] += new_count
            if not ctx.objective_sanity:
                ctx.level_state["hero_count"] += new_count
            hero_progress = True
            if enemysanity and hero_address == ADDRESS_ALIEN_COUNT:
                ctx.level_state["alien_progress"] += new_count
                alien_progress = True
        #elif expected_hero_value > current_count >= 0:
        #    ctx.level_state["hero_progress"] = current_count

        if hero_address is not None and hero_write is not None and restore_hero:
            new_count = expected_hero_value
            new_bytes = new_count.to_bytes(4, byteorder='big')
            writeBytes(hero_address, new_bytes)

    if dark_address is not None:
        current_bytes = dolphin_memory_engine.read_bytes(dark_address, dark_address_size)
        current_count = int.from_bytes(current_bytes, byteorder='big')

        if expected_dark_value is not None and current_count > expected_dark_value:
            print("dark count increased --", current_count, expected_dark_value)
            valid_compare_count = darkInfo.requirement_count + 2
            if ctx.level_state["dark_progress"] > darkInfo.requirement_count:
                valid_compare_count = ctx.level_state["dark_progress"] + 2
            if current_count > valid_compare_count:
                print("invalid value read for dark count:", current_count)
            else:
                new_count = (current_count - expected_dark_value)
                ctx.level_state["dark_progress"] += new_count
                dark_progress = True
                if not ctx.objective_sanity:
                    ctx.level_state["dark_count"] += new_count
                if enemysanity and dark_address == ADDRESS_SOLIDER_COUNT:
                    ctx.level_state["gun_progress"] += new_count
                    gun_progress = True
        #elif expected_dark_value > current_count >= 0:
        #    ctx.level_state["dark_progress"] = current_count

        if dark_address is not None and dark_write is not None and restore_dark:
            new_count = expected_dark_value
            new_bytes = new_count.to_bytes(4, byteorder='big')
            writeBytes(dark_address, new_bytes)

    if enemysanity and hero_address != ADDRESS_ALIEN_COUNT and alienInfo is not None:
        alien_count = ctx.level_state["alien_progress"]

        current_bytes = dolphin_memory_engine.read_bytes(ADDRESS_ALIEN_COUNT, alien_address_size)
        current_count = int.from_bytes(current_bytes, byteorder='big')

        if current_count > alien_count:
            print("alien count increased --", current_count, alien_count)
            if current_count > alienInfo.total_count + 2:
                print("invalid value read for alien count:", current_count)
            ctx.level_state["alien_progress"] += (current_count - alien_count)
            alien_progress = True

    if enemysanity and dark_address != ADDRESS_SOLIDER_COUNT and gunInfo is not None:
        gun_count = ctx.level_state["gun_progress"]

        current_bytes = dolphin_memory_engine.read_bytes(ADDRESS_SOLIDER_COUNT, gun_address_size)
        current_count = int.from_bytes(current_bytes, byteorder='big')

        if current_count > gun_count:
            print("gun count increased --", current_count, gun_count)
            if current_count > gunInfo.total_count + 2:
                print("invalid value read for GUN count:", current_count)
            ctx.level_state["gun_progress"] += (current_count - gun_count)
            gun_progress = True

    if enemysanity and hero_address != ADDRESS_EGG_COUNT and eggInfo is not None:
        egg_count = ctx.level_state["egg_progress"]

        current_bytes = dolphin_memory_engine.read_bytes(ADDRESS_EGG_COUNT, egg_address_size)
        current_count = int.from_bytes(current_bytes, byteorder='big')

        if current_count > egg_count:
            print("egg count increased --", current_count, egg_count)
            if current_count > eggInfo.total_count + 2:
                print("invalid value read for egg count:", current_count)
            ctx.level_state["egg_progress"] += (current_count - egg_count)
            egg_progress = True

    messages = []
    if hero_progress or dark_progress or alien_progress or gun_progress or egg_progress:
        # TODO: Check which check we are up to for hero and dark
        # Send only unchecked locations
        # Need state to be restorable maybe


        # Signal archipelago a check has been made
        if hero_progress:
            progress_locations = [ l.locationId for l in mission_locations if l.alignmentId == Levels.MISSION_ALIGNMENT_HERO and \
                l.stageId == current_level and l.count <= ctx.level_state["hero_progress"] and l.locationId not in ctx.checked_locations ]
            messages.extend(progress_locations)

        if dark_progress:
            progress_locations = [ l.locationId for l in mission_locations if l.alignmentId == Levels.MISSION_ALIGNMENT_DARK and \
                l.stageId == current_level and l.count <= ctx.level_state["dark_progress"]
                                   and l.locationId not in ctx.checked_locations]
            if len(progress_locations) > 0:
                messages.extend(progress_locations)

        if alien_progress:
            progress_locations = [l.locationId for l in enemysanity_locations if
                                  l.alignmentId == Locations.ENEMY_CLASS_ALIEN and \
                                  l.stageId == current_level and l.count <= ctx.level_state["alien_progress"]
                                  and l.locationId not in ctx.checked_locations]
            if len(progress_locations) > 0:
                messages.extend(progress_locations)

        if gun_progress:
            progress_locations = [l.locationId for l in enemysanity_locations if
                                  l.alignmentId == Locations.ENEMY_CLASS_GUN and \
                                  l.stageId == current_level and l.count <= ctx.level_state["gun_progress"]
                                  and l.locationId not in ctx.checked_locations]
            if len(progress_locations) > 0:
                messages.extend(progress_locations)

        if egg_progress:
            progress_locations = [l.locationId for l in enemysanity_locations if
                                  l.alignmentId == Locations.ENEMY_CLASS_EGG and \
                                  l.stageId == current_level and l.count <= ctx.level_state["egg_progress"]
                                  and l.locationId not in ctx.checked_locations]
            if len(progress_locations) > 0:
                messages.extend(progress_locations)

    if ctx.character_sanity:
        for character in CharacterAddresses:
            if character.name in ctx.characters_met:
                continue
            characterSet_bytes = dolphin_memory_engine.read_bytes(character.met_address, 1)
            characterSet = int.from_bytes(characterSet_bytes, byteorder='big') == 1
            if characterSet:
                charLocation = [ char.locationId for char in charactersanity_locations if char.other == character.name ]
                if len(charLocation) > 0:
                    if charLocation[0] not in ctx.checked_locations:
                        messages.append(charLocation[0])
                        ctx.characters_met.append(character.name)
    else:
        if len(ctx.characters_met) == 0:
            ctx.characters_met.extend(
                [c.name for c in CharacterAddresses]
            )

    if not ctx.level_state["characters_set"]:
        for character in ctx.characters_met:
            relevantCharData = [c for c in CharacterAddresses if c.name == character]
            if len(relevantCharData) != 0:
                relevantChar = relevantCharData[0]
                new_value = 1
                new_bytes = new_value.to_bytes(1, byteorder='big')
                writeBytes(relevantChar.met_address, new_bytes)

        ctx.level_state["characters_set"] = True

    # Check checkpoint flags and save the state when a new one is activated
    checkpoint_data_for_stage = [c for c in Locations.CheckpointLocations if c.stageId == current_level]
    if len(checkpoint_data_for_stage) > 0:
        total_count = checkpoint_data_for_stage[0].total_count
        max_checkpoint_bytes = dolphin_memory_engine.read_bytes(CHECKPOINT_MAX_FLAG_ADDRESS, 1)
        max_checkpoint = int.from_bytes(max_checkpoint_bytes, byteorder='big')

        if (max_checkpoint == 0 and len(ctx.level_state.keys()) > 0 and
                len(ctx.checkpoint_snapshots) > 1):
            print("Detected a restart!")
            ctx.restart = True
            ctx.level_state = {}
            ctx.checkpoint_snapshots = []

        active = []
        new = []
        for i in range(0, total_count):
            addr = CHECKPOINT_FLAGS[i]
            checkpoint_status_bytes = dolphin_memory_engine.read_bytes(addr, 1)
            checkpoint_status = int.from_bytes(checkpoint_status_bytes, byteorder='big') == 1
            if checkpoint_status:
                active.append(i + 1)
        max_active = max(active) if len(active) > 0 else 0
        if max_active != max_checkpoint:
            print("Data not valid")
        else:
            active_snapshots = [x[0] for x in ctx.checkpoint_snapshots]
            for a in active:
                if a not in active_snapshots:
                    new.append(a)
                    ctx.checkpoint_snapshots.append((a, deepcopy(ctx.level_state)))
                    if ctx.checkpoint_sanity:
                        locations = [c.locationId for c in checkpointsanity_locations if c.stageId == current_level and
                                     c.count == a]
                        messages.extend(locations)

    if ctx.key_sanity and current_level in KEY_IDENTIFIER_BY_STAGE:

        key_addresses = GetKeysanityAddresses()
        if "key_index" in ctx.level_state:
            state_key_index = ctx.level_state["key_index"]
            if state_key_index < len(key_addresses):
                current_key_bytes = dolphin_memory_engine.read_bytes(key_addresses[state_key_index], 4)
                current_key_data = int.from_bytes(current_key_bytes, byteorder='big')
                if current_key_data != 0xFFFFFFFF:
                    ctx.level_state["key_index"] = state_key_index + 1

                    key_options = KEY_IDENTIFIER_BY_STAGE[current_level]
                    if current_key_data in key_options:
                        key_index = key_options.index(current_key_data)
                        key_locations = [k for k in keysanity_locations if k.stageId == current_level and k.count == key_index]
                        if len(key_locations) == 0:
                            print("Unable to find location associated")
                        messages.extend([k.locationId for k in key_locations])
                    else:
                        logger.error("Unknown key object:", current_level, key_options, current_key_data)
                        key_locations = [k for k in keysanity_locations if k.stageId == current_level and k.count == state_key_index]
                        messages.extend([k.locationId for k in key_locations])






    # If an objective is currently completable then check for pause state, etc


    button_menu_address = 0x8056ED4F
    is_back_button = 0x20

    if ctx.objective_sanity:
        if dark_max_hit and current_alignment == MISSION_ALIGNMENT_DARK or \
            hero_max_hit and current_alignment == MISSION_ALIGNMENT_HERO:
            current_paused_data = dolphin_memory_engine.read_bytes(is_paused_address, 1)
            currently_paused = int.from_bytes(current_paused_data, byteorder='big') == 1

            button_data = dolphin_memory_engine.read_bytes(button_menu_address, 1)
            button_data_byte = int.from_bytes(button_data, byteorder='big')
            if currently_paused and button_data_byte == is_back_button:
                if current_alignment == MISSION_ALIGNMENT_DARK:
                    ctx.level_state["dark_completable"] = COMPLETE_FLAG_READY
                    #new_messages = complete_completable_levels(ctx, current_level, current_alignment)
                    #messages.extend(new_messages)
                elif current_alignment == MISSION_ALIGNMENT_HERO:
                    ctx.level_state["hero_completable"] = COMPLETE_FLAG_READY
                    #new_messages = complete_completable_levels(ctx, current_level, current_alignment)
                    #messages.extend(new_messages)


    if len(messages) > 0:
        #ctx.locations_checked = messages
        message = [{"cmd": 'LocationChecks', "locations": messages}]
        await ctx.send_msgs(message)



async def check_death(ctx: ShTHContext):

    LIVES_ADDRESS = 0x80576704
    lives_bytes = dolphin_memory_engine.read_bytes(LIVES_ADDRESS, 4)
    life_count = int.from_bytes(lives_bytes, byteorder='big')

    if life_count > ctx.lives:
        ctx.lives = life_count
    elif life_count < ctx.lives:
        ctx.lives = life_count
        print("Detected a death!")
        current_rings_bytes = dolphin_memory_engine.read_bytes(RINGS_ADDRESS, 4)
        print(current_rings_bytes)
        return True

    return False




async def dolphin_sync_task(ctx: ShTHContext):
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        death = False
        try:
            if ctx.slot is not None:
                pass
            else:
                #if not ctx.auth:
                #    # ctx.auth = read_string(SLOT_NAME_ADDR, 0x40)
                if ctx.awaiting_rom:
                    await ctx.server_auth()

            if dolphin_memory_engine.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if ctx.awaiting_server:
                    await asyncio.sleep(1)
                    continue

                if not await check_save_loaded(ctx):
                    # Reset give item array while not in game.
                    #writeBytes(GIVE_ITEM_ARRAY_ADDR, bytes([0xFF] * ctx.len_give_item_array))
                    await asyncio.sleep(0.1)
                    continue

                if True:
                    death = await check_death(ctx)
                    level = await check_level_status(ctx)
                    if level is not None:
                        await update_level_behaviour(ctx,level, death)
                    else:
                        ctx.lives = 0

                    await handle_ring_link(ctx, level, death)


                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    # Hook and check the game?!
                    game_id_bytes = dolphin_memory_engine.read_bytes(0x80000000, 6)
                    if game_id_bytes not in valid_game_bytes:
                        logger.info(CONNECTION_REFUSED_GAME_STATUS.format(str(game_id_bytes)))
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dolphin_memory_engine.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        #ctx.locations_checked = set()
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dolphin_memory_engine.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect(True)
            await asyncio.sleep(5)
            continue


def main(connect=None, password=None):
    Utils.init_logging("Shadow The Hedgehog Client")

    async def _main(connect, password):
        ctx = ShTHContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)

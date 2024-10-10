import asyncio
import time
import traceback
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import dolphin_memory_engine

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem
from worlds.shadow_the_hedgehog import Levels, Items, Locations
from worlds.shadow_the_hedgehog.Levels import *
from worlds.shadow_the_hedgehog.Locations import GetStageInformation, GetAlignmentsForStage

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a ROM for Shadow The Hedgehog. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure Shadow The Hedgehog is running."
)

CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."


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
    address: int
    addressSize: int
    searchIndex: int | None
    totalSearchIndex: int | None

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

def GetStageUnlockAddresses():
    unlock_addresses = {}

    for stage in Levels.ALL_STAGES:
        unlock_addresses[stage] = (westopolis_save_info_base_address +
                                                   (SAVE_STRUCTURE_DETAILS.Size * Levels.ALL_STAGES.index(stage)))

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



ADDRESS_ALIEN_COUNT = 0x8057FB54
ADDRESS_ALIEN_COUNT_BUT = 0x8057FB55
ADDRESS_SOLIDER_COUNT = 0x8057FB4C

#ADDRESS_SEARCH_STANDARD = 0x8052B74C
ADDRESS_MISSION_HERO_POINTER = 0x80575F04
ADDRESS_MISSION_DARK_POINTER = 0x805F0E44


ADDRESS_LAST_STORY_OPTION = 0x80578020
ADDRESS_WEAPONS_BYTES = 0x80578068
ADDRESS_LAST_CUTSCENE = 0x805EF2A0
ADDRESS_EXPERT_MODE_UNLOCK = 0x80578021


DEFAULT_SEARCH_INDEX = (16 * 6) + 8
SECONDARY_SEARCH_INDEX = (16 * 16) + 8
CC_HERO_INDEX = (30 * 16) + 4
PI_TD_HERO_INDEX = (16 * 6) + 4
DEFAULT_TOTAL_INDEX_HERO = (16 * 5) + 4
DEFAULT_TOTAL_INDEX = (16 * 5) + 8


StageAlignmentAddresses = [
    StageAlignmentAddress(STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_SOLIDER_COUNT, 4, searchIndex=None,
                          totalSearchIndex=DEFAULT_TOTAL_INDEX),
    StageAlignmentAddress(STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_ALIEN_COUNT, 4, searchIndex=None,
                          totalSearchIndex=DEFAULT_TOTAL_INDEX_HERO),

    StageAlignmentAddress(STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_MISSION_DARK_POINTER, 4,
                          searchIndex=DEFAULT_SEARCH_INDEX,totalSearchIndex=None),
    StageAlignmentAddress(STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_ALIEN_COUNT, 4,
                          searchIndex=None, totalSearchIndex=DEFAULT_TOTAL_INDEX),

    StageAlignmentAddress(STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_MISSION_HERO_POINTER, 4,
                          searchIndex=DEFAULT_SEARCH_INDEX,totalSearchIndex=None),
    StageAlignmentAddress(STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_MISSION_DARK_POINTER, 4,
                          searchIndex=DEFAULT_SEARCH_INDEX,totalSearchIndex=None),

    StageAlignmentAddress(STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_SOLIDER_COUNT, 4,
                          searchIndex=None,totalSearchIndex=DEFAULT_TOTAL_INDEX),
    StageAlignmentAddress(STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_MISSION_HERO_POINTER, 4,
                          searchIndex=PI_TD_HERO_INDEX,totalSearchIndex=None),

    StageAlignmentAddress(STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_SOLIDER_COUNT, 4,
                          searchIndex=None,totalSearchIndex=DEFAULT_TOTAL_INDEX),

    StageAlignmentAddress(STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_MISSION_DARK_POINTER, 4,
                          searchIndex=DEFAULT_SEARCH_INDEX,totalSearchIndex=None),
    StageAlignmentAddress(STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_MISSION_HERO_POINTER, 4,
                          searchIndex=CC_HERO_INDEX,totalSearchIndex=None),

    StageAlignmentAddress(STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_SOLIDER_COUNT, 4,
                          searchIndex=None,totalSearchIndex=DEFAULT_TOTAL_INDEX),
    StageAlignmentAddress(STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_MISSION_HERO_POINTER, 4,
                          searchIndex=PI_TD_HERO_INDEX,totalSearchIndex=None),

    StageAlignmentAddress(STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_MISSION_DARK_POINTER, 4,
                          searchIndex=DEFAULT_SEARCH_INDEX,totalSearchIndex=None),
    StageAlignmentAddress(STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_MISSION_HERO_POINTER, 4,
                          searchIndex=SECONDARY_SEARCH_INDEX,totalSearchIndex=None),

    StageAlignmentAddress(STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_MISSION_DARK_POINTER, 4,
                          searchIndex=DEFAULT_SEARCH_INDEX,totalSearchIndex=None),
    StageAlignmentAddress(STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_MISSION_HERO_POINTER, 4,
                          searchIndex=DEFAULT_SEARCH_INDEX,totalSearchIndex=None),

    StageAlignmentAddress(STAGE_DEATH_RUINS, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_ALIEN_COUNT_BUT, 4,
                          searchIndex=None,totalSearchIndex=DEFAULT_TOTAL_INDEX),

    StageAlignmentAddress(STAGE_THE_ARK, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_MISSION_DARK_POINTER, 4,
                          searchIndex=DEFAULT_SEARCH_INDEX,totalSearchIndex=None),

    StageAlignmentAddress(STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_ALIEN_COUNT, 4,
                          searchIndex=None,totalSearchIndex=DEFAULT_TOTAL_INDEX),

    StageAlignmentAddress(STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_SOLIDER_COUNT, 4,
                          searchIndex=None,totalSearchIndex=DEFAULT_TOTAL_INDEX),

    StageAlignmentAddress(STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_MISSION_DARK_POINTER, 4,
                          searchIndex=DEFAULT_SEARCH_INDEX,totalSearchIndex=None),

    StageAlignmentAddress(STAGE_LOST_IMPACT, Levels.MISSION_ALIGNMENT_HERO, ADDRESS_ALIEN_COUNT_BUT, 4,
                          searchIndex=None,totalSearchIndex=DEFAULT_TOTAL_INDEX),

    StageAlignmentAddress(STAGE_GUN_FORTRESS, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_MISSION_DARK_POINTER, 4,
                          searchIndex=DEFAULT_SEARCH_INDEX,totalSearchIndex=None),

    StageAlignmentAddress(STAGE_BLACK_COMET, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_SOLIDER_COUNT, 4,
                          searchIndex=None,totalSearchIndex=DEFAULT_TOTAL_INDEX),

    StageAlignmentAddress(STAGE_LAVA_SHELTER, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_MISSION_DARK_POINTER, 4,
                          searchIndex=DEFAULT_SEARCH_INDEX,totalSearchIndex=None),

    StageAlignmentAddress(STAGE_FINAL_HAUNT, Levels.MISSION_ALIGNMENT_DARK, ADDRESS_MISSION_DARK_POINTER, 4,
                          searchIndex=DEFAULT_SEARCH_INDEX,totalSearchIndex=None)
]

@dataclass
class CharacterAddress:
    name: str
    met_address: int

CharacterAddresses = [
    CharacterAddress("Sonic", 0x8057D77B),
    CharacterAddress("Knuckles", 0x8057D77F),
    CharacterAddress("Tails", 0x8057D783),
    CharacterAddress("Amy", 0x8057D787),
    CharacterAddress("Maria", 0x8057D79B),
    CharacterAddress("Eggman", 0x8057D7A3),
    CharacterAddress("Rouge", 0x8057D78B),
    CharacterAddress("Omega", 0x8057D78F),
    CharacterAddress("Doom", 0x8057D7A7),
    CharacterAddress("Espio", 0x8057D797),
    CharacterAddress("Charmy", 0x8057D79F),
    CharacterAddress("Vector", 0x8057D793),
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
        self.emeralds = []
        self.characters_met = []

        # Name of the current stage as read from the game's memory. Sent to trackers whenever its value changes to
        # facilitate automatically switching to the map of the current stage.
        self.current_stage_name: str = ""

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        self.salvage_locations_map = {}
        self.current_stage_name = ""
        self.visited_stage_names = None
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
        r = await self.send_connect()


    def on_package(self, cmd: str, args: dict):
        print("on_package", cmd, args)
        if cmd == "Connected":
            slot_data = args["slot_data"]
            self.available_levels.extend(slot_data["first_levels"])

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
    mission_clear_locations, mission_locations, end_location = Locations.GetAllLocationInfo()

    # TODO: Check for newly obtained instead of all

    if loaded:
        pass

        per_stage = {}
        cleared_missions = []

        messages = []
        for stage_clear_address in GetStageClearAddresses().items():
            stage, alignment = stage_clear_address[0]
            clear_address = stage_clear_address[1]

            current_bytes = dolphin_memory_engine.read_bytes(clear_address, 1)
            current_status = int.from_bytes(current_bytes, byteorder='big')

            if current_status == 1:
                cleared_missions.append((stage,alignment))
                if stage not in per_stage:
                    per_stage[stage] = []
                per_stage[stage].append(alignment)

                clear_location = [m for m in mission_clear_locations if m.stageId == stage
                                  and m.alignmentId == alignment]
                if len(clear_location) == 1:
                    messages.append(clear_location[0].locationId)

        # decide settings for goal

        set_last_way = False
        #if len(per_stage) == len(ALL_STAGES):
        # Unlock THE LAST WAY
        #    set_last_way = 1
        #

        if len(ctx.emeralds) == 7:
            set_last_way = True

        if set_last_way:
            set_to = 1
            set_last_way_bytes = set_to.to_bytes(1, byteorder='big')
            dolphin_memory_engine.write_bytes(ADDRESS_LAST_STORY_OPTION, set_last_way_bytes)

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
            ctx.locations_checked = messages
            message = [{"cmd": 'LocationChecks', "locations": messages}]
            await ctx.send_msgs(message)

        if finished:
            ctx.finished_game = True
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL,
            }])

        # Check for mission completes






    return loaded

# When not in a level, check the level
def check_level_status(ctx):

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

    remove = []
    for ix in i:
        ctx.handled.append(ix)
        remove.append(ix)

    for r in remove:
        ctx.items_to_handle.remove(r)

    # Set working address to set accessibility to levels
    # This data should save when the game is saved
    # Consider locking levels the player does not have access to

    #if 100 not in ctx.available_levels:
    #    ctx.available_levels.append(100)

    # TODO: Make it so you aren't checking/writing this constantly
    for level in LEVEL_ID_TO_LEVEL.keys():
        if level in ctx.available_levels:
            new_count = 1
        else:
            new_count = 0

        address = GetStageUnlockAddresses()[level]
        new_bytes = new_count.to_bytes(4, byteorder='big')
        dolphin_memory_engine.write_bytes(address, new_bytes)

    emeraldItems = Items.GetItemLookupDict()

    # TODO: Distinctness

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


    ADDRESS_IN_LEVEL = 0x8057D74A
    ADDRESS_CURRENT_LEVEL = 0x80584722

    ADDRESS_LOADING_MAYBE = 0x80570B26

    if True:
        in_level = dolphin_memory_engine.read_byte(ADDRESS_IN_LEVEL)
        if in_level == 255:
            # Reset the level state when not in a level
            ctx.level_state = {}

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


async def update_level_behaviour(ctx, current_level):
    # based on the level
    # work out which addresses to use for checks for each mission objective
    # handle picked up keys as they picked up
    # handle enemy counters if checks are enabled
    # Set initial value (to level of value from server)
    # If higher than previous value, recognise as check and reduce by 1

    ADDRESS_MISSION_ALIGNMENT = 0x80575F1F


    # Add handle for first load of level, when state is blank

    info = Items.GetItemLookupDict()
    mission_clear_locations, mission_locations, end_location = Locations.GetAllLocationInfo()

    handle_count = 0

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

        i = [unlock for unlock in ctx.handled if unlock[0].item in info and \
             info[unlock[0].item].stageId == current_level and info[unlock[0].item].type == "level_object"]

        group_by_alignment = {}
        for ix in i:
            item = info[ix[0].item]
            if item.alignmentId not in group_by_alignment:
                group_by_alignment[item.alignmentId] = []
            group_by_alignment[item.alignmentId].append(item)

        if ctx.level_state["hero_active"]:
            if Levels.MISSION_ALIGNMENT_HERO in group_by_alignment:
                hero_count = len(group_by_alignment[Levels.MISSION_ALIGNMENT_HERO])
                handle_count += 1
            else:
                hero_count = 0

            ctx.level_state["hero_count"] = hero_count

        if ctx.level_state["dark_active"]:
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
        if info[ix[0].item].alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            ctx.level_state["dark_count"] += 1
        elif info[ix[0].item].alignmentId == Levels.MISSION_ALIGNMENT_HERO:
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
    hero_address_size = None

    dark_address = None
    dark_address_size = None

    hero_max_hit = False
    dark_max_hit = False

    hero_addr_original = False
    if hero_address_data is not None:
        hero_address = hero_address_data.address
        if hero_address == ADDRESS_ALIEN_COUNT_BUT:
            hero_address -= 1
            hero_addr_original = True
        hero_address_size = hero_address_data.addressSize

    if dark_address_data is not None:
        dark_address = dark_address_data.address
        dark_address_size = dark_address_data.addressSize

    if hero_address_data is not None and hero_address_data.searchIndex is not None:
        current_pointer = dolphin_memory_engine.read_bytes(hero_address, hero_address_size)
        mission_requirement_count = int.from_bytes(current_pointer, byteorder="big") + hero_address_data.searchIndex
        hero_address = mission_requirement_count

    if dark_address_data is not None and dark_address_data.searchIndex is not None:
        current_pointer = dolphin_memory_engine.read_bytes(dark_address, dark_address_size)
        mission_requirement_count = int.from_bytes(current_pointer, byteorder="big") + dark_address_data.searchIndex
        dark_address = mission_requirement_count

    stageInfo = GetStageInformation(current_level)
    heroInfo = None
    stageInfoHero = [ s for s in stageInfo if s.alignmentId == Levels.MISSION_ALIGNMENT_HERO ]
    if len(stageInfoHero) > 0 and hero_address is not None:
        heroInfo = stageInfoHero[0]

    stageInfoDark = [s for s in stageInfo if s.alignmentId == Levels.MISSION_ALIGNMENT_DARK]
    darkInfo = None
    if len(stageInfoDark) > 0 and dark_address is not None:
        darkInfo = stageInfoDark[0]

    if heroInfo is not None:
        hero_count = ctx.level_state["hero_count"]
        max = heroInfo.requirement_count
        hero_write = hero_count

        hero_completable = ctx.level_state["hero_completable"]
        if hero_completable == COMPLETE_FLAG_OFF:
            set_max_up = True
            hero_count_max = heroInfo.requirement_count + 2
            ctx.level_state["hero_completable"] = COMPLETE_FLAG_OFF_SET
        elif hero_completable == COMPLETE_FLAG_READY:
            set_max_up = True
            hero_count_max = heroInfo.requirement_count
            ctx.level_state["hero_completable"] = COMPLETE_FLAG_ON_SET
            handle_count = True
        else:
            set_max_up = False
            hero_count_max = 255

        if hero_count == max:
            hero_max_hit = True

        if set_max_up:
            if hero_address == ADDRESS_ALIEN_COUNT:
                to_use = ADDRESS_MISSION_HERO_POINTER
                if hero_addr_original:
                    to_use = ADDRESS_MISSION_DARK_POINTER
                current_pointer = dolphin_memory_engine.read_bytes(to_use, hero_address_size)
                mission_requirement_count = (int.from_bytes(current_pointer, byteorder="big") +
                                             hero_address_data.totalSearchIndex)
                hero_total_address = mission_requirement_count
            else:
                hero_total_address = hero_address - 16

            new_count = hero_count_max
            new_bytes = new_count.to_bytes(hero_address_size, byteorder='big')
            dolphin_memory_engine.write_bytes(hero_total_address, new_bytes)

        if handle_count > 0:
            new_count = hero_write
            new_bytes = new_count.to_bytes(hero_address_size, byteorder='big')
            dolphin_memory_engine.write_bytes(hero_address, new_bytes)

    if darkInfo is not None:
        dark_count = ctx.level_state["dark_count"]
        dark_write = dark_count
        max = darkInfo.requirement_count
        dark_completable = ctx.level_state["dark_completable"]
        if dark_completable == COMPLETE_FLAG_OFF:
            set_max_up = True
            dark_count_max = darkInfo.requirement_count + 2
            ctx.level_state["dark_completable"] = COMPLETE_FLAG_OFF_SET
        elif dark_completable == COMPLETE_FLAG_READY:
            set_max_up = True
            dark_count_max = darkInfo.requirement_count
            ctx.level_state["dark_completable"] = COMPLETE_FLAG_ON_SET
            handle_count = True
        else:
            set_max_up = False
            dark_count_max = 255

        if dark_count == max:
            dark_max_hit = True

        if set_max_up:
            if dark_address == ADDRESS_SOLIDER_COUNT:
                current_pointer = dolphin_memory_engine.read_bytes(ADDRESS_MISSION_DARK_POINTER, dark_address_size)
                mission_requirement_count = (int.from_bytes(current_pointer, byteorder="big") +
                                             dark_address_data.totalSearchIndex)
                dark_total_address = mission_requirement_count
            else:
                dark_total_address = dark_address - 16

            new_count = dark_count_max
            new_bytes = new_count.to_bytes(dark_address_size, byteorder='big')
            dolphin_memory_engine.write_bytes(dark_total_address, new_bytes)

        if handle_count > 0:
            new_count = dark_write
            new_bytes = new_count.to_bytes(dark_address_size, byteorder='big')
            dolphin_memory_engine.write_bytes(dark_address, new_bytes)

    ## Handle new events

    expected_hero_value = hero_write
    expected_dark_value = dark_write

    hero_progress = False
    dark_progress = False

    if hero_address is not None:
        current_bytes = dolphin_memory_engine.read_bytes(hero_address, hero_address_size)
        current_count = int.from_bytes(current_bytes, byteorder='big')

        if current_count > expected_hero_value:
            print("hero count increased --", current_count, expected_hero_value)
            if current_count > heroInfo.requirement_count + 2:
                print("invalid value read for hero count:", current_count)
            ctx.level_state["hero_progress"] += (current_count - expected_hero_value)
            hero_progress = True
        elif expected_hero_value > current_count >= 0:
            ctx.level_state["hero_progress"] = current_count

        if hero_address is not None and hero_write is not None:
            new_count = expected_hero_value
            new_bytes = new_count.to_bytes(4, byteorder='big')
            dolphin_memory_engine.write_bytes(hero_address, new_bytes)

    if dark_address is not None:
        current_bytes = dolphin_memory_engine.read_bytes(dark_address, dark_address_size)
        current_count = int.from_bytes(current_bytes, byteorder='big')

        if current_count > expected_dark_value:
            print("dark count increased --", current_count, expected_dark_value)
            if current_count > darkInfo.requirement_count + 2:
                print("invalid value read for dark count", current_count)
            else:
                ctx.level_state["dark_progress"] += (current_count - expected_dark_value)
                dark_progress = True
        elif expected_dark_value > current_count >= 0:
            ctx.level_state["dark_progress"] = current_count

        if dark_address is not None and dark_write is not None:
            new_count = expected_dark_value
            new_bytes = new_count.to_bytes(4, byteorder='big')
            dolphin_memory_engine.write_bytes(dark_address, new_bytes)

    messages = []
    if hero_progress or dark_progress:
        # TODO: Check which check we are up to for hero and dark
        # Send only unchecked locations
        # Need state to be restorable maybe


        # Signal archipelago a check has been made
        if hero_progress:
            progress_locations = [ l.locationId for l in mission_locations if l.alignmentId == Levels.MISSION_ALIGNMENT_HERO and \
                l.stageId == current_level and l.count <= ctx.level_state["hero_progress"] ]
            messages.extend(progress_locations)

        if dark_progress:
            progress_locations = [ l.locationId for l in mission_locations if l.alignmentId == Levels.MISSION_ALIGNMENT_DARK and \
                l.stageId == current_level and l.count <= ctx.level_state["dark_progress"] ]
            messages.extend(progress_locations)

        if len(messages) > 0:
            ctx.locations_checked = messages
            message = [{"cmd": 'LocationChecks', "locations": messages}]
            await ctx.send_msgs(message)

        pass

    # If an objective is currently completable then check for pause state, etc

    is_paused_address = 0x805EE1DC
    button_menu_address = 0x8056ED4F
    is_back_button = 0x20

    if dark_max_hit and current_alignment == MISSION_ALIGNMENT_DARK or \
        hero_max_hit and current_alignment == MISSION_ALIGNMENT_HERO:
        current_paused_data = dolphin_memory_engine.read_bytes(is_paused_address, 1)
        currently_paused = int.from_bytes(current_paused_data, byteorder='big') == 1

        button_data = dolphin_memory_engine.read_bytes(button_menu_address, 1)
        button_data_byte = int.from_bytes(button_data, byteorder='big')
        if currently_paused and button_data_byte == is_back_button:
            if current_alignment == MISSION_ALIGNMENT_DARK:
                ctx.level_state["dark_completable"] = COMPLETE_FLAG_READY
            elif current_alignment == MISSION_ALIGNMENT_HERO:
                ctx.level_state["hero_completable"] = COMPLETE_FLAG_READY


    # TODO: Use existing character locations received
    # To determine if characters are met
    # If charactersanity is disabled, just set all every time a new level is entered

    character_sanity = False

    if character_sanity:
        # Implement checks for memory addresses to see if set
        # Send locations when this happens
        # Use the known locations done to set list of characters
        pass
    else:
        if len(ctx.characters_met) == 0:
            ctx.characters_met.extend(
                [c.name for c in CharacterAddresses]
            )

    pass

    if not ctx.level_state["characters_set"]:
        for character in ctx.characters_met:
            relevantCharData = [ c for c in CharacterAddresses if c.name == character ]
            if len(relevantCharData) != 0:
                relevantChar = relevantCharData[0]
                new_value = 1
                new_bytes = new_value.to_bytes(1, byteorder='big')
                dolphin_memory_engine.write_bytes(relevantChar.met_address, new_bytes)

        ctx.level_state["characters_set"] = True



async def dolphin_sync_task(ctx: ShTHContext):
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if ctx.slot is not None:
                if "DeathLink" in ctx.tags:
                    pass
                    # await check_death(ctx)
                # await give_items(ctx)
                # await check_locations(ctx)
                # await check_current_stage_changed(ctx)
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
                    #dolphin_memory_engine.write_bytes(GIVE_ITEM_ARRAY_ADDR, bytes([0xFF] * ctx.len_give_item_array))
                    await asyncio.sleep(0.1)
                    continue

                if True:
                    level = check_level_status(ctx)
                    if level is not None:
                        await update_level_behaviour(ctx,level)


                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    # Hook and check the game?!
                    if dolphin_memory_engine.read_bytes(0x80000000, 6) != bytes(Levels.SHADOW_THE_HEDGEHOG_GAME_ID, "utf-8"):
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dolphin_memory_engine.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
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
            await ctx.disconnect()
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

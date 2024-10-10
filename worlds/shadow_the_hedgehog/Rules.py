from BaseClasses import MultiWorld
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from worlds.shadow_the_hedgehog import Items, Levels
from worlds.shadow_the_hedgehog.Items import ShadowTheHedgehogItem, GetStageUnlockItem
from worlds.shadow_the_hedgehog.Locations import MissionClearLocations


def set_rules(multiworld: MultiWorld, world: World, player: int):

    for clear in MissionClearLocations:

        if clear.requirement_count == 1:
            continue
        id, name = Levels.GetLevelCompletionNames(clear.stageId, clear.alignmentId)
        try:
            location = multiworld.get_location(name, player)
            item_name = Items.GetStageAlignmentObject(clear.stageId, clear.alignmentId)
            add_rule(location, lambda state, itemname=item_name, count=clear.requirement_count:
            state.has(itemname, player, count=count))
        except KeyError:
            # Do nothing for mission locations that do not exist
            pass

    e = multiworld.get_entrance("final-story-unlock", player)
    emeralds = Items.GetEmeraldItems()
    e.access_rule = lambda state: state.has(emeralds[0].name, player) and state.has(emeralds[1].name, player) \
            and state.has(emeralds[2].name, player) and state.has(emeralds[3].name, player) \
            and state.has(emeralds[4].name, player) and state.has(emeralds[5].name, player) \
            and state.has(emeralds[6].name, player)

    final_item = Items.GetFinalItem()
    mw_final_item = ShadowTheHedgehogItem(final_item, world.player)
    multiworld.get_location(Levels.DevilDoom_Name, world.player).place_locked_item(
        mw_final_item)

    multiworld.completion_condition[player] = lambda state: state.has(Items.Progression.GoodbyeForever, player)

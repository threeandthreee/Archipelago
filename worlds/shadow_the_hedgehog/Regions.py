import typing
from typing import Dict

from BaseClasses import Region, Entrance, MultiWorld
from . import Levels, Items, Weapons, Story, GetLevelCompletionNames, Locations, Options
from .Options import LevelProgression
from .Story import PathInfo


def stage_id_to_region(level_id: int, region_id = 0) -> str:
    level_name = Levels.LEVEL_ID_TO_LEVEL[level_id]
    region_name = "REGION_" + level_name + "_" + str(region_id)
    return region_name

def stage_id_to_story_region(level_id: int, region_id = 0) -> str:
    level_name = Levels.LEVEL_ID_TO_LEVEL[level_id]
    region_name = "STORY_REGION_" + level_name + "_" + str(region_id)
    return region_name

def get_max_stage_region_id(level_id: int, key: bool = True) -> str:
    level_name = Levels.LEVEL_ID_TO_LEVEL[level_id]
    region_ids = [ r.regionIndex for r in Levels.INDIVIDUAL_LEVEL_REGIONS if r.stageId == level_id and
                   (True if key else r.restrictionType != Levels.REGION_RESTRICTION_TYPES.KeyDoor) ]
    region_id = 0 if len(region_ids) == 0 else max(region_ids)
    region_name = "REGION_" + level_name + "_" + str(region_id)
    return region_name

def character_name_to_region(name):
    return "REGION_" + name

def weapon_name_to_region(name):
    return "REGION_" + name

def region_name_for_character(stage_name, name):
    return name + "_in_" + stage_name

def region_name_for_weapon(stage_name, name):
    return name + "_in_" + stage_name


def early_region_checks(world):

    # needto iterate in story order, not default order
    available_story_stages = []

    story_sorted_stages = Story.StoryToOrder(world.shuffled_story_mode)

    last_way_required = not world.options.include_last_way_shuffle or world.options.level_progression == Options.LevelProgression.option_select

    if last_way_required:
        story_sorted_stages.append(Levels.STAGE_THE_LAST_WAY)

    # TODO: Add handling for story NOT having all stages, in future

    for level in story_sorted_stages:
        if Levels.LEVEL_ID_TO_LEVEL[level] in world.options.excluded_stages and \
            (level != Levels.STAGE_THE_LAST_WAY or not last_way_required):
            continue

        if world.options.level_progression != Options.LevelProgression.option_select:
            story_routes_to_stage = [ s for s in world.shuffled_story_mode if
                                      s.end_stage_id == level
                                      and
                                      ((s.start_stage_id is None) or
                                      ( GetLevelCompletionNames(s.start_stage_id,
                                      s.alignment_id)[1] not in
                                      world.options.exclude_locations) and
                                       Levels.LEVEL_ID_TO_LEVEL[s.start_stage_id] not in world.options.excluded_stages)
                                      ]
            if len(story_routes_to_stage) > 0:
                available_story_stages.append(level)
                world.available_levels.append(level)
                for story_route in story_routes_to_stage:
                    if story_route.boss is not None and story_route.boss not in available_story_stages\
                            and story_route.start_stage_id in world.available_levels:
                        world.available_levels.append(story_route.boss)
                        break

            stage_as_boss = [ s for s in world.shuffled_story_mode if s.boss == level and
                              s.start_stage_id in world.available_levels and level not in available_story_stages]
            if len(stage_as_boss) > 0:
                world.available_levels.append(level)

        if (world.options.level_progression != Options.LevelProgression.option_story \
                and ( level not in Levels.BOSS_STAGES or world.options.select_bosses )
                #and level not in Levels.FINAL_BOSSES
                and level != Levels.BOSS_DEVIL_DOOM
                #and level not in Levels.LAST_STORY_STAGES # Until resolved
                and (Story.GetVanillaBossStage(level) is None or level in Levels.FINAL_BOSSES
                     or Levels.LEVEL_ID_TO_LEVEL[Story.GetVanillaBossStage(level)] not in world.options.excluded_stages)
                and not (level in Levels.LAST_STORY_STAGES and not world.options.include_last_way_shuffle)
                and level not in world.available_levels):
            world.available_levels.append(level)

        if level == Levels.STAGE_THE_LAST_WAY and last_way_required:
            world.available_levels.append(level)


    for char_name in Levels.CharacterToLevel.keys():
        levels_in = Levels.CharacterToLevel[char_name]
        levels_in = [ (l[0] if type(l) is tuple else l) for l in levels_in  ]
        levels_left = [ l for l in levels_in if l in world.available_levels ]
        if len(levels_left) == 0:
            continue

        world.available_characters.append(char_name)

    for weapon in Weapons.WEAPON_INFO:
        levels_in = weapon.available_stages
        levels_in = [ (l[0] if type(l) is tuple else l) for l in levels_in  ]
        levels_left = [ l for l in levels_in if l in world.available_levels ]
        if len(levels_left) == 0:
            continue

        world.available_weapons.append(weapon.name)

def create_regions(world) -> Dict[str, Region]:
    regions: Dict[str, Region] = {}
    stages = Levels.ALL_STAGES

    stage_regions = []
    region_to_stage_id = {}
    possible_first_regions = []

    last_way_standard = (world.options.level_progression == Options.LevelProgression.option_select
                         or not world.options.include_last_way_shuffle or not world.options.story_shuffle == Options.StoryShuffle.option_chaos)


    limited_first_stages = []
    if world.options.guaranteed_level_clear:
        limited_first_stages = Locations.GetStagesWithNoRequirements(world)



    for level_id in stages:
        if level_id not in world.available_levels:
            print("Level not available:", Levels.LEVEL_ID_TO_LEVEL[level_id])
            continue
        base_region_name = stage_id_to_region(level_id, 0)
        new_region = Region(base_region_name, world.player, world.multiworld)
        regions[base_region_name] = new_region
        stage_regions.append(new_region)
        if level_id not in Levels.BOSS_STAGES and level_id not in Levels.LAST_STORY_STAGES:
            if len(limited_first_stages) == 0 or level_id in limited_first_stages:
                possible_first_regions.append(new_region)
        region_to_stage_id[new_region] = level_id

        for additional_region in [ r for r in Levels.INDIVIDUAL_LEVEL_REGIONS if r.stageId == level_id]:
            new_region_name = stage_id_to_region(level_id, additional_region.regionIndex)
            new_additional_region = Region(new_region_name, world.player, world.multiworld)
            regions[new_region_name] = new_additional_region

        if world.options.level_progression != LevelProgression.option_select:
            story_region_name = stage_id_to_story_region(level_id)
            new_story_region = Region(story_region_name, world.player, world.multiworld)
            regions[story_region_name] = new_story_region
            #stage_regions.append(new_story_region)

            connect(world.player, "stage-access:"+Levels.LEVEL_ID_TO_LEVEL[level_id],
                    new_story_region, new_region)

    if world.options.level_progression != Options.LevelProgression.option_story:
        first_regions = world.random.sample(possible_first_regions, world.options.starting_stages.value)
        world.first_regions = [ region_to_stage_id[region] for region in first_regions]

    if world.options.level_progression != Options.LevelProgression.option_select:
        stage_ids = [ start.end_stage_id for start in world.shuffled_story_mode if start.start_stage_id is None ]
        world.first_regions.extend(stage_ids)
        pass

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    #for region in first_regions:
    #    regions["Menu"].connect(regions[region.name], "Start Game "+region.name)

    if world.options.level_progression != LevelProgression.option_story:
        for region in stage_regions:
            #if region not in first_regions:
            stage_id = region_to_stage_id[region]

            connect_name = "menu-to-stage-"+str(stage_id)
            stage_item_name = Items.GetStageUnlockItem(stage_id)
            boss_item_name = None
            boss_stage_requirement = None

            if stage_id in Levels.LAST_STORY_STAGES:
                continue
            if stage_id in Levels.BOSS_STAGES:
                if stage_id not in Levels.LAST_STORY_STAGES and stage_id not in Levels.FINAL_BOSSES:
                    boss_stage_requirement = Story.GetVanillaBossStage(stage_id)
                    if boss_stage_requirement is not None:
                        boss_item_name = Items.GetStageUnlockItem(boss_stage_requirement)

            connect_rule = None
            if boss_item_name is None:
                connect_rule = lambda state, si=stage_item_name: state.has(si, world.player)
            elif boss_stage_requirement is not None and world.options.level_progression == LevelProgression.option_both:

                # check if available via story
                # check if available via select

                possible_via_select = True
                possible_via_story = True

                vanilla_boss_stage = Story.GetVanillaBossStage(stage_id)

                if vanilla_boss_stage is not None and vanilla_boss_stage not in world.available_levels:
                    possible_via_select = False

                if len([ s for s in world.shuffled_story_mode if s == stage_id ]) == 0:
                    possible_via_story = False

                if possible_via_story and possible_via_select:
                    connect_rule = lambda state, si=stage_item_name, b_name=boss_item_name, b_stage=boss_stage_requirement: (
                            state.has(si, world.player) and
                            (state.has(b_name, world.player)
                             or
                             state.can_reach_region(stage_id_to_story_region(b_stage),world.player))
                             )
                elif possible_via_select:
                    connect_rule = lambda state, si=stage_item_name, b_name=boss_item_name: (
                            state.has(si, world.player) and
                            state.has(b_name, world.player)
                    )
                    # Nothing to do, this is select logic
                    pass
                elif possible_via_story:
                    # Don't add route to stage via select!
                    pass

            else:
                connect_rule = lambda state, si=stage_item_name, b_name=boss_item_name: (
                        state.has(si, world.player) and state.has(b_name, world.player)
                )

            if connect_rule is not None:
                connect(world.player, connect_name,
                        regions["Menu"], region, connect_rule)

    for char_name in Levels.CharacterToLevel.keys():
        levels_in = Levels.CharacterToLevel[char_name]
        levels_in = [ (l[0] if type(l) is tuple else l) for l in levels_in  ]
        levels_left = [ l for l in levels_in if l in world.available_levels ]
        if len(levels_left) == 0:
            continue

        region_name = character_name_to_region(char_name)
        new_region = Region(region_name, world.player, world.multiworld)
        regions[region_name] = new_region
        world.available_characters.append(char_name)

    for weapon in Weapons.WEAPON_INFO:
        levels_in = weapon.available_stages
        levels_in = [ (l[0] if type(l) is tuple else l) for l in levels_in  ]
        levels_left = [ l for l in levels_in if l in world.available_levels ]
        if len(levels_left) == 0:
            continue

        region_name = weapon_name_to_region(weapon.name)
        new_region = Region(region_name, world.player, world.multiworld)
        regions[region_name] = new_region
        world.available_weapons.append(weapon.name)

    regions["FinalStory"] = Region("FinalStory", world.player, world.multiworld)
    connect(world.player, "final-story-unlock", regions["Menu"],
            regions["FinalStory"])

    regions["DevilDoom"] = Region("DevilDoom", world.player, world.multiworld)
    connect(world.player, "devil-doom-fight", regions["FinalStory"],
            regions["DevilDoom"])

    if last_way_standard:
        last_way_region = regions[stage_id_to_region(Levels.STAGE_THE_LAST_WAY)]
        connect(world.player, "final-story-unlock-tlw", regions["FinalStory"],
                last_way_region)

        pass



    return regions

def connect_by_story_mode(multiworld: MultiWorld, world, player: int, order: typing.List[PathInfo]):
    for path in order:
        if path.start_stage_id is None:
            start_region = world.get_region("Menu")
            end_region_name = stage_id_to_story_region(path.end_stage_id)
            end_region = world.get_region(end_region_name)

            secret_rule = None
            #if world.options.secret_story_progression and hasattr(multiworld, "re_gen_passthrough"):
            #    warp_item = Items.GetStageWarpItem(path.end_stage_id)
            #    secret_rule = lambda state, wi=warp_item: state.has(wi, world.player)

            connect(world.player, "Base Story Entrance_" + str(order.index(path)) + str(path.start_stage_id) + "/" +
                    str(path.end_stage_id), start_region, end_region, rule=secret_rule)
            continue

        # Boss handling before here, because we need to hande bosses

        boss_region = None
        boss_rule = None
        boss_base_region = None

        if (path.start_stage_id not in world.available_levels or
                (path.end_stage_id is not None and path.end_stage_id not in world.available_levels)):
            continue

        start_base_region_name = stage_id_to_story_region(path.start_stage_id)
        start_region = world.get_region(start_base_region_name)

        if path.boss is not None:
            if path.boss in world.available_levels:
                boss_base_region_name = stage_id_to_region(path.boss)
                boss_base_region = world.get_region(boss_base_region_name)

                boss_region_name = stage_id_to_story_region(path.boss)
                boss_region = world.get_region(boss_region_name)

                boss_item = [ b for b in Locations.BossClearLocations if b.stageId == path.boss][0]
                boss_id, boss_name = Locations.GetBossLocationName(boss_item.name, boss_item.stageId)
                boss_rule = lambda state,nn=boss_name: state.can_reach_location(nn, player)

        if path.end_stage_id is None:
            if boss_region is not None and boss_rule is not None:
                boss_completion_location_id, boss_completion_location_name = GetLevelCompletionNames(path.start_stage_id,
                                                                                           path.alignment_id)
                bf_rule = lambda state, bn=boss_completion_location_name: state.can_reach_location(bn, player)

                if world.options.secret_story_progression and hasattr(multiworld, "re_gen_passthrough"):
                    warp_item = Items.GetStageWarpItem(path.boss)
                    secret_rule = lambda state, wi=warp_item: state.has(wi, world.player)
                    bf_rule = lambda state, br=bf_rule, sr=secret_rule: br(state) and sr(state)

                boss_end_entrance = connect(world.player, "Boss Entrance_" + str(path.start_stage_id) + "/" +
                    str(path.end_stage_id) + "/" + str(path.alignment_id), start_region, boss_region,
                                        rule=bf_rule)

                multiworld.register_indirect_condition(start_region, boss_end_entrance)
                base_region_name = stage_id_to_region(path.start_stage_id)
                base_story_region_name = stage_id_to_story_region(path.start_stage_id)
                base_region = world.get_region(base_region_name)
                base_story_region = world.get_region(base_story_region_name)
                multiworld.register_indirect_condition(base_region, boss_end_entrance)
                multiworld.register_indirect_condition(base_story_region, boss_end_entrance)

                extra_level_regions = [l for l in Levels.INDIVIDUAL_LEVEL_REGIONS if l.stageId == path.start_stage_id]

                for region in extra_level_regions:
                    level_region_name = stage_id_to_region(region.stageId, region.regionIndex)
                    region_to_add = world.get_region(level_region_name)
                    if boss_end_entrance is not None:
                        multiworld.register_indirect_condition(region_to_add, boss_end_entrance)


            continue

        # If mission clear location is in excluded locations, ban this route
        completion_location_id, completion_location_name = GetLevelCompletionNames(path.start_stage_id,
                                                                                   path.alignment_id)

        if completion_location_name in world.options.exclude_locations:
            print("Unable to take story path due to excluded location:", path.start_stage_id, path.alignment_id)
            continue

        #end_region_base_name = stage_id_to_region(path.end_stage_id)
        #end_base_region = world.get_region(end_region_base_name)
        end_region_name = stage_id_to_story_region(path.end_stage_id)
        end_region = world.get_region(end_region_name)

        # get all regions associated to the stage and register as indirect
        # Because the condition can lead to complications due to breadth-first search

        extra_level_regions = [ l for l in Levels.INDIVIDUAL_LEVEL_REGIONS if l.stageId == path.start_stage_id ]

        base_rule = lambda state,n=completion_location_name: state.can_reach_location(n, player)

        boss_base_rule = base_rule
        if world.options.secret_story_progression and hasattr(multiworld, "re_gen_passthrough"):
            warp_item = Items.GetStageWarpItem(path.end_stage_id)
            secret_rule = lambda state, wi=warp_item: state.has(wi, world.player)
            base_rule = lambda state, br=base_rule, sr=secret_rule: br(state) and sr(state)

        boss_entrance = None
        if boss_region is not None:

            if world.options.secret_story_progression and hasattr(multiworld, "re_gen_passthrough"):
                warp_item = Items.GetStageWarpItem(path.boss)
                secret_rule = lambda state, wi=warp_item: state.has(wi, world.player)
                boss_base_rule = lambda state, br=boss_base_rule, sr=secret_rule: br(state) and sr(state)

            boss_entrance = connect(world.player, "Boss Entrance_"+str(order.index(path)) + str(path.start_stage_id) + "/" +
                    str(path.end_stage_id), start_region, boss_region, rule=boss_base_rule)
            multiworld.register_indirect_condition(start_region, boss_entrance)
            base_region_name = stage_id_to_region(path.start_stage_id)
            #base_story_region_name = stage_id_to_story_region(path.start_stage_id)
            base_region = world.get_region(base_region_name)
            #base_story_region = world.get_region(base_story_region_name)
            multiworld.register_indirect_condition(base_region, boss_entrance)
            #multiworld.register_indirect_condition(base_story_region, boss_entrance)
            #multiworld.register_indirect_condition(end_region, boss_entrance)
            #multiworld.register_indirect_condition(end_base_region, boss_entrance)
            #multiworld.register_indirect_condition(boss_region, boss_entrance)

        if boss_rule is not None:
            modified_rule = lambda state, r_rule=base_rule, b_rule=boss_rule: (r_rule(state) and b_rule(state))
        else:
            modified_rule = base_rule

        new_entrance = connect(world.player, "Story Entrance_"+str(path.start_stage_id) + "/" +
                    str(path.end_stage_id)+"/"+str(path.alignment_id), start_region, end_region, rule=modified_rule)

        for region in extra_level_regions:
            level_region_name = stage_id_to_region(region.stageId, region.regionIndex)
            region_to_add = world.get_region(level_region_name)
            multiworld.register_indirect_condition(region_to_add, new_entrance)
            if boss_entrance is not None:
                multiworld.register_indirect_condition(region_to_add, boss_entrance)
                #multiworld.register_indirect_condition(boss_region, new_entrance)
                multiworld.register_indirect_condition(boss_base_region, new_entrance)


def connect(player: int, name: str,
            source_region: Region, target_region: Region,
            rule: typing.Optional[typing.Callable] = None):

    connection = Entrance(player, name, source_region)

    if rule is not None:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)

    return connection
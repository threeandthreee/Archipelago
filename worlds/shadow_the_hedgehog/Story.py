import copy
import random
from dataclasses import dataclass

from Options import OptionError
from . import Levels, Options, Locations


@dataclass
class PathInfo:
    start_stage_id: int
    alignment_id: int
    end_stage_id: int
    cutscenes: []
    boss = None

    def __init__(self, o_id, alignment, n_id, cutscenes):
        self.start_stage_id = o_id
        self.alignment_id = alignment
        self.end_stage_id = n_id
        self.cutscenes = cutscenes
        self.boss = None

    def via_boss(self, boss):
        self.boss = boss
        return self

    def __str__(self):
        start = "START" if self.start_stage_id is None else Levels.LEVEL_ID_TO_LEVEL[self.start_stage_id]
        end = "END" if self.end_stage_id is None else Levels.LEVEL_ID_TO_LEVEL[self.end_stage_id]
        alignment = Levels.ALIGNMENT_TO_STRING[self.alignment_id] if self.alignment_id is not None else ""
        boss = "" if self.boss is None else " via " + Levels.LEVEL_ID_TO_LEVEL[self.boss]

        return f"{start} {alignment}{boss}>{end}\n"

def GetVanillaBossStage(boss):
    stages = [ b.start_stage_id for b in DefaultStoryMode if b.boss == boss]
    if len(stages) > 0:
        return stages[0]

    return None

def SortByAvailableLength(item):
    return len(item[1])

def ChoosePathOption(world, story_options):
    balancing_value = world.options.story_progression_balancing

    sorted_options = sorted(story_options, key=SortByAvailableLength)

    balance_index = (len(sorted_options) - 1) / 100 * balancing_value
    chosen_index = round(balance_index)

    weights = []
    for i in range(0, len(story_options)):
        weights.append(1000 / pow((abs(chosen_index-i) + 1), 2))

    randomised_item = random.choices(story_options, k=1, weights=weights)[0]
    #print(story_options.index(randomised_item), weights, chosen_index)

    # If 100: always the last item in the list
    # If 1, always the first item in the list

    return randomised_item


def TraversePath(story, available_stages, available_missions):
    clear_locations = Locations.MissionClearLocations

    unhandled_progression = [[s for s in story if s.start_stage_id == c.stageId and s.alignment_id == c.alignmentId][0].end_stage_id
                             for c in clear_locations if c in available_missions and
                             [s for s in story if s.start_stage_id == c.stageId and s.alignment_id == c.alignmentId][
                                 0].end_stage_id not in available_stages
                             ]

    unhandled_progression = [ u for u in unhandled_progression if u is not None]

    available_stages.extend(unhandled_progression)

    first = True
    new_available_without_objectivesanity = []
    while first or len(new_available_without_objectivesanity) != 0:
        first = False

        available_without_objectivesanity = [c for c in clear_locations if c.stageId in available_stages
                                             and c.requirement_count is None]

        new_available_without_objectivesanity = [a for a in available_without_objectivesanity if
                                                 a not in available_missions]


        for mission_clear in new_available_without_objectivesanity:
            story_element = [c for c in story if c.start_stage_id == mission_clear.stageId
                             and c.alignment_id == mission_clear.alignmentId][0]

            if story_element.end_stage_id is not None and story_element.end_stage_id not in available_stages:
                available_stages.append(story_element.end_stage_id)

            available_missions.append(mission_clear)

class StoryAssignmentObject:
    start_stage_id: int
    alignmentId: int
    end_start_id: int
    mission_id: int


def DecideStoryPath(world, story):
    clear_locations = Locations.MissionClearLocations
    starting_stage = [ s for s in story if s.start_stage_id is None]

    stage = starting_stage[0]

    stage_count = len([ x for x in Levels.ALL_STAGES if x not in Levels.BOSS_STAGES and
                        Levels.LEVEL_ID_TO_LEVEL[x] not in world.options.excluded_stages])

    available_stages = [stage.end_stage_id]
    available_missions = []
    TraversePath(story, available_stages, available_missions)

    # Add sphere 0
    sphere_results = [(None, available_stages, available_missions)]

    while len(available_stages) < stage_count:
        objectivesanity_missions = [ s for s in clear_locations if s.stageId in available_stages and s not in available_missions ]

        options = []
        for option in objectivesanity_missions:
            option_available_stages = available_stages.copy()
            option_available_missions = available_missions.copy()
            option_available_missions.append(option)

            TraversePath(story, option_available_stages, option_available_missions)
            if len(option_available_stages) > len(available_stages):
                options.append((option, option_available_stages, option_available_missions))

        choice = ChoosePathOption(world, options)
        chosen_option = choice[0]
        available_stages = choice[1]
        available_missions = choice[2]

        sphere_results.append(choice)

    return sphere_results


def AlterOverridesForStoryPath(spheres, current_overrides):

    first_sphere_size = len(spheres[0][1])
    new_sphere_size = first_sphere_size

    intended_percentage = {
        0: 1,
        1: 2,
        2: 3,
        3: 4,
        4: 5,
        5: 10,
        6: 12,
        7: 15,
        8: 15,
        9: 20,
        10: 25,
        11: 30,
        12: 35,
        13: 40,
        14: 50,
        15: 60,
        16: 75,
        17: 80,
        18: 85,
        19: 90,
        20: 95,
        21: 98,
        22: 99,
        23: 100
    }


    new_overrides = {}

    for sphere in spheres:
        if sphere == spheres[0]:
            continue

        sphere_mission = sphere[0]
        sphere_key = ("C"+
                      ("D" if sphere_mission.alignmentId == Levels.MISSION_ALIGNMENT_DARK else
                       "H")+"."+
                      Levels.LEVEL_ID_TO_LEVEL[sphere_mission.stageId])

        sphere_key_a = ("A" +
                      ("D" if sphere_mission.alignmentId == Levels.MISSION_ALIGNMENT_DARK else
                       "H") + "." +
                      Levels.LEVEL_ID_TO_LEVEL[sphere_mission.stageId])

        percent_value = intended_percentage[new_sphere_size]
        new_sphere_size = len(sphere[1])

        new_overrides[sphere_key] = percent_value

        if sphere_key_a in current_overrides and current_overrides[sphere_key_a] < percent_value:
            current_overrides[sphere_key_a] = percent_value


    return new_overrides




def StoryToOrder(StoryMode):

    ordered_data = []
    set_data = set()

    starting_stages = [ s.end_stage_id for s in StoryMode if s.start_stage_id is None ]
    set_data = set_data.union(set(starting_stages))
    ordered_data.extend(list(set_data))

    while True:
        story_nodes = [ s for s in StoryMode if s.start_stage_id in set_data]
        if len(story_nodes) == 0:
            break
        b_len = len(set_data)
        set_data = set_data.union(set([s.end_stage_id for s in story_nodes if s.end_stage_id is not None and s.end_stage_id not in set_data]))
        set_data = set_data.union(set([s.boss for s in story_nodes if s.boss not in set_data and s.boss is not None and s.boss not in set_data]))
        if b_len == len(set_data):
            break
        else:
            missing = [ x for x in set_data if x not in ordered_data]
            ordered_data.extend(missing)

    return ordered_data


def ChaosShuffle(world):

    ModifiedStoryMode = copy.deepcopy(DefaultStoryMode)

    include_last_way = world.options.include_last_way_shuffle

    stages_to_assign = [ l for l in Levels.ALL_STAGES if Levels.LEVEL_ID_TO_LEVEL[l] not in world.options.excluded_stages and l
                         not in Levels.BOSS_STAGES and l not in Levels.LAST_STORY_STAGES ]
                         #and l != Levels.STAGE_WESTOPOLIS]

    possible_stages = stages_to_assign.copy()

    final_bosses_full = [boss.boss for boss in ModifiedStoryMode if boss.end_stage_id is None and
                         Levels.LEVEL_ID_TO_LEVEL[boss.boss] not in world.options.excluded_stages]
    final_bosses = final_bosses_full.copy()

    boss_groups = Levels.BOSS_GROUPING
    if world.options.single_egg_dealer:
        options = [ b for b in final_bosses if b in boss_groups["Egg Dealer"]]
        if len(options) > 0:
            for o in options:
                final_bosses.remove(o)
            chosen = world.random.choice(options)
            final_bosses.append(chosen)

    if world.options.single_black_doom:
        options = [b for b in final_bosses if b in boss_groups["Black Doom"]]
        if len(options) > 0:
            for o in options:
                final_bosses.remove(o)

            chosen = world.random.choice(options)
            final_bosses.append(chosen)

    if world.options.single_diablon:
        options = [b for b in final_bosses if b in boss_groups["Diablon"]]
        if len(options) > 0:
            for o in options:
                final_bosses.remove(o)

            chosen = world.random.choice(options)
            final_bosses.append(chosen)


    # Removes the duplicate Lava Shelter Egg Dealer
    final_bosses = list(set(final_bosses))

    world.random.shuffle(final_bosses)

    story_boss_stages = [ l for l in Levels.BOSS_STAGES if Levels.LEVEL_ID_TO_LEVEL[l] not in world.options.excluded_stages
                          and l not in Levels.LAST_STORY_STAGES
                          and l not in final_bosses_full ]

    last_way_active = Levels.LEVEL_ID_TO_LEVEL[Levels.STAGE_THE_LAST_WAY] not in world.options.excluded_stages

    if include_last_way:
        if last_way_active:
            stages_to_assign.append(Levels.STAGE_THE_LAST_WAY)

        final_bosses.append(Levels.BOSS_DEVIL_DOOM)

    if len(stages_to_assign) == 0:
        raise OptionError("No stages to assign!")

    random.shuffle(stages_to_assign)

    bosses_to_assign = []
    boss_set = story_boss_stages
    for i in range(0, world.options.story_boss_count):
        bosses_to_assign.extend(boss_set)

    random.shuffle(bosses_to_assign)
    random.shuffle(final_bosses)

    # Potentially duplicate some bosses for more clarity

    #steps_to_randomise = [ s for s in ModifiedStoryMode if s.start_stage_id is not None ]
    steps_to_randomise = [s for s in ModifiedStoryMode if s.start_stage_id is not None
                          and Levels.LEVEL_ID_TO_LEVEL[s.start_stage_id] not in world.options.excluded_stages]

    if include_last_way and last_way_active:
        steps_to_randomise.append(PathInfo(Levels.STAGE_THE_LAST_WAY, Levels.MISSION_ALIGNMENT_NEUTRAL, None, []))

    #untouched_steps = [ s for s in ModifiedStoryMode if s not in steps_to_randomise ]

    new_story = []
    #new_story.extend(untouched_steps)

    bosses_by_alignment = {}

    random.shuffle(steps_to_randomise)

    steps_to_randomise.insert(0, PathInfo(None, None, None, []))

    SafeStartingStages = Locations.GetStagesWithNoRequirements(world)

    new_steps = []
    stage_nodes = []
    first_stage = None

    force_path = None #[0, Levels.MISSION_ALIGNMENT_HERO, Levels.BOSS_DEVIL_DOOM]

    while len(steps_to_randomise) > 0:
        step = None
        boss_possible = False
        first_step = [ step for step in steps_to_randomise if step.start_stage_id is None ]
        if len(first_step) == 1:
            step = first_step[0]
        else:
            valid_steps = [ s for s in steps_to_randomise if s.start_stage_id in stage_nodes ]
            if len(valid_steps) == len(steps_to_randomise):
                boss_possible = True
            if len(valid_steps) > 0:
                step = world.random.choice(valid_steps)

            #step = steps_to_randomise[0]

        if step is None:
            raise Exception("Unable to work out next step to take!")

        if force_path is not None and step.start_stage_id == force_path[0] and \
            step.alignment_id == force_path[1]:
            if force_path[2] in Levels.BOSS_STAGES and not boss_possible:
                continue
            else:
                if force_path[2] in Levels.BOSS_STAGES and (
                        force_path[2] in final_bosses_full or force_path[2] == Levels.BOSS_DEVIL_DOOM):
                    step.end_stage_id = None
                    step.boss = force_path[2]
                    pass

        elif boss_possible and len(final_bosses) > 0 and step.start_stage_id is not None:
            step.end_stage_id = None
            step.boss = final_bosses.pop()
        else:
            boss_assigned = False
            if boss_possible and len(bosses_to_assign) > 0 and step.start_stage_id is not None:
                possible_boss = random.choice(bosses_to_assign)

                if possible_boss not in bosses_by_alignment:
                    bosses_by_alignment[possible_boss] = []

                if step.alignment_id not in bosses_by_alignment[possible_boss]:
                    step.boss = possible_boss
                    bosses_by_alignment[possible_boss].append(step.alignment_id)
                    bosses_to_assign.remove(step.boss)
                    boss_assigned = True

            if not boss_assigned:
                step.boss = None

            if world.options.guaranteed_level_clear and step.start_stage_id is None and len(SafeStartingStages) > 0:
                step.end_stage_id = random.choice(SafeStartingStages)
                stages_to_assign.remove(step.end_stage_id)
                first_stage = step.end_stage_id
                if force_path is not None and force_path[0] == 0:
                    force_path[0] = first_stage
            elif len(stages_to_assign) > 0:
                step.end_stage_id = stages_to_assign.pop()
                if step.end_stage_id == step.start_stage_id and len(stages_to_assign) != 0:
                    stages_to_assign.append(step.end_stage_id)
            else:
                step.end_stage_id = random.choice(possible_stages)

        steps_to_randomise.remove(step)
        new_steps.append(step)
        if step.end_stage_id not in stage_nodes:
            stage_nodes.append(step.end_stage_id)

    new_story.extend(new_steps)

    return new_story




def ShuffleStoryMode(world):
    ModifiedStoryMode = copy.deepcopy(DefaultStoryMode)
    story_stages = []
    for step in ModifiedStoryMode:
        if step.end_stage_id is not None and step.end_stage_id not in story_stages and \
                Levels.LEVEL_ID_TO_LEVEL[step.end_stage_id] not in world.options.excluded_stages:
            if step.end_stage_id == Levels.STAGE_WESTOPOLIS:
                continue
            story_stages.append(step.end_stage_id)

    story_base = story_stages.copy()
    random.shuffle(story_stages)

    for step in ModifiedStoryMode:
        if step.end_stage_id in story_base:
            index = story_base.index(step.end_stage_id)
            new_stage = story_stages[index]
            step.end_stage_id = new_stage

    return ModifiedStoryMode



def GenerateStoryMode(world):
    ModifiedStoryMode = copy.deepcopy(DefaultStoryMode)
    ModifiedStoryMode[0].end_stage_id = world.random.choice(
        [s for s in Levels.ALL_STAGES if s not in Levels.BOSS_STAGES and s not in Levels.LAST_STORY_STAGES
         and s not in Levels.FINAL_STAGES and Levels.LEVEL_ID_TO_LEVEL[s] not in world.options.excluded_stages])
    return ModifiedStoryMode

def GetStoryMode(world):
    #if world.options.story_shuffle == Options.StoryShuffle.option_basic:
    #    return GenerateStoryMode(world)
    #elif world.options.story_shuffle == Options.StoryShuffle.option_shuffle:
    #    return ShuffleStoryMode(world)
    if world.options.story_shuffle == Options.StoryShuffle.option_chaos:
        return ChaosShuffle(world)
    else:
        return DefaultStoryMode


def StoryToString(Story):
    string = ""
    for item in Story:
        start_id = item.start_stage_id
        end_id = item.end_stage_id
        alignment = item.alignment_id
        boss = item.boss
        cutscenes = item.cutscenes
        cutscene_count = len(cutscenes)

        if start_id is None:
            start_id = -1

        if end_id is None:
            end_id = -1

        if boss is None:
            boss = -1

        if alignment is None:
            alignment = -1

        cutscene_string = "" if cutscene_count == 0 else "&".join([str(c) for c in cutscenes])

        string += f"{start_id}&{end_id}&{alignment}&{boss}&{cutscene_count}{cutscene_string}/"

    return string

def StringToStory(string):
    story = []
    items = string.split("/")
    for item in items:
        if len(item) == 0:
            continue
        split = item.split("&")
        start_id = int(split[0])
        end_id = int(split[1])
        alignment = int(split[2])
        boss = int(split[3])
        cutscene_count = int(split[4])

        if start_id == -1:
            start_id = None

        if end_id == -1:
            end_id = None

        if alignment == -1:
            alignment = None

        if boss == -1:
            boss = None

        step = PathInfo(start_id, alignment, end_id, [])

        if cutscene_count > 0:
            cutscenes = [ int(x) for x in split[5].split(",")]
            step.cutscenes = cutscenes

        if boss is not None:
            step.boss = boss

        story.append(step)

    return story



DefaultStoryMode = \
[
    PathInfo(None, None, Levels.STAGE_WESTOPOLIS, []),

    PathInfo(Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_DIGITAL_CIRCUIT, []),
    PathInfo(Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_GLYPHIC_CANYON, []),
    PathInfo(Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LETHAL_HIGHWAY, [])
    ,
    PathInfo(Levels.STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_CRYPTIC_CASTLE, []),
    PathInfo(Levels.STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_PRISON_ISLAND, []),

    PathInfo(Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_CRYPTIC_CASTLE, []),
    PathInfo(Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_PRISON_ISLAND, []),
    PathInfo(Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_CIRCUS_PARK, []),

    PathInfo(Levels.STAGE_LETHAL_HIGHWAY, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_PRISON_ISLAND, [])
        .via_boss(Levels.BOSS_BLACK_BULL_LH),
    PathInfo(Levels.STAGE_LETHAL_HIGHWAY, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_CIRCUS_PARK, [])
        .via_boss(Levels.BOSS_BLACK_BULL_LH),

    PathInfo(Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_CENTRAL_CITY, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_CC),
    PathInfo(Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_THE_DOOM, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_CC),
    PathInfo(Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_SKY_TROOPS, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_CC),

    PathInfo(Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_THE_DOOM, []),
    PathInfo(Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_SKY_TROOPS, []),
    PathInfo(Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_MAD_MATRIX, []),

    PathInfo(Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_SKY_TROOPS, []),
    PathInfo(Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_MAD_MATRIX, []),
    PathInfo(Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_DEATH_RUINS, []),

    PathInfo(Levels.STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_THE_ARK, []),
    PathInfo(Levels.STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_AIR_FLEET, []),

    PathInfo(Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_THE_ARK, [])
        .via_boss(Levels.BOSS_HEAVY_DOG),
    PathInfo(Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_AIR_FLEET, [])
        .via_boss(Levels.BOSS_HEAVY_DOG),
    PathInfo(Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_IRON_JUNGLE, [])
        .via_boss(Levels.BOSS_HEAVY_DOG),

    PathInfo(Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_AIR_FLEET, []),
    PathInfo(Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_IRON_JUNGLE, []),
    PathInfo(Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_SPACE_GADGET, []),

    PathInfo(Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_IRON_JUNGLE, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_MM),
    PathInfo(Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_SPACE_GADGET, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_MM),
    PathInfo(Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LOST_IMPACT, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_MM),

    PathInfo(Levels.STAGE_DEATH_RUINS, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_SPACE_GADGET, [])
        .via_boss(Levels.BOSS_BLACK_BULL_DR),
    PathInfo(Levels.STAGE_DEATH_RUINS, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LOST_IMPACT, [])
        .via_boss(Levels.BOSS_BLACK_BULL_DR),

    PathInfo(Levels.STAGE_THE_ARK, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_GUN_FORTRESS, [])
        .via_boss(Levels.BOSS_BLUE_FALCON),
    PathInfo(Levels.STAGE_THE_ARK, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_BLACK_COMET, [])
        .via_boss(Levels.BOSS_BLUE_FALCON),

    PathInfo(Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_GUN_FORTRESS, []),
    PathInfo(Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_BLACK_COMET, []),
    PathInfo(Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_LAVA_SHELTER, []),

    PathInfo(Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_BLACK_COMET, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_IJ),
    PathInfo(Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_LAVA_SHELTER, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_IJ),
    PathInfo(Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_COSMIC_FALL, [])
        .via_boss(Levels.BOSS_EGG_BREAKER_IJ),

    PathInfo(Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_DARK, Levels.STAGE_LAVA_SHELTER, []),
    PathInfo(Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_COSMIC_FALL, []),
    PathInfo(Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_FINAL_HAUNT, []),

    PathInfo(Levels.STAGE_LOST_IMPACT, Levels.MISSION_ALIGNMENT_NEUTRAL, Levels.STAGE_COSMIC_FALL, []),
    PathInfo(Levels.STAGE_LOST_IMPACT, Levels.MISSION_ALIGNMENT_HERO, Levels.STAGE_FINAL_HAUNT, []),

    PathInfo(Levels.STAGE_GUN_FORTRESS, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_DIABLON_GF),
    PathInfo(Levels.STAGE_GUN_FORTRESS, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_BLACK_DOOM_GF),

    PathInfo(Levels.STAGE_BLACK_COMET, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_DIABLON_BC),
    PathInfo(Levels.STAGE_BLACK_COMET, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_BC),

    PathInfo(Levels.STAGE_LAVA_SHELTER, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_LS),
    PathInfo(Levels.STAGE_LAVA_SHELTER, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_LS),

    PathInfo(Levels.STAGE_COSMIC_FALL, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_EGG_DEALER_CF),
    PathInfo(Levels.STAGE_COSMIC_FALL, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_BLACK_DOOM_CF),

    PathInfo(Levels.STAGE_FINAL_HAUNT, Levels.MISSION_ALIGNMENT_DARK, None, [])
        .via_boss(Levels.BOSS_DIABLON_FH),
    PathInfo(Levels.STAGE_FINAL_HAUNT, Levels.MISSION_ALIGNMENT_HERO, None, [])
        .via_boss(Levels.BOSS_BLACK_DOOM_FH),

]

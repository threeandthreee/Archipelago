import logging
import typing
from math import ceil, floor

from BaseClasses import MultiWorld, Region, Entrance, Item, ItemClassification
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from . import Items, Levels, Utils, Weapons, Regions, Vehicle, Options, Locations,Names, Objects
    
#LEVEL_ID_TO_LEVEL, CharacterToLevel, Items.ITEM_TOKEN_TYPE_FINAL, \    Levels.MISSION_ALIGNMENT_DARK, Levels.MISSION_ALIGNMENT_HERO, Items.ITEM_TOKEN_TYPE_OBJECTIVE
#Items.ITEM_TOKEN_TYPE_STANDARD, Items.ITEM_TOKEN_TYPE_ALIGNMENT,GetLevelObjectNamesItems.ITEM_TOKEN_TYPE_BOSSItems.ITEM_TOKEN_TYPE_FINAL_BOSSLevels.REGION_RESTRICTION_REFERENCE_TYPES
#Names.REGION_RESTRICTION_TYPESGetEnemyLocationNameLevelRegion

from .Items import ShadowTheHedgehogItem, GetLevelTokenItems
from .Locations import MissionClearLocations, LocationInfo, BossClearLocations
from .Options import LevelProgression
from .Regions import character_name_to_region, stage_id_to_region, region_name_for_character, weapon_name_to_region, \
    region_name_for_weapon
from . import Utils as ShadowUtils

def GetKeyRule(stage, player):
    relevant_key_base = [ k for k in Locations.KeyLocations if k.stageId == stage]
    key_regions = relevant_key_base[0].region
    regions = set([ Names.GetDistributionRegionEventName(stage, k) for k in key_regions])
    return lambda state, ri=regions: state.has_all(ri, player)

def GetRelevantTokenItem(token: LocationInfo):
    level_token_items = GetLevelTokenItems()

    if token.other == Items.ITEM_TOKEN_TYPE_FINAL:
        level_token_items = [ t for t in level_token_items if t.value == Items.ITEM_TOKEN_TYPE_FINAL ]
    elif token.other == Items.ITEM_TOKEN_TYPE_OBJECTIVE:
        level_token_items = [ t for t in level_token_items if t.value == Items.ITEM_TOKEN_TYPE_OBJECTIVE ]
    elif token.other == Items.ITEM_TOKEN_TYPE_STANDARD:
        level_token_items = [t for t in level_token_items if t.value == Items.ITEM_TOKEN_TYPE_STANDARD]
    elif token.other == Items.ITEM_TOKEN_TYPE_ALIGNMENT:
        level_token_items = [t for t in level_token_items if t.value == Items.ITEM_TOKEN_TYPE_ALIGNMENT]
        if token.alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            level_token_items = [ t for t in level_token_items if t.alignmentId == Levels.MISSION_ALIGNMENT_DARK]
        elif token.alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            level_token_items = [ t for t in level_token_items if t.alignmentId == Levels.MISSION_ALIGNMENT_HERO]
    elif token.other == Items.ITEM_TOKEN_TYPE_BOSS:
        level_token_items = [t for t in level_token_items if t.value == Items.ITEM_TOKEN_TYPE_BOSS]
    elif token.other == Items.ITEM_TOKEN_TYPE_FINAL_BOSS:
        level_token_items = [t for t in level_token_items if t.value == Items.ITEM_TOKEN_TYPE_FINAL_BOSS]

    if len(level_token_items) == 0:
        return None

    return level_token_items[0]

def handle_path_rules(options, player, additional_level_region, path_type):
    rule = lambda state: True

    if additional_level_region.hardLogicOnly:
        if options.logic_level != Options.LogicLevel.option_hard:
            print("Path denied", additional_level_region)
            rule = lambda state: False
            return rule

    if not Levels.IsLogicLevelApplicable(additional_level_region, options, path_type, options.start_inventory):
        return rule

    if Names.REGION_RESTRICTION_TYPES.Impassable in additional_level_region.restrictionTypes:
        # Temp solution
        final_item = Items.GetFinalItem()
        return lambda state: state.has(final_item.name, player)

    if options.chaos_control_logic_level != Options.ChaosControlLogicLevel.option_off \
        and additional_level_region.chaosControlLogicRequiresHeal:

        weapon_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.HEAL,
                                                         additional_level_region.stageId,
                                                         additional_level_region.fromRegions)

        if additional_level_region.chaosControlLogicType == Options.ChaosControlLogicLevel.option_intermediate and \
                options.chaos_control_logic_level not in \
                [Options.ChaosControlLogicLevel.option_off, Options.ChaosControlLogicLevel.option_easy]:

            return weapon_rule

        if additional_level_region.chaosControlLogicType == Options.ChaosControlLogicLevel.option_hard and \
                options.chaos_control_logic_level == Options.ChaosControlLogicLevel.option_hard:

            return weapon_rule

    if Names.REGION_RESTRICTION_TYPES.KeyDoor in additional_level_region.restrictionTypes:
        key_rule = GetKeyRule(additional_level_region.stageId, player)
        rule = lambda state,r=rule: key_rule(state) and r(state)

    if Names.REGION_RESTRICTION_TYPES.ShootOrTurret in additional_level_region.restrictionTypes:
        if options.weapon_sanity_unlock and options.vehicle_logic:
            rule_weapon = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.LONG_RANGE,
                                                      additional_level_region.stageId,
                                                      additional_level_region.fromRegions)

            rule_vehicle = Vehicle.GetRuleByVehicleRequirement(player, "Gun Turret")

            rule_w_or_v = lambda state: (rule_weapon(state) or rule_vehicle(state))
            rule = lambda state, r=rule: rule_w_or_v(state) and r(state)

    if Names.REGION_RESTRICTION_TYPES.Explosion in additional_level_region.restrictionTypes:
        weapon_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.EXPLOSION,
                                                  additional_level_region.stageId, additional_level_region.fromRegions)

        weapon_available = False
        bombs_available = True
        if weapon_rule is not None:
            weapon_available = True

        bomb_rule = lambda state: state.has("Bombs", player)

        if additional_level_region.stageId == Levels.STAGE_DEATH_RUINS:
            bombs_available = False

        explosion_rule = lambda state: True
        if weapon_available and options.weapon_sanity_unlock and \
            (not bombs_available):
            explosion_rule = weapon_rule
        elif bombs_available and weapon_available and options.weapon_sanity_unlock and \
            options.object_unlocks and options.object_units:
            explosion_rule = lambda state, wr=weapon_rule, br=bomb_rule: wr(state) or br(state)
        elif not weapon_available and options.object_unlocks and options.object_units:
            explosion_rule = bomb_rule

        rule = lambda state,r=rule: explosion_rule(state) and r(state)

    elif Names.REGION_RESTRICTION_TYPES.Heal in additional_level_region.restrictionTypes:
        weapon_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.HEAL,
                                                         additional_level_region.stageId,
                                                         additional_level_region.fromRegions)

        weapon_available = False
        units_available = False
        if weapon_rule is not None:
            weapon_available = True

        unit_rule = lambda state: state.has("Heal Units", player)

        if additional_level_region.stageId == Levels.STAGE_THE_DOOM:
            units_available = True

        heal_rule = lambda state: True
        if weapon_available and \
                (not units_available):
            heal_rule = weapon_rule
        elif units_available and weapon_available and \
                options.object_unlocks and options.object_units:
            heal_rule = lambda state, wr=weapon_rule, ur=unit_rule: wr(state) or ur(state)
        elif not weapon_available and options.object_unlocks and options.object_units:
            heal_rule = unit_rule

        rule = lambda state, r=rule: heal_rule(state) and r(state)

    if Names.REGION_RESTRICTION_TYPES.GoldBeetle in additional_level_region.restrictionTypes:
        if options.logic_level == Options.LogicLevel.option_easy:
            gb_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.VACUUM,
                                                      additional_level_region.stageId,
                                                      additional_level_region.fromRegions)

            rule = lambda state, r=rule: gb_rule(state) and r(state)

        elif options.logic_level == Options.LogicLevel.option_normal:
            gb_rule = Weapons.GetRuleByWeaponRequirement(player, None, additional_level_region.stageId, additional_level_region.fromRegions)
            rule = lambda state, r=rule: gb_rule(state) and r(state)

    if options.weapon_sanity_unlock and Levels.IsWeaponsanityRestriction(additional_level_region.restrictionTypes):
        if Names.REGION_RESTRICTION_TYPES.Torch in additional_level_region.restrictionTypes:
            rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.TORCH,
                                                      additional_level_region.stageId, additional_level_region.fromRegions)

        w_rule = lambda state: True
        if Names.REGION_RESTRICTION_TYPES.VacuumOrShot in additional_level_region.restrictionTypes:
            v_or_s_rule = lambda state: True
            ruleA = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.LONG_RANGE,
                                                      additional_level_region.stageId,
                                                      additional_level_region.fromRegions)

            ruleB = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.VACUUM,
                                                      additional_level_region.stageId,
                                                      additional_level_region.fromRegions)

            if ruleA is None and ruleB is None:
                raise Exception("Unhandled issue with VacuumOrShot region")

            elif ruleA is None:
                v_or_s_rule = ruleB

            elif ruleB is None:
                v_or_s_rule = ruleA
            else:
                v_or_s_rule = lambda state, a=ruleA, b=ruleB: a(state) or b(state)

            w_rule = lambda state, w=w_rule: v_or_s_rule(state) and w(state)

        if Names.REGION_RESTRICTION_TYPES.LongRangeGun in additional_level_region.restrictionTypes:
            w_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.LONG_RANGE,
                                                      additional_level_region.stageId, additional_level_region.fromRegions)

        if Names.REGION_RESTRICTION_TYPES.Vacuum in additional_level_region.restrictionTypes:
            w_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.VACUUM,
                                                      additional_level_region.stageId, additional_level_region.fromRegions)

        if Names.REGION_RESTRICTION_TYPES.Gun in additional_level_region.restrictionTypes:
            w_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.SHOT,
                                                      additional_level_region.stageId, additional_level_region.fromRegions)

        if Names.REGION_RESTRICTION_TYPES.AnyStageWeapon in additional_level_region.restrictionTypes:
            w_rule = Weapons.GetRuleByWeaponRequirement(player, None, additional_level_region.stageId, additional_level_region.fromRegions)

        if Names.REGION_RESTRICTION_TYPES.SatelliteGun in additional_level_region.restrictionTypes:
            w_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.LOCKON,
                                                      additional_level_region.stageId,
                                                      additional_level_region.fromRegions)

        rule = lambda state, r=rule: w_rule(state) and r(state)

    if options.vehicle_logic and Names.REGION_RESTRICTION_TYPES.Car in additional_level_region.restrictionTypes:
        c_rule = lambda state: True
        # If used anywhere else, need to change to check accessibility
        ruleCar = Vehicle.GetRuleByVehicleRequirement(player, "Standard Car")
        ruleConv = Vehicle.GetRuleByVehicleRequirement(player, "Convertible")
        c_rule = lambda state, r_car=ruleCar, r_conv=ruleConv: r_car(state) or r_conv(state)

        rule = lambda state, r=rule: c_rule(state) and r(state)


    if options.vehicle_logic and Levels.IsVeichleSanityRestriction(additional_level_region.restrictionTypes):
        v_rule = lambda state: True
        if Names.REGION_RESTRICTION_TYPES.BlackArmsTurret in additional_level_region.restrictionTypes:
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Black Turret")
        if Names.REGION_RESTRICTION_TYPES.BlackVolt in additional_level_region.restrictionTypes:
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Black Volt")
        if Names.REGION_RESTRICTION_TYPES.BlackHawk in additional_level_region.restrictionTypes:
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Black Hawk")
        if Names.REGION_RESTRICTION_TYPES.GunJumper in additional_level_region.restrictionTypes:
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Gun Jumper")
        if Names.REGION_RESTRICTION_TYPES.AirSaucer in additional_level_region.restrictionTypes:
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Air Saucer")
        if Names.REGION_RESTRICTION_TYPES.GunLift in additional_level_region.restrictionTypes:
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Gun Lift")
        if Names.REGION_RESTRICTION_TYPES.GunTurret in additional_level_region.restrictionTypes:
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Gun Turret")

        rule = lambda state, r=rule: v_rule(state) and r(state)

    if Names.REGION_RESTRICTION_TYPES.ShadowRifle in additional_level_region.restrictionTypes:
        sr_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.SHADOW_RIFLE,
                                                         additional_level_region.stageId,
                                                         additional_level_region.fromRegions)

        rule = lambda state, r=rule, r2=sr_rule: r2(state) and r(state)


    if options.object_unlocks and Levels.IsObjectRestriction(additional_level_region.restrictionTypes):
        o_rule = lambda state: True
        if Names.REGION_RESTRICTION_TYPES.Zipwire in additional_level_region.restrictionTypes and options.object_ziplines:
            o_rule = lambda state: state.has("Zipwire", player)
        if Names.REGION_RESTRICTION_TYPES.LightDash in additional_level_region.restrictionTypes  and options.object_light_dashes:
            o_rule = lambda state: state.has("Air Shoes", player)
        if Names.REGION_RESTRICTION_TYPES.WarpHole in additional_level_region.restrictionTypes  and options.object_warp_holes:
            o_rule = lambda state: state.has("Warp Holes", player)
        if Names.REGION_RESTRICTION_TYPES.Rocket in additional_level_region.restrictionTypes  and options.object_rockets:
            o_rule = lambda state: state.has("Rocket", player)
        if Names.REGION_RESTRICTION_TYPES.Pulley in additional_level_region.restrictionTypes  and options.object_pulleys:
            o_rule = lambda state: state.has("Pulley", player)

        rule = lambda state, r=rule: o_rule(state) and r(state)

    for regionAccess in [ a for a in additional_level_region.restrictionTypes if a > 100]:
        required_stage_region = regionAccess - 100
        access_rule = lambda state: state.can_reach_region(
            stage_id_to_region(additional_level_region.stageId, required_stage_region), player)

        rule = lambda state, r=rule: access_rule(state) and r(state)

    return rule

def restrict_objects(multiworld, world, player):
    world_locations = [ l.name for l in world.get_locations()]

    for object in [ x for x in Objects.GetObjectChecks() if x.restrictionType != 10 ]:
        location_id, entry_location_name = Names.GetObjectLocationName(object)
        if entry_location_name in world_locations:
            location_with_restriction = world.get_location(entry_location_name)
            dummy_region = Levels.LevelRegion(object.stage, object.region, [object.restrictionType])
            location_with_restriction.access_rule = handle_path_rules(world.options, player, dummy_region,
                                                                      Levels.REGION_RESTRICTION_REFERENCE_TYPES.BaseLogic)

def lock_warp_items(multiworld, world, player):

    if world.options.level_progression == Options.LevelProgression.option_select or not world.options.secret_story_progression:
        return

    (clear_locations, mission_locations, end_location,
     enemysanity_locations, checkpointsanity_locations, charactersanity_locations,
     token_locations, keysanity_locations, weaponsanity_locations, boss_locations,
     warp_locations, object_locations) = Locations.GetAllLocationInfo()

    warpItemInfos = Items.PopulateLevelWarpPoints()

    for warp in warp_locations:
        if warp.stageId in Levels.LAST_STORY_STAGES and not world.options.include_last_way_shuffle:
            continue

        if warp.stageId in Levels.BOSS_STAGES and world.options.level_progression == Options.LevelProgression.option_select:
            continue

        if warp.stageId not in world.available_story_levels:
            continue

        warp_story_region = Regions.stage_id_to_story_region(warp.stageId)
        location = multiworld.get_location(warp.name, player)
        i = [ w for w in warpItemInfos if w.stageId == warp.stageId][0]
        mw_token_item = ShadowTheHedgehogItem(i, player)
        new_access_rule = lambda state, r=location.access_rule, s=warp_story_region: r(state) and state.can_reach_region(
            s, player)

        location.access_rule = new_access_rule

        location.place_locked_item(
            mw_token_item)

def CountRegionAccessibility(state, keys, data, ix, player, perc=100):
    #sum(

    #    [data[r] for r in GetReachableRegions(state, keys) if r in keys]) >= ix)

    # This method uses events but they show up in spoiler log and look bad so use other method
    # Which uses reachable regions instead of events

    use_event_method = True
    if use_event_method:
        keys = list(keys)

        # Which is better, % of total, or % of each region?

        total = 0
        all = True
        values = []
        have = []
        for key in keys:

            count_in_region = data[key]
            # print("Does player have", key, count_in_region)
            if count_in_region > 0:
                if state.has(key, player):
                    # print("player have", key, count_in_region)
                    values.append(count_in_region)
                    have.append(key)
                else:
                    # print("Doesn't player have", key, count_in_region)
                    all = False

        for i in values:
            if all:
                total += i
            else:
                total += floor(i * (perc / 100))

        if all:
            new_total = floor(total * (perc / 100))
            if new_total == 0 and total > 0:
                total = 1

        return total >= ix
    else:
        keys = list(keys)
        all_regions = [ a.name for a in  state.reachable_regions[player]]
        matching_counts = [ data[r] for r in all_regions if r in keys]
        total_accessible = sum(matching_counts)
        return total_accessible >= ix


def set_rules(multiworld: MultiWorld, world: World, player: int):

    token_assignments = {}

    if world.options.level_progression != LevelProgression.option_select:
        Regions.connect_by_story_mode(multiworld, world, player, world.shuffled_story_mode)

    for stage in Levels.ALL_STAGES:
        if stage in Levels.BOSS_STAGES:
            continue

        if stage not in world.available_levels:
            continue

        view_name = Names.GetDistributionRegionEventName(stage, 0)

        event_location = multiworld.get_location(view_name, player)
        event_location.access_rule = lambda state, r=stage_id_to_region(stage,
                                                                        0): \
            state.can_reach_region(r, player)

        event_location.place_locked_item(Item(view_name,
                                              ItemClassification.progression_skip_balancing, None, player))

    skip_regions = []
    if world.options.logic_level != Options.LogicLevel.option_hard:
        hard_only = [ r for r in Levels.INDIVIDUAL_LEVEL_REGIONS if r.hardLogicOnly]
        skip_regions.extend([ (h.stageId, h.regionIndex) for h in hard_only])

    for additional_level_region in Levels.INDIVIDUAL_LEVEL_REGIONS:
        if additional_level_region.stageId not in world.available_levels:
            continue

        if (additional_level_region.stageId, additional_level_region.regionIndex) in skip_regions:
            continue

        from_regions = additional_level_region.fromRegions
        new_region_name = stage_id_to_region(additional_level_region.stageId, additional_level_region.regionIndex)

        for region_from in from_regions:

            if (additional_level_region.stageId, region_from) in skip_regions:
                continue

            base_region_name = stage_id_to_region(additional_level_region.stageId, region_from)

            base_region = world.get_region(base_region_name)
            new_region = world.get_region(new_region_name)

            path_rule = handle_path_rules(world.options, player, additional_level_region,
                                          Levels.REGION_RESTRICTION_REFERENCE_TYPES.BaseLogic)
            if path_rule is not None:
                connect(world.player, base_region_name+ ">" + "(" + str(additional_level_region.restrictionTypes) + ")" + new_region_name,
                    base_region, new_region, path_rule)
            else:
                print("Path rule is None", base_region_name, new_region_name)

        view_name = Names.GetDistributionRegionEventName(additional_level_region.stageId, additional_level_region.regionIndex)

        event_location = multiworld.get_location(view_name, player)
        event_location.access_rule = lambda state, r=stage_id_to_region(additional_level_region.stageId,
                                                                        additional_level_region.regionIndex): \
            state.can_reach_region(r, player)

        event_location.place_locked_item(Item(view_name,
                                              ItemClassification.progression_skip_balancing, None, player))

            # TODO: Add logic here for obtaining access

    override_settings = world.options.percent_overrides
    lock_warp_items(multiworld, world, world.player)

    restrict_objects(multiworld, world, world.player)

    for clear in MissionClearLocations:

        if clear.stageId not in world.available_levels:
            continue

        id, name = Levels.GetLevelCompletionNames(clear.stageId, clear.alignmentId)
        if True:
            req_rule = lambda state: True
            level_rule = lambda state: True
            rule_change = False

            if clear.requirements is not None:
                for req in clear.requirements:
                    lr = Levels.LevelRegion(clear.stageId, None, req)
                    lr.setLogicType(clear.logicType)

                    logic_type = Levels.REGION_RESTRICTION_REFERENCE_TYPES.BaseLogic

                    req_rule_a = handle_path_rules(world.options, player, lr,
                                                 logic_type)
                    if req_rule_a is not None:
                        req_rule = lambda state, z=req_rule, a=req_rule_a: \
                            z(state) and a(state)
                        level_rule = lambda state, r_rule=req_rule, l_rule=level_rule: (
                                r_rule(state) and l_rule(state))

                        rule_change = True
            if clear.craft_requirements is not None:
                for req in clear.craft_requirements:
                    lr = Levels.LevelRegion(clear.stageId, None, req)
                    lr.setLogicType(clear.logicType)

                    logic_type = Levels.REGION_RESTRICTION_REFERENCE_TYPES.CraftLogic

                    req_rule_b = handle_path_rules(world.options, player, lr,
                                                 logic_type)
                    if req_rule_b is not None:
                        req_rule = lambda state, z=req_rule, b=req_rule_b: \
                            z(state) and b(state)
                        level_rule = lambda state, r_rule=req_rule, l_rule=level_rule: (
                                r_rule(state) and l_rule(state))
                        rule_change = True

            if clear.getDistribution() is not None:

                # This functionality requires access to ALL to complete which is inflating
                # When logically you can find with access to either
                # But this also needs handling for objective-less
                #for region_id in clear.getDistribution().keys():
                #    required_region = Regions.stage_id_to_region(clear.stageId, region_id)
                ##    new_rule = lambda state, r_region=required_region: state.can_reach_region(r_region, player)
                #    level_rule = lambda state, l_rule=level_rule, n_rule=new_rule: n_rule(state) and l_rule(state)
                #    rule_change = True

                if clear.requirement_count is not None and world.options.objective_sanity:

                    max_required = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                                  clear.mission_object_name, world.options,
                                                                  clear.stageId, clear.alignmentId,
                                                                  world.options.percent_overrides),
                        clear.requirement_count, clear.stageId, clear.alignmentId,
                        override_settings)

                    frequency_required = ShadowUtils.getMaxRequired(
                        ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_FREQUENCY,
                                                                  clear.mission_object_name, world.options,
                                                                  clear.stageId, clear.alignmentId,
                                                                  world.options.percent_overrides),
                        100, clear.stageId, clear.alignmentId,
                        override_settings)

                    progress_distribution = clear.getDistribution().items()
                    progress_dist_by_name = {}

                    total = 0

                    if world.options.objective_sanity_system == Options.ObjectiveSanitySystem.option_individual:
                        if (clear.stageId, clear.alignmentId) in Objects.STAGE_OBJECT_ITEMS:
                            lookup_info = Objects.STAGE_OBJECT_ITEMS[(clear.stageId, clear.alignmentId)]
                            is_objectable = lookup_info[1]
                            if is_objectable == Objects.WORKS_WITH_INDIVIDUAL:
                                total = -1
                    if total != -1:
                        for region, count in progress_distribution:
                            progress_dist_by_name[Names.GetDistributionRegionEventName(clear.stageId, region)] = count
                            total += count

                    for l in range(1, total + 1):
                        if l > max_required:
                            break

                        if l % frequency_required != 0 and max_required != l:
                            continue

                        prog_rule = lambda state, ix=l, data=progress_dist_by_name, keys=progress_dist_by_name.keys() \
                            : CountRegionAccessibility(state, keys, data, ix, player)

                        location_id, objective_location_name = (
                            Levels.GetLevelObjectNames(clear.stageId, clear.alignmentId, clear.mission_object_name,
                                                l))
                        location = multiworld.get_location(objective_location_name, player)

                        progression_rule = lambda state, p_rule=prog_rule, r_rule=req_rule : \
                            p_rule(state) and r_rule(state)

                        add_rule(location, progression_rule)

                        if l > max_required:
                            break


            if clear.requirement_count is not None:
                location = multiworld.get_location(name, player)
                item_name = Items.GetStageAlignmentObject(clear.stageId, clear.alignmentId)
                max_required = ShadowUtils.getMaxRequired(
                    ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION,
                                                              clear.mission_object_name, world.options,
                                                              clear.stageId, clear.alignmentId,
                                                              world.options.percent_overrides),
                    clear.requirement_count, clear.stageId, clear.alignmentId,
                    override_settings)

                new_rule = lambda state: True
                if world.options.objective_sanity and world.options.objective_sanity_behaviour != Options.ObjectiveSanityBehaviour.option_base_clear:
                    new_rule = lambda state, itemname=item_name, count=max_required: state.has(itemname, player, count=count)

                progress_distribution = clear.getDistribution().items()
                progress_dist_by_name = {}

                total = 0

                if total != -1:
                    for region, count in progress_distribution:
                        progress_dist_by_name[Names.GetDistributionRegionEventName(clear.stageId, region)] = count
                        total += count

                finish_count = 1
                if (not world.options.objective_sanity
                        or world.options.objective_sanity_behaviour != Options.ObjectiveSanityBehaviour.option_default):
                    finish_count = max_required
                    if finish_count == 0:
                        finish_count = 1

                # Enemy stage clears don't require completing objectives
                if world.options.objective_sanity and world.options.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_default and \
                    clear.mission_object_name in ("Soldier", "Artificial Chaos", "Alien"):
                    finish_count = 0

                prog_rule = lambda state, keys=progress_dist_by_name.keys(), data=progress_dist_by_name,\
                                   ix=finish_count\
                    : CountRegionAccessibility(state, keys, data, ix, player)

                # Does this work as an AND or an OR?
                level_rule = lambda state, l_rule=level_rule, n_rule=new_rule, p_rule=prog_rule:\
                    l_rule(state) and n_rule(state) and p_rule(state)
                add_rule(location, level_rule)
                rule_change = True
            else:

                # if equal to 1 there should only be one, and we need that region to finish
                # e.g. goal ring, core, etc.
                if clear.getDistribution() is not None:

                    # This functionality requires access to ALL to complete which is inflating
                    # When logically you can find with access to either
                    # But this also needs handling for objective-less
                    for region_id in clear.getDistribution().keys():
                        required_region = Regions.stage_id_to_region(clear.stageId, region_id)
                        new_rule = lambda state, r_region=required_region: state.can_reach_region(r_region, player)
                        level_rule = lambda state, l_rule=level_rule, n_rule=new_rule: n_rule(state) and l_rule(state)
                        rule_change = True

                location = multiworld.get_location(name, player)
                if rule_change:
                    add_rule(location, level_rule)

            associated_tokens = [t for t in world.token_locations if
                                 t.alignmentId == clear.alignmentId and
                                 t.stageId == clear.stageId and t.other != Items.ITEM_TOKEN_TYPE_BOSS]

            for token in associated_tokens:
                location = multiworld.get_location(token.name, player)
                if rule_change:
                    add_rule(location, level_rule)
                allocated_item = GetRelevantTokenItem(token)
                if allocated_item is None:
                    print("Could not resolve:", token)
                    continue
                if allocated_item.name not in token_assignments:
                    token_assignments[allocated_item.name] = []
                token_assignments[allocated_item.name].append(location)
                mw_token_item = ShadowTheHedgehogItem(allocated_item, world.player)
                location.place_locked_item(
                    mw_token_item)

        #except KeyError as e:
        #    # Do nothing for mission locations that do not exist
        #    print("Key error in handling!", e)
        #    pass

    for boss in BossClearLocations:
        if boss.stageId not in world.available_levels:
            continue

        if boss.stageId == Levels.BOSS_DEVIL_DOOM:
            continue

        boss_id, boss_name = Locations.GetBossLocationName(boss.name, boss.stageId)
        location = multiworld.get_location(boss_name, player)

        boss_rule = None
        if boss.requirements is not None:
            if boss.stageId not in world.available_levels:
                continue
            lr = Levels.LevelRegion(boss.stageId, None, boss.requirements)
            lr.setLogicType(boss.logicType)
            req_rule = handle_path_rules(world.options, player, lr, Levels.REGION_RESTRICTION_REFERENCE_TYPES.BossLogic)
            if req_rule is not None:
                boss_rule = lambda state, r_rule=req_rule: r_rule(state)
                boss_id, boss_name = Locations.GetBossLocationName(boss.name, boss.stageId)
                location = multiworld.get_location(boss_name, player)
                add_rule(location, boss_rule)

        associated_tokens = [t for t in world.token_locations if
                             t.stageId == boss.stageId and
                             (t.other == Items.ITEM_TOKEN_TYPE_BOSS or t.other == Items.ITEM_TOKEN_TYPE_FINAL_BOSS)]
        for token in associated_tokens:
            allocated_item = GetRelevantTokenItem(token)
            if allocated_item.name not in token_assignments:
                token_assignments[allocated_item.name] = []
            token_location = multiworld.get_location(token.name, player)
            if boss_rule is not None:
                add_rule(token_location, boss_rule)
            token_assignments[allocated_item.name].append(location)
            mw_token_item = ShadowTheHedgehogItem(allocated_item, world.player)
            token_location.place_locked_item(
                mw_token_item)

    for character,stages in Levels.CharacterToLevel.items():
        if character in world.available_characters:
            region_name = character_name_to_region(character)
            region = world.get_region(region_name)
            for stage in stages:
                region_index = 0
                if type(stage) is tuple:
                    region_index = stage[1]
                    stage = stage[0]
                    pass

                if stage not in world.available_levels:
                    continue
                region_stage = world.get_region(stage_id_to_region(stage, region_index))
                region_stage.connect(region, region_name_for_character(Levels.LEVEL_ID_TO_LEVEL[stage], character))

    for weapon in Weapons.WEAPON_INFO:
        if weapon.name in world.available_weapons:
            region_name = weapon_name_to_region(weapon.name)
            region = world.get_region(region_name)
            for stage in weapon.available_stages:
                region_index = 0
                if type(stage) is tuple:
                    region_index = stage[1]
                    stage = stage[0]
                    pass

                if stage not in world.available_levels:
                    continue

                rule = lambda state: True

                if (world.options.weapon_sanity_unlock and
                    world.options.weapon_sanity_hold == Options.WeaponsanityHold.option_unlocked) or \
                    Weapons.WeaponAttributes.SPECIAL in weapon.attributes:
                        rule = Weapons.GetRuleByWeaponRequirement(player, weapon.name, None, None)

                region_stage = world.get_region(stage_id_to_region(stage, region_index))
                region_stage.connect(region, region_name_for_weapon(Levels.LEVEL_ID_TO_LEVEL[stage], weapon.name),
                                     rule=rule)

    if world.options.enemy_sanity and world.options.objective_sanity_system != Options.ObjectiveSanitySystem.option_individual:
        for enemy in Locations.GetEnemySanityLocations():

            if enemy.stageId not in world.available_levels:
                continue

            if world.options.exclude_go_mode_items and enemy.stageId == Levels.STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue

            max_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                          enemy.mission_object_name, world.options,
                                                          enemy.stageId, enemy.enemyClass,
                                                          world.options.percent_overrides),
                enemy.total_count, enemy.stageId, enemy.enemyClass,
                override_settings)

            perc_required = ShadowUtils.getPercRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                          enemy.mission_object_name, world.options,
                                                          enemy.stageId, enemy.enemyClass,
                                                          world.options.percent_overrides),
                enemy.stageId, enemy.enemyClass,
                override_settings)


            frequency_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY_FREQUENCY,
                                                          enemy.mission_object_name, world.options,
                                                          enemy.stageId, enemy.enemyClass,
                                                          world.options.percent_overrides),
                100, enemy.stageId, enemy.enemyClass,
                override_settings)


            enemy_distribution = enemy.getDistribution().items()
            enemy_dist_by_name = {}

            total = 0
            for region, count in enemy_distribution:
                enemy_dist_by_name[Names.GetDistributionRegionEventName(enemy.stageId, region)] = count
                total += count

            for l in range(1, total+1):
                if l > max_required:
                    break

                if l % frequency_required != 0 and max_required != l:
                    continue

                new_rule = lambda state, ix=l, data=enemy_dist_by_name, keys=enemy_dist_by_name.keys(),p=perc_required\
                    : CountRegionAccessibility(state, keys, data, ix, player, p)
                location_id, objective_location_name = (
                    Locations.GetEnemyLocationName(enemy.stageId, enemy.enemyClass, enemy.mission_object_name,
                                        l))
                location = multiworld.get_location(objective_location_name, player)
                add_rule(location, new_rule)

                if l > max_required:
                    break

    goal_has = []
    if world.options.goal_chaos_emeralds:
        emeralds = Items.GetEmeraldItems()
        goal_has.extend([ (ce.name,1) for ce in emeralds ])
    if world.options.goal_missions > 0:
        tokens = get_token_count(world, Items.Progression.StandardMissionToken, token_assignments, world.options.goal_missions)
        goal_has.append(tokens)
    if world.options.goal_hero_missions > 0:
        tokens = get_token_count(world, Items.Progression.StandardHeroToken, token_assignments, world.options.goal_hero_missions)
        goal_has.append(tokens)
    if world.options.goal_dark_missions > 0:
        tokens = get_token_count(world, Items.Progression.StandardDarkToken, token_assignments, world.options.goal_dark_missions)
        goal_has.append(tokens)
    if world.options.goal_final_missions > 0:
        tokens = get_token_count(world, Items.Progression.FinalToken, token_assignments, world.options.goal_final_missions)
        goal_has.append(tokens)
    if world.options.goal_objective_missions > 0:
        tokens = get_token_count(world, Items.Progression.ObjectiveToken, token_assignments, world.options.goal_objective_missions)
        goal_has.append(tokens)
    if world.options.goal_bosses > 0:
        tokens = get_token_count(world, Items.Progression.BossToken, token_assignments, world.options.goal_bosses)
        goal_has.append(tokens)
    if world.options.goal_final_bosses > 0:
        tokens = get_token_count(world, Items.Progression.FinalBossToken, token_assignments, world.options.goal_final_bosses)
        goal_has.append(tokens)
    if world.options.include_last_way_shuffle:
        pass

    e_rule = lambda state, g_has=goal_has: check_final_rule(state, player, goal_has)

    if world.options.include_last_way_shuffle:

        # handle requirement that DD must be found in the level shuffle!
        devil_doom_story_region = Regions.stage_id_to_story_region(Levels.BOSS_DEVIL_DOOM)
        devil_doom_region = multiworld.get_region(devil_doom_story_region, player)

        for entrance in devil_doom_region.entrances:
            entrance.access_rule = lambda state, er=e_rule, b_rule=entrance.access_rule: er(state) and b_rule(state)
            #entrance.access_rule = lambda state, er=e_rule : er(state) and state.can_reach_region(devil_doom_story_region, player)
        #multiworld.register_indirect_condition(multiworld.get_region(devil_doom_story_region, player),
        #                                       multiworld.get_entrance('devil-doom-fight', player))

    else:
        last_way_region = multiworld.get_region(stage_id_to_region(Levels.STAGE_THE_LAST_WAY), player)
        connect(world.player, 'LastStoryToLastWay', multiworld.get_region("Menu", player),
                last_way_region, rule=e_rule)
        # Ensure TLW is beatable
        tlw_location_id, tlw_location_name = Levels.GetLevelCompletionNames(Levels.STAGE_THE_LAST_WAY, Levels.MISSION_ALIGNMENT_NEUTRAL)
        last_way_rule = lambda state: state.can_reach_location(tlw_location_name, player)
        entrance = connect(world.player, "LastWayToDevilDoom", last_way_region,
                multiworld.get_region(Regions.stage_id_to_region(Levels.BOSS_DEVIL_DOOM), player))

        entrance.access_rule = lambda state, lw_rule=last_way_rule, er=e_rule: er(state) and lw_rule(state)

    final_item = Items.GetFinalItem()
    mw_final_item = ShadowTheHedgehogItem(final_item, world.player)
    multiworld.get_location(Levels.DevilDoom_Name, world.player).place_locked_item(
        mw_final_item)

    if world.options.rifle_components:
        location = multiworld.get_location("Complete Shadow Rifle", player)
        shadow_rifle = Items.GetShadowRifle()
        mw_shadow_rifle = ShadowTheHedgehogItem(shadow_rifle, world.player)
        location.place_locked_item(mw_shadow_rifle)

        rifle_components = Items.GetRifleComponents()
        rifle_rule = lambda state: True

        for component in rifle_components:
            new_rifle_part = lambda state, cn=component.name: state.has(cn, player)
            rifle_rule = lambda state, rr=rifle_rule, nrp=new_rifle_part: rr(state) and nrp(state)

        add_rule(location, rifle_rule)

    multiworld.completion_condition[player] = lambda state: state.has(Items.Progression.GoodbyeForever, player)

def check_final_rule(state, player, goal_has):
    have = ([x for x in goal_has if state.has(x[0], player, count=x[1])])
    return len(have) == len(goal_has)

def get_token_count(world, type, token_assignments, goal_value):
    if type not in token_assignments:
        return (type, 0)
    count = len(token_assignments[type])
    goal_req = Utils.getRequiredCount(count, goal_value, ceil)
    world.required_tokens[type] = goal_req
    return (type, goal_req)


def connect(player: int, name: str,
            source_region: Region, target_region: Region,
            rule: typing.Optional[typing.Callable] = None):
    connection = Entrance(player, name, source_region)

    if rule is not None:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
    return connection
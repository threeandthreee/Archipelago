from __future__ import annotations

import functools
from typing import Any, Dict, List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TheElderScrollsVSkyrimSpecialEditionArchipelagoOptions:
    the_elder_scrolls_v_skyrim_special_edition_dlc_owned: TheElderScrollsVSkyrimSpecialEditionDLCOwned


class TheElderScrollsVSkyrimSpecialEditionGame(Game):
    name = "The Elder Scrolls V: Skyrim - Special Edition"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    should_autoregister = False
    is_adult_only_or_unrated = True

    options_cls = TheElderScrollsVSkyrimSpecialEditionArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Create a new RACE character.  Sex: SEX  Skill: SKILL  Armor: ARMOR  Difficulty: DIFFICULTY  Survival: SURVIVAL",
                data={
                    "RACE": (self.races, 1),
                    "SEX": (self.sexes, 1),
                    "SKILL": (self.main_skills, 1),
                    "ARMOR": (self.armor_classes, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "SURVIVAL": (self.survival_mode, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Unlock all the achievements in GAME",
                data={"GAME": (self.games, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

        # Join the following Faction: FACTION
        # Complete the following Daedric Quest: QUEST
        # Complete the following Side Quest: QUEST
        # Have at least COUNT ATTRIBUTE points
        # Reach Level LEVEL
        # Level SKILL to LEVEL
        # Level SKILLS to LEVEL
        # Make the following skill Legendary: SKILL
        # Unlock the following perk: PERK
        # Unlock the following perks: PERKS
        # Unlock COUNT perks in the SKILL tree
        # Harvest COUNTx RESOURCE
        # Discover COUNT Alchemy Effects from the following ingredient: INGREDIENT
        # Brew COUNT Potions (or Poisons) using the following ingredient: INGREDIENT
        # Brew COUNT Potions with the following effect: EFFECT
        # Brew COUNT Poisons with the following effect: EFFECT
        # Enchant an item to the following specification: SPECIFICATION
        # Learn the following Enchantment Effect through disenchantment: ENCHANTMENT
        # Trap the Soul of the following creature in a Soul Gem: CREATURE
        # Enchant the following Staff: STAFF
        # At a Forge, craft COUNT items from the following category: CATEGORY
        # At a Grindstone, improve a Weapon from the following category to QUALITY quality: CATEGORY
        # At a Workbench, improve a piece of Armor from the following category to QUALITY quality: CATEGORY
        # Obtain the following outcome at the Atronach Forge: OUTCOME
        # Bake COUNTx ITEM at an Oven
        # Collect COUNT of the following Baking Ingredient: INGREDIENT
        # Fully construct the following house: HOUSE
        # Construct and fully furnish the following section for HOUSE: SECTION
        # Cook COUNTx ITEM at a Cooking Pot
        # Collect COUNT of the following Cooking Ingredient: INGREDIENT


        # Fishing
        # Hunting

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.the_elder_scrolls_v_skyrim_special_edition_dlc_owned.value)

    @property
    def has_anniversary_upgrade(self) -> bool:
        return "Anniversary Upgrade" in self.dlc_owned

    @staticmethod
    def races() -> List[str]:
        return [
            "Argonian",
            "Breton",
            "Dark Elf",
            "High Elf",
            "Imperial",
            "Khajiit",
            "Nord",
            "Orc",
            "Redguard",
            "Wood Elf",
        ]

    @staticmethod
    def sexes() -> List[str]:
        return [
            "Female",
            "Male",
        ]

    @functools.cached_property
    def mains_skills_by_skill(self) -> Dict[str, Any]:
        return {
            "Alchemy": self.main_skills_alchemy,
            "Alteration": self.main_skills_alteration,
            "Archery": self.main_skills_archery,
            "Block": self.main_skills_block,
            "Conjuration": self.main_skills_conjuration,
            "Destruction": self.main_skills_destruction,
            "Enchanting": self.main_skills_enchanting,
            "Illusion": self.main_skills_illusion,
            "Lockpicking": self.main_skills_lockpicking,
            "One-Handed": self.main_skills_one_handed,
            "Pickpocket": self.main_skills_pickpocket,
            "Restoration": self.main_skills_restoration,
            "Smithing": self.main_skills_smithing,
            "Sneak": self.main_skills_sneak,
            "Speech": self.main_skills_speech,
            "Two-Handed": self.main_skills_two_handed,
            "Unarmed": self.main_skills_unarmed,
        }

    def main_skills(self) -> List[str]:
        skill: str = self.random.choice(list(self.mains_skills_by_skill.keys()))

        return self.mains_skills_by_skill[skill]

    @staticmethod
    def main_skills_alchemy() -> List[str]:
        return [
            "Alchemy (Buffs)",
            "Alchemy (Poisoned Blades)",
            "Alchemy (Poisoned Projectiles)",
        ]

    @staticmethod
    def main_skills_alteration() -> List[str]:
        return [
            "Alteration (Magic Armor)",
            "Alteration (Paralysis)",
        ]

    @staticmethod
    def main_skills_archery() -> List[str]:
        return [
            "Archery (Bows)",
            "Archery (Crossbows)",
        ]

    @staticmethod
    def main_skills_block() -> List[str]:
        return [
            "Block (Shield Bash)",
        ]

    @staticmethod
    def main_skills_conjuration() -> List[str]:
        return [
            "Conjuration (Bound Weapons)",
            "Conjuration (Daedra Summons)",
            "Conjuration (Spirit Summons)",
            "Conjuration (Undead Summons)",
        ]

    @staticmethod
    def main_skills_destruction() -> List[str]:
        return [
            "Destruction (Fire)",
            "Destruction (Frost)",
            "Destruction (Shock)",
        ]

    @staticmethod
    def main_skills_enchanting() -> List[str]:
        return [
            "Enchanting (Self-Enchanted Gear)",
        ]

    @staticmethod
    def main_skills_illusion() -> List[str]:
        return [
            "Illusion (Frenzy)",
            "Illusion (Invisibility)",
        ]

    @staticmethod
    def main_skills_lockpicking() -> List[str]:
        return [
            "Lockpicking (Treasure Hunter)",
        ]

    @staticmethod
    def main_skills_one_handed() -> List[str]:
        return [
            "One-Handed (Maces)",
            "One-Handed (Swords)",
            "One-Handed (War Axes)",
        ]

    @staticmethod
    def main_skills_pickpocket() -> List[str]:
        return [
            "Pickpocket (Thief)",
        ]

    @staticmethod
    def main_skills_restoration() -> List[str]:
        return [
            "Restoration (Party Healer)",
        ]

    @staticmethod
    def main_skills_smithing() -> List[str]:
        return [
            "Smithing (Self-Crafted Gear)",
        ]

    @staticmethod
    def main_skills_sneak() -> List[str]:
        return [
            "Sneak (Dagger Attacks)",
            "Sneak (Melee Attacks)",
            "Sneak (Ranged Attacks)",
        ]

    @staticmethod
    def main_skills_speech() -> List[str]:
        return [
            "Speech (Merchant)",
        ]

    @staticmethod
    def main_skills_two_handed() -> List[str]:
        return [
            "Two-Handed (Battle Axes)",
            "Two-Handed (Greatswords)",
            "Two-Handed (Warhammers)",
        ]

    @staticmethod
    def main_skills_unarmed() -> List[str]:
        return [
            "Unarmed (Fist Weapons)",
        ]

    @staticmethod
    def armor_classes() -> List[str]:
        return [
            "Light",
            "Light",
            "Light",
            "Heavy",
            "Heavy",
            "Heavy",
            "Unarmored",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Novice",
            "Apprentice",
            "Adept",
            "Expert",
            "Master",
            "Legendary",
        ]

    @staticmethod
    def survival_mode() -> List[str]:
        return ["Off", "Off", "Off", "On"]

    @functools.cached_property
    def factions_base(self) -> List[str]:
        return [
            "Companions",
            "College of Winterhold",
            "Thieves Guild",
            "Dark Brotherhood",
            "Imperial Legion",
            "Stormcloaks",
            "Bards College",
            "Dawnguard",
            "Volkihar Vampire Clan",
        ]

    @functools.cached_property
    def factions_anniversary(self) -> List[str]:
        return [
            "Tribunal Temple",
        ]

    def factions(self) -> List[str]:
        factions: List[str] = self.factions_base[:]

        if self.has_anniversary_upgrade:
            factions.extend(self.factions_anniversary)

        return sorted(factions)

    @staticmethod
    def quests_daedric() -> List[str]:
        return [
            "The Black Star (Azura)",
            "Boethiah's Calling (Boethiah)",
            "A Daedra's Best Friend (Clavicus Vile)",
            "Discerning the Transmundane (Hermaeus Mora)",
            "Ill Met By Moonlight (Hircine)",
            "The Cursed Tribe (Malacath)",
            "Pieces of the Past (Mehrunes Dagon)",
            "The Whispering Door (Mephala)",
            "The Break of Dawn (Meridia)",
            "The House of Horrors (Molag Bal)",
            "The Taste of Death (Namira)",
            "Darkness Returns (Nocturnal)",
            "The Only Cure (Peryite)",
            "A Night To Remember (Sanguine)",
            "The Mind of Madness (Sheogorath)",
            "Waking Nightmare (Vaermina)",
        ]

    @staticmethod
    def quests_side() -> List[str]:
        return [
            "No One Escapes Cidhna Mine (Markarth)",
            "The Forsworn Conspiracy (Markarth)",
            "The Heart of Dibella (Markarth)",
            "The Lost Expedition (Markarth)",
            "Laid to Rest (Morthal)",
            "Rising at Dawn (Morthal)",
            "A New Debt (Raven Rock)",
            "Black Book: The Winds of Change (Raven Rock)",
            "March of the Dead (Raven Rock)",
            "Served Cold (Raven Rock)",
            "The Final Descent (Raven Rock)",
            "Promises to Keep (Riften)",
            "The Book of Love (Riften)",
            "Unfathomable Depths (Riften)",
            "Lights Out! (Solitude)",
            "Tending the Flames (Solitude)",
            "The Man Who Cried Wolf (Solitude)",
            "The Wolf Queen Awakened (Solitude)",
            "In My Time Of Need (Whiterun)",
            "Missing In Action (Whiterun)",
            "The Blessings of Nature (Whiterun)",
            "Blood on the Ice (Windhelm)",
            "Repairing the Phial (Windhelm)",
            "Rise in the East (Windhelm)",
            "The White Phial (Windhelm)",
            "The Golden Claw (Riverwood)",
            "A New Source of Stalhrim (Skaal Village)",
            "Filial Bonds (Skaal Village)",
            "Lost Legacy (Skaal Village)",
            "Azra's Staffs (Tel Mithryn)",
            "Black Book: The Hidden Twilight (Tel Mithryn)",
            "Briarheart Necropsy (Tel Mithryn)",
            "Experimental Subject A (Tel Mithryn)",
            "From the Ashes (Tel Mithryn)",
            "Healing a House (Tel Mithryn)",
            "Heart Stones (Tel Mithryn)",
            "Lost Knowledge (Tel Mithryn)",
            "Old Friends (Tel Mithryn)",
            "Reluctant Steward (Tel Mithryn)",
            "Telvanni Research (Tel Mithryn)",
            "Wind and Sand (Tel Mithryn)",
            "Retaking Thirsk (Thirsk Mead Hall)",
            "The Chief of Thirsk Hall (Thirsk Mead Hall)",
        ]

    @staticmethod
    def attributes() -> List[str]:
        return [
            "Health",
            "Magicka",
            "Stamina",
        ]

    @staticmethod
    def attribute_range() -> range:
        return range(200, 501, 10)

    @staticmethod
    def level_range() -> range:
        return range(20, 81)

    @staticmethod
    def skill_level_range() -> range:
        return range(25, 91)

    @staticmethod
    def skills() -> List[str]:
        return [
            "Alteration",
            "Archery",
            "Alchemy",
            "Conjuration",
            "Block",
            "Light Armor",
            "Destruction",
            "Heavy Armor",
            "Lockpicking",
            "Enchanting",
            "One-Handed",
            "Pickpocket",
            "Illusion",
            "Smithing",
            "Sneak",
            "Restoration",
            "Two-Handed",
            "Speech",
        ]

    @staticmethod
    def perk_unlock_range() -> range:
        return range(3, 7)

    @staticmethod
    def perks() -> List[str]:
        return [
            "Novice Alteration (Alteration)",
            "Alteration Dual Casting (Alteration)",
            "Apprentice Alteration (Alteration)",
            "Magic Resistance (Alteration)",
            "Adept Alteration (Alteration)",
            "Expert Alteration (Alteration)",
            "Atronach (Alteration)",
            "Master Alteration (Alteration)",
            "Stability (Alteration)",
            "Mage Armor (Alteration)",
            "Overdraw (Archery)",
            "Critical Shot (Archery)",
            "Hunter's Discipline (Archery)",
            "Ranger (Archery)",
            "Eagle Eye (Archery)",
            "Power Shot (Archery)",
            "Quick Shot (Archery)",
            "Steady Hand (Archery)",
            "Bullseye (Archery)",
            "Alchemist (Alchemy)",
            "Physician (Alchemy)",
            "Benefactor (Alchemy)",
            "Experimenter (Alchemy)",
            "Poisoner (Alchemy)",
            "Concentrated Poison (Alchemy)",
            "Green Thumb (Alchemy)",
            "Snakeblood (Alchemy)",
            "Purity (Alchemy)",
            "Novice Conjuration (Conjuration)",
            "Apprentice Conjuration (Conjuration)",
            "Adept Conjuration (Conjuration)",
            "Expert Conjuration (Conjuration)",
            "Master Conjuration (Conjuration)",
            "Conjuration Dual Casting (Conjuration)",
            "Mystic Binding (Conjuration)",
            "Soul Stealer (Conjuration)",
            "Oblivion Binding (Conjuration)",
            "Necromancy (Conjuration)",
            "Dark Souls (Conjuration)",
            "Summoner (Conjuration)",
            "Atromancy (Conjuration)",
            "Elemental Potency (Conjuration)",
            "Twin Souls (Conjuration)",
            "Shield Wall (Block)",
            "Deflect Arrows (Block)",
            "Elemental Protection (Block)",
            "Block Runner (Block)",
            "Power Bash (Block)",
            "Deadly Bash (Block)",
            "Disarming Bash (Block)",
            "Shield Charge (Block)",
            "Quick Reflexes (Block)",
            "Agile Defender (Light Armor)",
            "Custom Fit (Light Armor)",
            "Matching Set (Light Armor)",
            "Unhindered (Light Armor)",
            "Wind Walker (Light Armor)",
            "Deft Movement (Light Armor)",
            "Novice Destruction (Destruction)",
            "Apprentice Destruction (Destruction)",
            "Adept Destruction (Destruction)",
            "Expert Destruction (Destruction)",
            "Master Destruction (Destruction)",
            "Rune Master (Destruction)",
            "Augmented Flames (Destruction)",
            "Intense Flames (Destruction)",
            "Augmented Frost (Destruction)",
            "Deep Freeze (Destruction)",
            "Augmented Shock (Destruction)",
            "Disintegrate (Destruction)",
            "Destruction Dual Casting (Destruction)",
            "Impact (Destruction)",
            "Juggernaut (Heavy Armor)",
            "Fists of Steel (Heavy Armor)",
            "Cushioned (Heavy Armor)",
            "Conditioning (Heavy Armor)",
            "Well Fitted (Heavy Armor)",
            "Tower of Strength (Heavy Armor)",
            "Matching Set (Heavy Armor)",
            "Reflect Blows (Heavy Armor)",
            "Novice Locks (Lockpicking)",
            "Apprentice Locks (Lockpicking)",
            "Quick Hands (Lockpicking)",
            "Wax Key (Lockpicking)",
            "Adept Locks (Lockpicking)",
            "Expert Locks (Lockpicking)",
            "Golden Touch (Lockpicking)",
            "Treasure Hunter (Lockpicking)",
            "Locksmith (Lockpicking)",
            "Unbreakable (Lockpicking)",
            "Master Locks (Lockpicking)",
            "Enchanter (Enchanting)",
            "Fire Enchanter (Enchanting)",
            "Frost Enchanter (Enchanting)",
            "Storm Enchanter (Enchanting)",
            "Insightful Enchanter (Enchanting)",
            "Corpus Enchanter (Enchanting)",
            "Extra Effect (Enchanting)",
            "Soul Squeezer (Enchanting)",
            "Soul Siphon (Enchanting)",
            "Armsman (One-Handed)",
            "Bladesman (One-Handed)",
            "Bone Breaker (One-Handed)",
            "Dual Flurry (One-Handed)",
            "Dual Savagery (One-Handed)",
            "Fighting Stance (One-Handed)",
            "Critical Charge (One-Handed)",
            "Savage Strike (One-Handed)",
            "Paralyzing Strike (One-Handed)",
            "Hack and Slash (One-Handed)",
            "Light Fingers (Pickpocket)",
            "Night Thief (Pickpocket)",
            "Cutpurse (Pickpocket)",
            "Keymaster (Pickpocket)",
            "Misdirection (Pickpocket)",
            "Perfect Touch (Pickpocket)",
            "Extra Pockets (Pickpocket)",
            "Poisoned (Pickpocket)",
            "Novice Illusion (Illusion)",
            "Animage (Illusion)",
            "Kindred Mage (Illusion)",
            "Quiet Casting (Illusion)",
            "Apprentice Illusion (Illusion)",
            "Adept Illusion (Illusion)",
            "Expert Illusion (Illusion)",
            "Master Illusion (Illusion)",
            "Hypnotic Gaze (Illusion)",
            "Aspect of Terror (Illusion)",
            "Rage (Illusion)",
            "Master of the Mind (Illusion)",
            "Illusion Dual Casting (Illusion)",
            "Steel Smithing (Smithing)",
            "Arcane Blacksmith (Smithing)",
            "Dwarven Smithing (Smithing)",
            "Orcish Smithing (Smithing)",
            "Ebony Smithing (Smithing)",
            "Daedric Smithing (Smithing)",
            "Elven Smithing (Smithing)",
            "Advanced Armors (Smithing)",
            "Glass Smithing (Smithing)",
            "Dragon Armor (Smithing)",
            "Stealth (Sneak)",
            "Backstab (Sneak)",
            "Deadly Aim (Sneak)",
            "Assassin's Blade (Sneak)",
            "Muffled Movement (Sneak)",
            "Light Foot (Sneak)",
            "Silent Roll (Sneak)",
            "Silence (Sneak)",
            "Shadow Warrior (Sneak)",
            "Novice Restoration (Restoration)",
            "Apprentice Restoration (Restoration)",
            "Adept Restoration (Restoration)",
            "Expert Restoration (Restoration)",
            "Master Restoration (Restoration)",
            "Recovery (Restoration)",
            "Avoid Death (Restoration)",
            "Regeneration (Restoration)",
            "Necromage (Restoration)",
            "Respite (Restoration)",
            "Restoration Dual Casting (Restoration)",
            "Ward Absorb (Restoration)",
            "Barbarian (Two-Handed)",
            "Champion's Stance (Two-Handed)",
            "Devastating Blow (Two-Handed)",
            "Great Critical Charge (Two-Handed)",
            "Sweep (Two-Handed)",
            "Warmaster (Two-Handed)",
            "Deep Wounds (Two-Handed)",
            "Limbsplitter (Two-Handed)",
            "Skullcrusher (Two-Handed)",
            "Haggling (Speech)",
            "Allure (Speech)",
            "Merchant (Speech)",
            "Investor (Speech)",
            "Fence (Speech)",
            "Master Trader (Speech)",
            "Bribery (Speech)",
            "Persuasion (Speech)",
            "Intimidation (Speech)",
        ]

    @staticmethod
    def harvest_count_range() -> range:
        return range(3, 11)

    @functools.cached_property
    def harvestables_base(self) -> List[str]:
        return [
            "Beehive Husk",
            "Bleeding Crown",
            "Blisterwort",
            "Blue Mountain Flower",
            "Cabbage",
            "Canis Root",
            "Carrot",
            "Chaurus Egg",
            "Creep Cluster",
            "Crimson Nirnroot",
            "Deathbell",
            "Dragon's Tongue",
            "Elves Ear",
            "Flame Stalk",
            "Fly Amanita",
            "Frost Mirriam",
            "Garlic",
            "Giant Lichen",
            "Gleamblossom",
            "Glowing Mushroom",
            "Gourd",
            "Grass Pod",
            "Hanging Moss",
            "Honeycomb",
            "Imp Stool",
            "Jazbay Grapes",
            "Juniper Berries",
            "Lavender",
            "Leek",
            "Mora Tapinella",
            "Namira's Rot",
            "Nightshade",
            "Nirnroot",
            "Nordic Barnacle",
            "Poison Bloom",
            "Potato",
            "Purple Mountain Flower",
            "Red Mountain Flower",
            "Rot Scale",
            "Scaly Pholiota",
            "Screaming Maw",
            "Snowberries",
            "Swamp Fungal Pod",
            "Thistle Branch",
            "Thorn Hook",
            "Tundra Cotton",
            "Wheat",
            "White Cap",
            "Yellow Mountain Flower",
        ]

    @functools.cached_property
    def harvestables_anniversary(self) -> List[str]:
        return [
            "Bloodgrass",
            "Harrada",
            "Ironwood Fruit",
            "Spiddal Stick",
            "Steel-Blue Entoloma",
        ]

    def harvestables(self) -> List[str]:
        harvestables: List[str] = self.harvestables_base[:]

        if self.has_anniversary_upgrade:
            harvestables.extend(self.harvestables_anniversary)

        return sorted(harvestables)

    @staticmethod
    def alchemy_effect_count_range() -> range:
        return range(2, 5)

    @functools.cached_property
    def alchemy_ingredients_base(self) -> List[str]:
        return [
            "Abecean Longfin",
            "Alocasia Fruit",
            "Aloe Vera Leaves",
            "Ambrosia",
            "Ancestor Moth Wing",
            "Angelfish",
            "Angler Larvae",
            "Ash Creep Cluster",
            "Ash Hopper Jelly",
            "Ashen Grass Pod",
            "Aster Bloom Core",
            "Bear Claws",
            "Bee",
            "Beehive Husk",
            "Bittergreen Petals",
            "Bleeding Crown",
            "Blind Watcher's Eye",
            "Bliss Bug Thorax",
            "Blister Pod Cap",
            "Blisterwort",
            "Blue Butterfly Wing",
            "Blue Dartwing",
            "Blue Mountain Flower",
            "Boar Tusk",
            "Bog Beacon",
            "Bone Meal",
            "Briar Heart",
            "Bungler's Bane",
            "Burnt Spriggan Wood",
            "Butterfly Wing",
            "Canis Root",
            "Charred Skeever Hide",
            "Chaurus Eggs",
            "Chaurus Hunter Antennae",
            "Chicken's Egg",
            "Chokeberry",
            "Chokeweed",
            "Coda Flower",
            "Comberry",
            "Congealed Putrescence",
            "Corkbulb Root",
            "Creep Cluster",
            "Crimson Nirnroot",
            "Cyrodilic Spadetail",
            "Daedra Heart",
            "Daedra Silk",
            "Daedra Venin",
            "Daedroth Teeth",
            "Deathbell",
            "Dragon's Tongue",
            "Dreugh Wax",
            "Dwarven Oil",
            "Ectoplasm",
            "Elves Ear",
            "Elytra Ichor",
            "Emperor Parasol Moss",
            "Eye of Sabre Cat",
            "Falmer Ear",
            "Felsaad Tern Feathers",
            "Fire Petal",
            "Fire Salts",
            "Flame Stalk",
            "Fly Amanita",
            "Frost Mirriam",
            "Frost Salts",
            "Fungus Stalk",
            "Garlic",
            "Giant Lichen",
            "Giant's Toe",
            "Glassfish",
            "Gleamblossom",
            "Glow Dust",
            "Glowing Mushroom",
            "Gnarl Bark",
            "Gold Kanet",
            "Goldfish",
            "Grass Pod",
            "Green Butterfly Wing",
            "Hackle-Lo Leaf",
            "Hagraven Claw",
            "Hagraven Feathers",
            "Hanging Moss",
            "Hawk Beak",
            "Hawk Feathers",
            "Hawk's Egg",
            "Heart of Order",
            "Histcarp",
            "Honeycomb",
            "Human Flesh",
            "Human Heart",
            "Hunger Tongue",
            "Hydnum Azure Giant Spore",
            "Hypha Facia",
            "Ice Wraith Teeth",
            "Imp Gall",
            "Imp Stool",
            "Jazbay Grapes",
            "Juniper Berries",
            "Juvenile Mudcrab",
            "Kagouti Hide",
            "Kresh Fiber",
            "Large Antlers",
            "Lavender",
            "Lichor",
            "Luminous Russula",
            "Luna Moth Wing",
            "Lyretail Anthias",
            "Marshmerrow",
            "Minotaur Horn",
            "Moon Sugar",
            "Mora Tapinella",
            "Mudcrab Chitin",
            "Namira's Rot",
            "Netch Jelly",
            "Nightshade",
            "Nightshade",
            "Nirnroot",
            "Nordic Barnacle",
            "Ogre's Teeth",
            "Orange Dartwing",
            "Pearl",
            "Pearlfish",
            "Pine Thrush Egg",
            "Poison Bloom",
            "Powdered Mammoth Tusk",
            "Purple Butterfly Wing",
            "Purple Mountain Flower",
            "Pygmy Sunfish",
            "Red Kelp Gas Bladder",
            "Red Mountain Flower",
            "Redwort Flower",
            "River Betty",
            "Rock Warbler Egg",
            "Roobrush",
            "Rot Scale",
            "Sabre Cat Tooth",
            "Salmon Roe",
            "Salt Pile",
            "Saltrice",
            "Scalon Fin",
            "Scaly Pholiota",
            "Scathecraw",
            "Screaming Maw",
            "Scrib Jelly",
            "Scrib Jerky",
            "Silverside Perch",
            "Skeever Tail",
            "Slaughterfish Egg",
            "Slaughterfish Scales",
            "Sload Soap",
            "Small Antlers",
            "Small Pearl",
            "Snowberries",
            "Spadefish",
            "Spawn Ash",
            "Spider Egg",
            "Spriggan Sap",
            "Stoneflower Petals",
            "Swamp Fungal Pod",
            "Taproot",
            "Thistle Branch",
            "Thorn Hook",
            "Torchbug Thorax",
            "Trama Root",
            "Troll Fat",
            "Tundra Cotton",
            "Vampire Dust",
            "Void Essence",
            "Void Salts",
            "Watcher's Eye",
            "Wheat",
            "White Cap",
            "Wisp Stalk Caps",
            "Wisp Wrappings",
            "Withering Moon",
            "Worm's Head Cap",
            "Yellow Mountain Flower",
        ]

    @functools.cached_property
    def alchemy_ingredients_anniversary(self) -> List[str]:
        return [
            "Bloodgrass",
            "Harrada",
            "Ironwood Fruit",
            "Mort Flesh",
            "Spiddal Stick",
            "Steel-Blue Entoloma",
            "Wild Grass Pod",
        ]

    def alchemy_ingredients(self) -> List[str]:
        alchemy_ingredients: List[str] = self.alchemy_ingredients_base[:]

        if self.has_anniversary_upgrade:
            alchemy_ingredients.extend(self.alchemy_ingredients_anniversary)

        return sorted(alchemy_ingredients)

    @staticmethod
    def alchemy_brewing_count_range() -> range:
        return range(2, 8)

    @staticmethod
    def alchemy_effects_potion() -> List[str]:
        return [
            "Cure Disease",
            "Cure Poison",
            "Fortify Alteration",
            "Fortify Barter",
            "Fortify Block",
            "Fortify Carry Weight",
            "Fortify Conjuration",
            "Fortify Destruction",
            "Fortify Enchanting",
            "Fortify Health",
            "Fortify Heavy Armor",
            "Fortify Illusion",
            "Fortify Light Armor",
            "Fortify Lockpicking",
            "Fortify Magicka",
            "Fortify Marksman",
            "Fortify One-Handed",
            "Fortify Pickpocket",
            "Fortify Restoration",
            "Fortify Smithing",
            "Fortify Sneak",
            "Fortify Stamina",
            "Fortify Two-Handed",
            "Invisibility",
            "Light",
            "Night Eye",
            "Regenerate Health",
            "Regenerate Magicka",
            "Regenerate Stamina",
            "Resist Fire",
            "Resist Frost",
            "Resist Magic",
            "Resist Poison",
            "Resist Shock",
            "Restore Health",
            "Restore Magicka",
            "Restore Stamina",
            "Spell Absorption",
            "Waterbreathing",
        ]

    @staticmethod
    def alchemy_effects_poison() -> List[str]:
        return [
            "Damage Health",
            "Damage Magicka",
            "Damage Magicka Regen",
            "Damage Stamina",
            "Damage Stamina Regen",
            "Fear",
            "Frenzy",
            "Lingering Damage Health",
            "Lingering Damage Magicka",
            "Lingering Damage Stamina",
            "Paralysis",
            "Ravage Health",
            "Ravage Magicka",
            "Ravage Stamina",
            "Slow",
            "Weakness to Fire",
            "Weakness to Frost",
            "Weakness to Magic",
            "Weakness to Poison",
            "Weakness to Shock",
        ]

    @functools.cached_property
    def enchantment_effects_by_item_type(self) -> Dict[str, Any]:
        return {
            "Head Apparel": self.enchantment_effects_apparel_head,
            "Neck Apparel": self.enchantment_effects_apparel_neck,
            "Chest Apparel": self.enchantment_effects_apparel_chest,
            "Hands Apparel": self.enchantment_effects_apparel_hands,
            "Finger Apparel": self.enchantment_effects_apparel_finger,
            "Feet Apparel": self.enchantment_effects_apparel_feet,
            "Weapon 1": self.enchantment_effects_weapons,
            "Weapon 2": self.enchantment_effects_weapons,
            "Weapon 3": self.enchantment_effects_weapons,
        }

    def enchantment_effects(self) -> List[str]:
        effect_category: str = self.random.choice(list(self.enchantment_effects_by_item_type.keys()))

        effect_category = effect_category.replace(" 1", "")
        effect_category = effect_category.replace(" 2", "")
        effect_category = effect_category.replace(" 3", "")

        return [f"{effect_category} -> {effect}" for effect in self.enchantment_effects_by_item_type[effect_category]()]

    @staticmethod
    def enchantment_effects_apparel_head() -> List[str]:
        return [
            "Fortify Alchemy",
            "Fortify Alteration",
            "Fortify Archery",
            "Fortify Conjuration",
            "Fortify Destruction",
            "Fortify Illusion",
            "Fortify Lockpicking",
            "Fortify Restoration",
            "Fortify Magicka",
            "Fortify Magicka Regen",
            "Waterbreathing",
        ]

    @staticmethod
    def enchantment_effects_apparel_neck() -> List[str]:
        return [
            "Fortify Alchemy",
            "Fortify Alteration",
            "Fortify Archery",
            "Fortify Barter",
            "Fortify Block",
            "Fortify Conjuration",
            "Fortify Destruction",
            "Fortify Heavy Armor",
            "Fortify Illusion",
            "Fortify Light Armor",
            "Fortify Lockpicking",
            "Fortify One-Handed",
            "Fortify Pickpocket",
            "Fortify Restoration",
            "Fortify Smithing",
            "Fortify Sneak",
            "Fortify Two-Handed",
            "Fortify Healing Rate",
            "Fortify Health",
            "Fortify Magicka",
            "Fortify Stamina",
            "Fortify Stamina Regen",
            "Fortify Carry Weight",
            "Resist Disease",
            "Resist Fire",
            "Resist Frost",
            "Resist Magic",
            "Resist Poison",
            "Resist Shock",
            "Waterbreathing",
        ]

    @staticmethod
    def enchantment_effects_apparel_chest() -> List[str]:
        return [
            "Fortify Alteration",
            "Fortify Conjuration",
            "Fortify Destruction",
            "Fortify Heavy Armor",
            "Fortify Illusion",
            "Fortify Light Armor",
            "Fortify Restoration",
            "Fortify Smithing",
            "Fortify Healing Rate",
            "Fortify Health",
            "Fortify Magicka Regen",
            "Fortify Stamina",
            "Fortify Stamina Regen",
            "Fortify Alteration & Magicka Regen",
            "Fortify Conjuration & Magicka Regen",
            "Fortify Destruction & Magicka Regen",
            "Fortify Illusion & Magicka Regen",
            "Fortify Restoration & Magicka Regen",
            "Resist Disease",
            "Resist Poison",
        ]

    @staticmethod
    def enchantment_effects_apparel_hands() -> List[str]:
        return [
            "Fortify Alchemy",
            "Fortify Archery",
            "Fortify Block",
            "Fortify Heavy Armor",
            "Fortify Light Armor",
            "Fortify Lockpicking",
            "Fortify One-Handed",
            "Fortify Pickpocket",
            "Fortify Smithing",
            "Fortify Sneak",
            "Fortify Two-Handed",
            "Fortify Magicka",
            "Fortify Carry Weight",
            "Fortify Unarmed",
        ]

    @staticmethod
    def enchantment_effects_apparel_finger() -> List[str]:
        return [
            "Fortify Alchemy",
            "Fortify Alteration",
            "Fortify Archery",
            "Fortify Block",
            "Fortify Conjuration",
            "Fortify Destruction",
            "Fortify Heavy Armor",
            "Fortify Illusion",
            "Fortify Light Armor",
            "Fortify Lockpicking",
            "Fortify One-Handed",
            "Fortify Pickpocket",
            "Fortify Restoration",
            "Fortify Smithing",
            "Fortify Sneak",
            "Fortify Two-Handed",
            "Fortify Healing Rate",
            "Fortify Health",
            "Fortify Magicka",
            "Fortify Magicka Regen",
            "Fortify Stamina",
            "Fortify Stamina Regen",
            "Fortify Carry Weight",
            "Fortify Unarmed",
            "Resist Disease",
            "Resist Fire",
            "Resist Frost",
            "Resist Magic",
            "Resist Poison",
            "Resist Shock",
            "Waterbreathing",
        ]

    @staticmethod
    def enchantment_effects_apparel_feet() -> List[str]:
        return [
            "Fortify One-Handed",
            "Fortify Pickpocket",
            "Fortify Sneak",
            "Fortify Two-Handed",
            "Fortify Stamina",
            "Fortify Stamina Regen",
            "Fortify Carry Weight",
            "Resist Fire",
            "Resist Frost",
            "Resist Shock",
            "Muffle",
        ]

    @staticmethod
    def enchantment_effects_apparel_shield() -> List[str]:
        return [
            "Fortify Block",
            "Fortify Health",
            "Resist Disease",
            "Resist Fire",
            "Resist Frost",
            "Resist Magic",
            "Resist Poison",
            "Resist Shock",
        ]

    @staticmethod
    def enchantment_effects_weapons() -> List[str]:
        return [
            "Absorb Health",
            "Absorb Magicka",
            "Absorb Stamina",
            "Chaos Damage",
            "Fire Damage",
            "Frost Damage",
            "Magicka Damage",
            "Shock Damage",
            "Stamina Damage",
            "Banish",
            "Fear",
            "Turn Undead",
            "Paralyze",
            "Soul Trap",
        ]

    @staticmethod
    def enchantment_effects_disenchantment() -> List[str]:
        return [
            "Fortify Alchemy",
            "Fortify Alteration",
            "Fortify Archery",
            "Fortify Barter",
            "Fortify Block",
            "Fortify Conjuration",
            "Fortify Destruction",
            "Fortify Heavy Armor",
            "Fortify Illusion",
            "Fortify Light Armor",
            "Fortify Lockpicking",
            "Fortify One-Handed",
            "Fortify Pickpocket",
            "Fortify Restoration",
            "Fortify Smithing",
            "Fortify Sneak",
            "Fortify Two-Handed",
            "Fortify Healing Rate",
            "Fortify Health",
            "Fortify Magicka",
            "Fortify Magicka Regen",
            "Fortify Stamina",
            "Fortify Stamina Regen",
            "Fortify Carry Weight",
            "Fortify Alteration & Magicka Regen",
            "Fortify Conjuration & Magicka Regen",
            "Fortify Destruction & Magicka Regen",
            "Fortify Illusion & Magicka Regen",
            "Fortify Restoration & Magicka Regen",
            "Fortify Unarmed",
            "Resist Disease",
            "Resist Fire",
            "Resist Frost",
            "Resist Magic",
            "Resist Poison",
            "Resist Shock",
            "Muffle",
            "Waterbreathing",
            "Absorb Health",
            "Absorb Magicka",
            "Absorb Stamina",
            "Chaos Damage",
            "Fire Damage",
            "Frost Damage",
            "Magicka Damage",
            "Shock Damage",
            "Stamina Damage",
            "Banish",
            "Fear",
            "Turn Undead",
            "Paralyze",
            "Soul Trap",
        ]

    @staticmethod
    def soul_trap_souls() -> List[str]:
        return [
            "Alpha Wolf (Petty)",
            "Chicken (Petty)",
            "Corrupted Shade (Petty)",
            "Cow (Petty)",
            "Deer (Petty)",
            "Dog (Petty)",
            "Draugr Thrall (Petty)",
            "Draugr (Petty)",
            "Elk (Petty)",
            "Fox (Petty)",
            "Frostbite Spider (Petty)",
            "Goat (Petty)",
            "Horker (Petty)",
            "Mudcrab (Petty)",
            "Rabbit (Petty)",
            "Skeever (Petty)",
            "Skeleton (Petty)",
            "Slaughterfish (Petty)",
            "Snow Fox (Petty)",
            "Wisp (Petty)",
            "Wolf (Petty)",
            "Ash Hopper (Lesser)",
            "Bear (Lesser)",
            "Bristleback (Lesser)",
            "Chaurus (Lesser)",
            "Death Hound (Lesser)",
            "Draugr Overlord (Lesser)",
            "Draugr Restless (Lesser)",
            "Draugr Wight (Lesser)",
            "Falmer Skulker (Lesser)",
            "Falmer (Lesser)",
            "Flame Atronach (Lesser)",
            "Frostbite Spider (Lesser)",
            "Gargoyle (Lesser)",
            "Giant Frostbite Spider (Lesser)",
            "Horse (Lesser)",
            "Ice Wolf (Lesser)",
            "Ice Wraith (Lesser)",
            "Pit Wolf (Lesser)",
            "Restless Draugr (Lesser)",
            "Riekling (Lesser)",
            "Riekling Scout (Lesser)",
            "Sabre Cat (Lesser)",
            "Shade (Lesser)",
            "Snowy Sabre Cat (Lesser)",
            "Spriggan (Lesser)",
            "Troll (Lesser)",
            "Venomfang Skeever (Lesser)",
            "Werewolf (Lesser)",
            "Wounded Frostbite Spider (Lesser)",
            "Ash Spawn (Common)",
            "Cave Bear (Common)",
            "Chaurus Reaper (Common)",
            "Curalmil (Common)",
            "Draugr Deathlord (Common)",
            "Draugr Scourge Lord (Common)",
            "Draugr Scourge (Common)",
            "Falmer Shadowmaster (Common)",
            "Frost Atronach (Common)",
            "Frost Troll (Common)",
            "Hagraven (Common)",
            "Hulking Draugr (Common)",
            "King Olaf One-Eye (Common)",
            "Mikrul Gauldurson (Common)",
            "Mounted Riekling (Common)",
            "Netch Calf (Common)",
            "Potema's Remains (Common)",
            "Riekling Chief (Common)",
            "Riekling Hunter (Common)",
            "Riekling Rider (Common)",
            "Riekling Warrior (Common)",
            "Sigdis Gauldurson (Common)",
            "Snow Bear (Common)",
            "Spriggan Matron (Common)",
            "Udefrykte (Common)",
            "Werebear (Common)",
            "Ash Spawn Skirmisher (Greater)",
            "Burnt Spriggan (Greater)",
            "Bull Netch (Greater)",
            "Chaurus Hunter (Greater)",
            "Draugr Death Overlord (Greater)",
            "Draugr Deathlord (Greater)",
            "Falmer Warmonger (Greater)",
            "Giant (Greater)",
            "King Olaf One-Eye (Greater)",
            "Riekling Courser (Greater)",
            "Spriggan Earth Mother (Greater)",
            "Storm Atronach (Greater)",
            "The Pale Lady (Greater)",
            "Wispmother (Greater)",
            "Falmer Nightprowler (Greater)",
            "Ash Spawn Immolator (Grand)",
            "Betty Netch (Grand)",
            "Dragon Priest (Grand)",
            "Draugr Death Overlord (Grand)",
            "Draugr Deathlord (Grand)",
            "Falmer Shadowmaster (Grand)",
            "Falmer Warmonger (Grand)",
            "Frost Giant (Grand)",
            "King Olaf One-Eye (Grand)",
            "Mammoth (Grand)",
            "Potema's Remains (Grand)",
            "Riekling Charger (Grand)",
            "NPC (Black)",
        ]

    @functools.cached_property
    def enchanted_staves_base(self) -> List[str]:
        return [
            "Staff of Magelight",
            "Staff of Paralysis",
            "Staff of Banishing",
            "Staff of Daedric Command",
            "Staff of Dread Zombies",
            "Staff of Expulsion",
            "Staff of Reanimation",
            "Staff of Revenants",
            "Staff of Soul Trapping",
            "Staff of Zombies",
            "Staff of the Familiar",
            "Staff of the Flame Atronach",
            "Staff of the Frost Atronach",
            "Staff of the Storm Atronach",
            "Staff of Chain Lightning",
            "Staff of Fireballs",
            "Staff of Firebolts",
            "Staff of Flames",
            "Staff of Frostbite",
            "Staff of Ice Spikes",
            "Staff of Ice Storms",
            "Staff of Icy Spear",
            "Staff of Incineration",
            "Staff of Lightning Bolts",
            "Staff of Sparks",
            "Staff of Thunderbolts",
            "Staff of the Flame Wall",
            "Staff of the Frost Wall",
            "Staff of the Storm Wall",
            "Staff of Calm",
            "Staff of Courage",
            "Staff of Fear",
            "Staff of Frenzy",
            "Staff of Fury",
            "Staff of Inspiration",
            "Staff of Vanquishment",
            "Grand Staff of Repulsion",
            "Grand Staff of Turning",
            "Minor Staff of Turning",
            "Staff of Mending",
            "Staff of Repulsion",
            "Staff of Turning",
            "Staff of the Healing Hand",
        ]

    @functools.cached_property
    def enchanted_staves_anniversary(self) -> List[str]:
        return [
            "Arm of the Moon",
            "Arm of the Sun",
            "Staff of Sheogorath",
        ]

    def enchanted_staves(self) -> List[str]:
        enchanted_staves: List[str] = self.enchanted_staves_base[:]

        if self.has_anniversary_upgrade:
            enchanted_staves.extend(self.enchanted_staves_anniversary)

        return sorted(enchanted_staves)

    @staticmethod
    def smithing_craft_count_range() -> range:
        return range(2, 7)

    @functools.cached_property
    def smithing_crafting_categories_base(self) -> List[str]:
        return [
            "Hide Armor",
            "Studded Armor",
            "Leather Armor",
            "Iron Armor",
            "Banded Iron Armor",
            "Bone Hawk Amulet",
            "Gold Jewelry",
            "Silver Jewelry",
            "Iron Weapons",
            "Imperial Armor",
            "Steel Armor",
            "Steel Weapons",
            "Elven Armor",
            "Elven Gilded Armor",
            "Elven Weapons",
            "Scaled Armor",
            "Steel Plate Armor",
            "Glass Armor",
            "Glass Weapons",
            "Dwarven Armor",
            "Dwarven Weapons",
            "Orcish Armor",
            "Orcish Weapons",
            "Ebony Armor",
            "Ebony Weapons",
            "Daedric Armor",
            "Daedric Weapons",
            "Dragonscale Armor",
            "Dragonplate Armor",
            "Dragonbone Weapons",
            "Ancient Nord Armor",
            "Nord Hero Weapons",
            "Housebuilding Materials",
            "Bonemold Armor",
            "Improved Bonemold Armor",
            "Chitin Armor",
            "Nordic Carved Armor",
            "Nordic Weapons",
            "Stalhrim Armor",
            "Stalhrim Weapons",
            "Shellbug Helmet",
            "Corkbulb Ammunition",
            "Bonemold Ammunition",
            "Amber Armor",
            "Amber Weapons",
            "Madness Armor",
            "Madness Weapons",
            "Dark Armor",
            "Dark Weapons",
            "Golden Armor",
            "Golden Weapons",
            "Fishing Rods",
        ]

    @functools.cached_property
    def smithing_crafting_categories_anniversary(self) -> List[str]:
        return [
            "Arcane Arrows",
            "Bone Arrows",
            "Telekinesis Arrows",
            "Soul Stealer Arrows",
            "Soul Gem Arrowhead",
            "Backpacks",
            "Camping Supplies",
            "Nordic Jewelry",
            "Animal Accessories",
            "Vigil Armor",
            "Spell Knight Armor",
            "Netch Leather Armor",
            "Silver Armor",
            "Indoril Armor",
            "Her Hand Armor",
            "Remnant Armor",
            "Remnant Weapons",
        ]

    def smithing_crafting_categories(self) -> List[str]:
        smithing_crafting_categories: List[str] = self.smithing_crafting_categories_base[:]

        if self.has_anniversary_upgrade:
            smithing_crafting_categories.extend(self.smithing_crafting_categories_anniversary)

        return sorted(smithing_crafting_categories)

    @staticmethod
    def smithing_qualities() -> List[str]:
        return [
            "Fine",
            "Superior",
            "Exquisite",
            "Flawless",
            "Epic",
            "Legendary",
        ]

    @functools.cached_property
    def smithing_weapon_categories_base(self) -> List[str]:
        return [
            "Iron Weapons",
            "Steel Weapons",
            "Elven Weapons",
            "Glass Weapons",
            "Dwarven Weapons",
            "Orcish Weapons",
            "Ebony Weapons",
            "Daedric Weapons",
            "Dragonbone Weapons",
            "Nord Hero Weapons",
            "Nordic Weapons",
            "Stalhrim Weapons",
            "Amber Weapons",
            "Madness Weapons",
            "Dark Weapons",
            "Golden Weapons",
        ]

    @functools.cached_property
    def smithing_weapon_categories_anniversary(self) -> List[str]:
        return [
            "Remnant Weapons",
        ]

    def smithing_weapon_categories(self) -> List[str]:
        smithing_weapon_categories: List[str] = self.smithing_weapon_categories_base[:]

        if self.has_anniversary_upgrade:
            smithing_weapon_categories.extend(self.smithing_weapon_categories_anniversary)

        return sorted(smithing_weapon_categories)

    @functools.cached_property
    def smithing_armor_categories_base(self) -> List[str]:
        return [
            "Hide Armor",
            "Studded Armor",
            "Leather Armor",
            "Iron Armor",
            "Banded Iron Armor",
            "Imperial Armor",
            "Steel Armor",
            "Elven Armor",
            "Elven Gilded Armor",
            "Scaled Armor",
            "Steel Plate Armor",
            "Glass Armor",
            "Dwarven Armor",
            "Orcish Armor",
            "Ebony Armor",
            "Daedric Armor",
            "Dragonscale Armor",
            "Dragonplate Armor",
            "Ancient Nord Armor",
            "Bonemold Armor",
            "Improved Bonemold Armor",
            "Chitin Armor",
            "Nordic Carved Armor",
            "Stalhrim Armor",
            "Shellbug Helmet",
            "Amber Armor",
            "Madness Armor",
            "Dark Armor",
            "Golden Armor",
        ]

    @functools.cached_property
    def smithing_armor_categories_anniversary(self) -> List[str]:
        return [
            "Vigil Armor",
            "Spell Knight Armor",
            "Netch Leather Armor",
            "Silver Armor",
            "Indoril Armor",
            "Her Hand Armor",
            "Remnant Armor",
        ]

    def smithing_armor_categories(self) -> List[str]:
        smithing_armor_categories: List[str] = self.smithing_armor_categories_base[:]

        if self.has_anniversary_upgrade:
            smithing_armor_categories.extend(self.smithing_armor_categories_anniversary)

        return sorted(smithing_armor_categories)

    @functools.cached_property
    def atronach_forge_outcomes_base(self) -> List[str]:
        return [
            "Flame Atronach",
            "Frost Atronach",
            "Storm Atronach",
            "Dremora",
            "Daedra Heart",
            "Staff of the Flame Atronach",
            "Staff of the Frost Atronach",
            "Staff of the Storm Atronach",
            "Spell Tome: Conjure Flame Atronach",
            "Spell Tome: Conjure Frost Atronach",
            "Spell Tome: Conjure Storm Atronach",
            "Spell Tome: Soul Trap",
            "Scroll of Conjure Flame Atronach",
            "Scroll of Conjure Frost Atronach",
            "Scroll of Conjure Storm Atronach",
            "Conjurer's Elixir",
            "Fire Salts",
            "Frost Salts",
            "Void Salts",
            "Random Daedric Enchanted Weapon",
            "Random Daedric Enchanted Armor",
            "Daedric Bow",
            "Daedric Mace",
            "Daedric Dagger",
            "Daedric Greatsword",
            "Daedric Sword",
            "Daedric Warhammer",
            "Daedric War Axe",
            "Daedric Battleaxe",
            "Daedric Shield",
            "Daedric Boots",
            "Daedric Gauntlets",
            "Daedric Armor",
            "Daedric Helmet",
            "Spell Tome: Conjure Staada",
            "Scroll of Conjure Staada",
            "Staada",
            "Spell Tome: Conjure Golden Saint Archer",
            "Spell Tome: Conjure Golden Saint Warrior",
            "Scroll of Conjure Golden Saint Archer",
            "Scroll of Conjure Golden Saint Warrior",
            "Golden Saint Archer",
            "Golden Saint Warrior",
            "Spell Tome: Conjure Dark Seducer Archer",
            "Spell Tome: Conjure Dark Seducer Warrior",
            "Scroll of Conjure Dark Seducer Archer",
            "Scroll of Conjure Dark Seducer Warrior",
            "Dark Seducer Archer",
            "Dark Seducer Warrior",
        ]

    @functools.cached_property
    def atronach_forge_outcomes_anniversary(self) -> List[str]:
        return [
            "Spell Tome: Conjure Ayleid Lich",
        ]

    def atronach_forge_outcomes(self) -> List[str]:
        atronach_forge_outcomes: List[str] = self.atronach_forge_outcomes_base[:]

        if self.has_anniversary_upgrade:
            atronach_forge_outcomes.extend(self.atronach_forge_outcomes_anniversary)

        return sorted(atronach_forge_outcomes)

    @staticmethod
    def baking_count_range() -> range:
        return range(2, 13)

    @staticmethod
    def baking_goods() -> List[str]:
        return [
            "Apple Dumpling",
            "Apple Pie",
            "Braided Bread",
            "Bread",
            "Chicken Dumpling",
            "Garlic Bread",
            "Jazbay Crostata",
            "Juniper Berry Crostata",
            "Lavender Dumpling",
            "Potato Bread",
            "Snowberry Crostata",
            "Sweet Roll",
        ]

    @staticmethod
    def baking_ingredient_count_range() -> range:
        return range(3, 10)

    @staticmethod
    def baking_ingredients() -> List[str]:
        return [
            "Sack of Flour",
            "Green Apple",
            "Red Apple",
            "Salt Pile",
            "Butter",
            "Chicken's Egg",
            "Jug of Milk",
            "Chicken Breast",
            "Garlic",
            "Leek",
            "Jazbay Grapes",
            "Juniper Berries",
            "Moon Sugar",
            "Snowberries",
            "Lavender",
            "Potato",
        ]

    @staticmethod
    def construtible_houses() -> List[str]:
        return [
            "Lakeview Manor",
            "Windstad Manor",
            "Heljarchen Hall",
        ]

    @staticmethod
    def construtible_house_features() -> List[str]:
        return [
            "Cellar",
            "Aquarium",
            "Armory",
            "Kitchen",
            "Library",
            "Alchemy Laboratory",
            "Storage Room",
            "Trophy Room",
            "Bedrooms",
            "Enchanter's Tower",
            "Greenhouse",
        ]

    @staticmethod
    def cooking_count_range() -> range:
        return range(2, 13)

    @staticmethod
    def cooking_foods() -> List[str]:
        return [
            "Apple Cabbage Stew",
            "Beef Stew",
            "Cabbage Potato Soup",
            "Clam Chowder",
            "Cooked Angelfish",
            "Cooked Angler",
            "Cooked Angler Larvae",
            "Cooked Arctic Char",
            "Cooked Arctic Grayling",
            "Cooked Beef",
            "Cooked Boar Meat",
            "Cooked Brook Bass",
            "Cooked Carp",
            "Cooked Catfish",
            "Cooked Cod",
            "Cooked Direfish",
            "Cooked Glass Catfish",
            "Cooked Glassfish",
            "Cooked Goldfish",
            "Cooked Juvenile Mudcrab",
            "Cooked Lyretail Anthias",
            "Cooked Pearlfish",
            "Cooked Pogfish",
            "Cooked Pygmy Sunfish",
            "Cooked Scorpion Fish",
            "Cooked Spadefish",
            "Cooked Tripod Spiderfish",
            "Cooked Vampire Fish",
            "Crab Stew",
            "Creamy Crab Bisque",
            "Elsweyr Fondue",
            "Grilled Chicken Breast",
            "Horker and Ash Yam Stew",
            "Horker Loaf",
            "Horker Stew",
            "Horse Haunch",
            "Leg of Goat Roast",
            "Mammoth Steak",
            "Pheasant Roast",
            "Potato Crab Chowder",
            "Potato Soup",
            "Rabbit Haunch",
            "Roasted Tomato Crab Bisque",
            "Salmon Steak",
            "Steamed Mudcrab Legs",
            "Tomato Soup",
            "Vegetable Soup",
            "Venison Chop",
            "Venison Stew",
            "Hot Apple Cabbage Stew",
            "Hot Beef Stew",
            "Hot Cabbage Potato Soup",
            "Hot Cabbage Soup",
            "Hot Clam Chowder",
            "Hot Crab Stew",
            "Hot Creamy Crab Bisque",
            "Hot Elsweyr Fondue",
            "Hot Horker and Ash Yam Stew",
            "Hot Horker Stew",
            "Hot Potato Crab Chowder",
            "Hot Potato Soup",
            "Hot Roasted Tomato Crab Bisque",
            "Hot Tomato Soup",
            "Hot Vegetable Soup",
            "Hot Venison Stew",
        ]

    @staticmethod
    def cooking_ingredient_count_range() -> range:
        return range(3, 10)

    @staticmethod
    def cooking_ingredients() -> List[str]:
        return [
            "Potato",
            "Leek",
            "Fire Salts",
            "Tomato",
            "Cabbage",
            "Garlic",
            "Crab Meat",
            "Butter",
            "Jug of Milk",
            "Lavender",
            "Ash Yam",
            "Moon Sugar",
            "Eidar Cheese Wheel",
            "Ale",
            "Sack of Flour",
            "Clam Meat",
            "Carrot",
            "Red Apple",
            "Mudcrab Legs",
        ]


# Archipelago Options
class TheElderScrollsVSkyrimSpecialEditionDLCOwned(OptionSet):
    """
    Indicates which The Elder Scrolls V: Skyrim - Special Edition DLC the player owns, if any.
    """

    display_name = "The Elder Scrolls V: Skyrim - Special Edition DLC Owned"
    valid_keys = [
        "Anniversary Upgrade",
    ]

    default = valid_keys

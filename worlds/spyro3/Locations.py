from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import Spyro3Item

class Spyro3LocationCategory(IntEnum):
    EGG = 0,
    SKIP = 1,
    EVENT = 2,
    GEM = 3,
    SKILLPOINT = 4,


class Spyro3LocationData(NamedTuple):
    name: str
    default_item: str
    category: Spyro3LocationCategory


class Spyro3Location(Location):
    game: str = "Spyro 3"
    category: Spyro3LocationCategory
    default_item_name: str

    def __init__(
            self,
            player: int,
            name: str,
            category: Spyro3LocationCategory,
            default_item_name: str,
            address: Optional[int] = None,
            parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category
        self.name = name

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 1230000
        table_offset = 1000

        table_order = [
            "Sunrise Spring","Sunny Villa","Cloud Spires","Molten Crater","Seashell Shore","Mushroom Speedway","Sheila's Alp", "Buzz", "Crawdad Farm",
            "Midday Gardens","Icy Peak","Enchanted Towers","Spooky Swamp","Bamboo Terrace","Country Speedway","Sgt. Byrd's Base","Spike","Spider Town",
            "Evening Lake","Frozen Altars","Lost Fleet","Fireworks Factory","Charmed Ridge","Honey Speedway","Bentley's Outpost","Scorch","Starfish Reef",
            "Midnight Mountain","Crystal Islands","Desert Ruins","Haunted Tomb","Dino Mines","Harbor Speedway","Agent 9's Lab","Sorceress","Bugbot Factory","Super Bonus Round"
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(location_tables[region_name]), table_offset, i))

            output.update({location_data.name: id for id, location_data in enumerate(location_tables[region_name], base_id + (table_offset * i))})

        return output

    def place_locked_item(self, item: Spyro3Item):
        self.item = item
        self.locked = True
        item.location = self

location_tables = {
#Homeworld 1
"Sunrise Spring": [
    Spyro3LocationData(f"Sunrise Spring Home: Learn gliding. (Coltrane)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sunrise Spring Home: Egg by the stream. (Isabelle)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sunrise Spring Home: Fly through the cave. (Ami)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sunrise Spring Home: Bottom of the lake. (Bruce)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sunrise Spring Home: Head bash the rock. (Liam)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sunrise Spring: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
"Sunny Villa": [
    Spyro3LocationData(f"Sunny Villa: Rescue the mayor. (Sanders)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sunny Villa: Hop to Rapunzel. (Lucy)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sunny Villa: Lizard skating I. (Emily)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sunny Villa: Lizard skating II. (Daisy)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sunny Villa: Egg by the building. (Vanessa)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sunny Villa: Glide to the spring. (Miles)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Sunny Villa Complete", "Sunny Villa Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData("Sunny Villa: All Gems", "Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Sunny Villa: Flame all trees (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
    Spyro3LocationData(f"Sunny Villa: Skateboard course record I (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Cloud Spires": [
    Spyro3LocationData(f"Cloud Spires: Turn on the cloud generator. (Henry)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Cloud Spires: Plant the sun seeds. (LuLu)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Cloud Spires: Bell tower spirits. (Jake)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Cloud Spires: Bell tower thief. (Bryan)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Cloud Spires: Run along the wall. (Stephanie)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Cloud Spires: Glide to the island. (Clare)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Cloud Spires Complete", "Cloud Spires Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Cloud Spires: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
"Molten Crater": [
    Spyro3LocationData(f"Molten Crater: Get to the tiki lodge. (Curlie)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Molten Crater: Replace idol heads. (Ryan)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Molten Crater: Catch the thief. (Moira)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Molten Crater: Supercharge after the thief. (Kermitt)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Molten Crater: Sgt. Byrd blows up a wall. (Luna)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Molten Crater: Egg by lava river. (Rikki)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Molten Crater Complete", "Molten Crater Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Molten Crater: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Molten Crater: Assemble tiki heads (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
    Spyro3LocationData(f"Molten Crater: Supercharge the wall (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Seashell Shore": [
    Spyro3LocationData(f"Seashell Shore: Free the seals. (Dizzy)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Seashell Shore: Under the docks. (Jason)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Seashell Shore: Destroy the sand castle. (Mollie)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Seashell Shore: Defeat the shark sub. (Jackie)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Seashell Shore: Clear out the pipe. (Duke)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Seashell Shore: Hop to the secret cave. (Jared)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Seashell Shore Complete", "Seashell Shore Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Seashell Shore: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Seashell Shore: Catch the funky chicken (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Mushroom Speedway": [
    Spyro3LocationData(f"Mushroom Speedway: Time attack. (Sabina)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Mushroom Speedway: Race the butterflies. (John)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Mushroom Speedway: Hunter's dogfight. (Tater)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Mushroom Speedway: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
"Sheila's Alp": [
    Spyro3LocationData(f"Sheila's Alp: Help Bobby get home. (Nan)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sheila's Alp: Help Pete get home. (Jenny)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sheila's Alp: Help Billy get home. (Ruby)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Sheila's Alp Complete", "Sheila's Alp Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Sheila's Alp: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
"Buzz": [
    Spyro3LocationData(f"Buzz's Dungeon: Defeat Buzz. (Grayson)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Buzz Defeated", "Buzz Defeated", Spyro3LocationCategory.EVENT)
],
"Crawdad Farm": [
    Spyro3LocationData(f"Crawdad Farm: Take Sparx to the farm. (Nora)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Crawdad Farm Complete", "Crawdad Farm Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Crawdad Farm: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
#Homeworld 2
"Midday Gardens": [
    Spyro3LocationData(f"Midday Gardens Home: Underwater egg. (Dave)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Midday Gardens Home: Secret ice cave. (Mingus)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Midday Gardens Home: Catch the thief. (Trixie)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Midday Gardens Home: Superflame the flowerpots. (Matt)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Midday Gardens Home: Climb to the ledge. (Modesty)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Midday Gardens: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
"Icy Peak": [
    Spyro3LocationData(f"Icy Peak: Find Doug the polar bear. (Chet)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Icy Peak: Protect Nancy the skater. (Cerny)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Icy Peak: Speedy thieves I. (Betty)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Icy Peak: Speedy thieves II. (Scout)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Icy Peak: On top of a ledge. (Maynard)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Icy Peak: Glide to the sky island. (Reez)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Icy Peak Complete", "Icy Peak Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Icy Peak: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Icy Peak: Glide to pedestal (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Enchanted Towers": [
    Spyro3LocationData(f"Enchanted Towers: Destroy the sorceress statue. (Peanut)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Enchanted Towers: Rescue the lost wolf. (Lys)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Enchanted Towers: Collect the bones. (Ralph)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Enchanted Towers: Trick skater I. (Caroline)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Enchanted Towers: Trick skater II. (Alex)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Enchanted Towers: Glide to the small island. (Gladys)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Enchanted Towers Complete", "Enchanted Towers Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Enchanted Towers: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Enchanted Towers: Skateboard course record II (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Spooky Swamp": [
    Spyro3LocationData(f"Spooky Swamp: Find Shiny the firefly. (Thelonious)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Spooky Swamp: Jump to the island. (Michael)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Spooky Swamp: Across the treetops. (Frank)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Spooky Swamp: Escort the twins I. (Peggy)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Spooky Swamp: Escort the twins II. (Michele)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Spooky Swamp: Defeat sleepy head. (Herbi)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Spooky Swamp Complete", "Spooky Swamp Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Spooky Swamp: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Spooky Swamp: Destroy all piranha signs (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Bamboo Terrace": [
    Spyro3LocationData(f"Bamboo Terrace: Clear the pandas' path. (Tom)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Bamboo Terrace: Shoot from the boat. (Rusty)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Bamboo Terrace: Smash to the mountain top. (Brubeck)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Bamboo Terrace: Glide to the hidden cave. (Madison)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Bamboo Terrace: Glide to the small island. (Dwight)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Bamboo Terrace: Catch the thief. (Pee-wee)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Bamboo Terrace Complete", "Bamboo Terrace Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Bamboo Terrace: All Gems", f"Filler", Spyro3LocationCategory.GEM),
],
"Country Speedway": [
    Spyro3LocationData(f"Country Speedway: Time attack. (Gavin)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Country Speedway: Race the pigs. (Shemp)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Country Speedway: Hunter's rescue mission. (Roberto)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Country Speedway: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
"Sgt. Byrd's Base": [
    Spyro3LocationData(f"Sgt. Byrd's Base: Clear the building. (RyanLee)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sgt. Byrd's Base: Clear the caves. (Sigfried)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Sgt. Byrd's Base: Rescue 5 hummingbirds. (Roy)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Sgt. Byrd's Base Complete", "Sgt. Byrd's Base Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Sgt. Byrd's Base: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Sgt. Byrd's Base: Bomb the gophers (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Spike": [
    Spyro3LocationData(f"Spike's Arena: Defeat Spike. (Monique)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Spike Defeated", "Spike Defeated", Spyro3LocationCategory.EVENT)
],
"Spider Town": [
    Spyro3LocationData(f"Spider Town: Go to town. (Tootie)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Spider Town Complete", "Spider Town Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Spider Town: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
#Homeworld 3
"Evening Lake": [
    Spyro3LocationData(f"Evening Lake Home: On the bridge (Ted)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Evening Lake Home: Glide to the tower. (Hannah)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Evening Lake Home: Break the tower wall. (Stooby)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Evening Lake Home: Belly of the whale. (Jonah)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Evening Lake Home: I'm invincible! (Stuart)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Evening Lake: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
"Frozen Altars": [
    Spyro3LocationData(f"Frozen Altars: Melt the snowmen. (Jana)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Frozen Altars: Box the yeti. (Aly)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Frozen Altars: Box the yeti again! (Ricco)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Frozen Altars: Catch the ice cats. (Ba'ah)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Frozen Altars: Glide from the temple roof. (Cecil)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Frozen Altars: Across the rooftops. (Jasper)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Frozen Altars Complete", "Frozen Altars Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Frozen Altars: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Frozen Altars: Beat yeti in two rounds (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Lost Fleet": [
    Spyro3LocationData(f"Lost Fleet: Find Crazy Ed's treasure. (Craig)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Lost Fleet: Sink the subs I. (Ethel)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Lost Fleet: Sink the subs II. (Dolores)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Lost Fleet: Swim through acid. (Chad)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Lost Fleet: Skate race the rhynocs. (Oliver)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Lost Fleet: Skate race Hunter. (Aiden)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Lost Fleet Complete", "Lost Fleet Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Lost Fleet: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Lost Fleet: Skateboard record time (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Fireworks Factory": [
    Spyro3LocationData(f"Fireworks Factory: Destwoy the wocket! (Grady)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Fireworks Factory: You're doomed! (Patty)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Fireworks Factory: You're still doomed! (Donovan)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Fireworks Factory: Ninja HQ (Sam)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Fireworks Factory: Bad dragon! (Evan)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Fireworks Factory: Hidden in an alcove. (Noodles)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Fireworks Factory Complete", "Fireworks Factory Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Fireworks Factory: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Fireworks Factory: Find Agent 9's powerup (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Charmed Ridge": [
    Spyro3LocationData(f"Charmed Ridge: Rescue the Fairy Princess. (Sakura)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Charmed Ridge: Glide to the tower. (Moe)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Charmed Ridge: Egg in the cave. (Benjamin)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Charmed Ridge: Cat witch chaos. (Abby)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Charmed Ridge: Jack and the beanstalk I. (Shelley)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Charmed Ridge: Jack and the beanstalk II. (Chuck)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Charmed Ridge Complete", "Charmed Ridge Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Charmed Ridge: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Charmed Ridge: The Impossible Tower (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
    Spyro3LocationData(f"Charmed Ridge: Shoot the temple windows (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Honey Speedway": [
    Spyro3LocationData(f"Honey Speedway: Time attack. (Chris)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Honey Speedway: Race the bees (Henri)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Honey Speedway: Hunter's narrow escape. (Nori)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Honey Speedway: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
"Bentley's Outpost": [
    Spyro3LocationData(f"Bentley's Outpost: Help Bartholomew home. (Eric)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Bentley's Outpost: The Gong Show (Brian)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Bentley's Outpost: Snowball's chance. (Charlie)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Bentley's Outpost Complete", "Bentley's Outpost Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Bentley's Outpost: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Bentley's Outpost: Push box off the cliff (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Scorch": [
    Spyro3LocationData(f"Scorch's Pit: Defeat Scorch. (James)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Scorch Defeated", "Scorch Defeated", Spyro3LocationCategory.EVENT)
],
"Starfish Reef": [
    Spyro3LocationData(f"Starfish Reef: Beach party! (Ahnashawn)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Starfish Reef Complete", "Starfish Reef Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Starfish Reef: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
#Homeworld 4
"Midnight Mountain": [
    Spyro3LocationData(f"Midnight Mountain Home: Shhh, it's a secret (Billy)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Midnight Mountain Home: At the top of the waterfall. (Evie)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Midnight Mountain Home: Catch the thief. (Maiken)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Midnight Mountain Home: Glide to the island. (Saki)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Midnight Mountain Home: Stomp the floor. (Buddy)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Midnight Mountain Home: Egg for sale. (Al)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Midnight Mountain Home: Moneybags Chase Complete", "Moneybags Chase Complete",Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Midnight Mountain: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
"Crystal Islands": [
    Spyro3LocationData(f"Crystal Islands: Reach the crystal tower. (Lloyd)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Crystal Islands: Ride the slide. (Elloise)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Crystal Islands: Whack a mole. (Hank)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Crystal Islands: Fly to the hidden egg. (Grace)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Crystal Islands: Glide to the island. (Manie)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Crystal Islands: Catch the flying thief. (Max)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Crystal Islands Complete", "Crystal Islands Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Crystal Islands: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
"Desert Ruins": [
    Spyro3LocationData(f"Desert Ruins: Raid the tomb. (Marty)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Desert Ruins: Shark shootin'. (Sadie)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Desert Ruins: Krash Kangaroo I. (Lester)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Desert Ruins: Krash Kangaroo II. (Pete)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Desert Ruins: Sink or singe. (Nelly)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Desert Ruins: Give me a hand (Andy)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Desert Ruins Complete", "Desert Ruins Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Desert Ruins: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Desert Ruins: Destroy all seaweed (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Haunted Tomb": [
    Spyro3LocationData(f"Haunted Tomb: Release the temple dweller. (Will)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Haunted Tomb: Snake slide. (Malcom)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Haunted Tomb: Tank blast I. (MJ)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Haunted Tomb: Tank blast II. (TJ)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Haunted Tomb: Clear the caves. (Roxy)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Haunted Tomb: Climb the wall. (Christine)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Haunted Tomb Complete", "Haunted Tomb Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Haunted Tomb: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Haunted Tomb: Swim into the dark hole (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Dino Mines": [
    Spyro3LocationData(f"Dino Mines: Jail break! (Kiki)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Dino Mines: Shafted! (Elliot)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Dino Mines: Swim through the wall. (Romey)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Dino Mines: Gunfight at the Jurassic Corral. (Sharon)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Dino Mines: Leap of faith. (Dan)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Dino Mines: Take it to the bank. (Sergio)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Dino Mines Complete", "Dino Mines Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Dino Mines: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Dino Mines: Hit all the seahorses (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
    Spyro3LocationData(f"Dino Mines: Hit the secret dino (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Harbor Speedway": [
    Spyro3LocationData(f"Harbor Speedway: Time attack. (Kobe)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Harbor Speedway: Race the blue footed boobies. (Jessie)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Harbor Speedway: Hunter's pursuit. (Sara)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Harbor Speedway: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
"Agent 9's Lab": [
    Spyro3LocationData(f"Agent 9's Lab: Blast and bomb the rhynocs. (Rowan)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Agent 9's Lab: Snipe the boats (Tony)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData(f"Agent 9's Lab: This place has gone to the birds. (Beulah)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Agent 9's Lab Complete", "Agent 9's Lab Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Agent 9's Lab: All Gems", f"Filler", Spyro3LocationCategory.GEM),
    Spyro3LocationData(f"Agent 9's Lab: Blow up all palm trees (Skill Point)", f"Filler", Spyro3LocationCategory.SKILLPOINT),
],
"Sorceress": [
    Spyro3LocationData(f"Sorceress's Lair: Defeat the Sorceress? (George)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Sorceress Defeated", "Sorceress Defeated", Spyro3LocationCategory.EVENT)
],
"Bugbot Factory": [
    Spyro3LocationData(f"Bugbot Factory: Shut down the factory. (Anabelle)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Bugbot Factory Complete", "Bugbot Factory Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Bugbot Factory: All Gems", f"Filler", Spyro3LocationCategory.GEM)
],
"Super Bonus Round": [
    Spyro3LocationData(f"Super Bonus Round: Woo, a secret egg. (Yin Yang)",f"Egg",Spyro3LocationCategory.EGG),
    Spyro3LocationData("Super Bonus Round Complete", "Super Bonus Round Complete", Spyro3LocationCategory.EVENT),
    Spyro3LocationData(f"Super Bonus Round: All Gems", f"Filler", Spyro3LocationCategory.GEM)
]

}

location_dictionary: Dict[str, Spyro3LocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})

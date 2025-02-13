from typing import TYPE_CHECKING, FrozenSet, List, Optional, Set, Union
from dataclasses import dataclass

from BaseClasses import CollectionState

from .options import LevelScaling
from .util import bound

if TYPE_CHECKING:
    from . import PokemonFRLGWorld


@dataclass
class ScalingData:
    name: str
    region: str
    type: Optional[str]
    connections: Optional[List[str]]
    data_ids: Union[str, List[str]]
    tags: FrozenSet


def create_scaling_data(world: "PokemonFRLGWorld"):
    if world.options.level_scaling == LevelScaling.option_off:
        return

    kanto_trainer_data = {
        "Professor Oak's Lab": [{"name": "Oak's Lab Rival",
                                 "data_ids": ["TRAINER_RIVAL_OAKS_LAB_BULBASAUR", "TRAINER_RIVAL_OAKS_LAB_CHARMANDER",
                                              "TRAINER_RIVAL_OAKS_LAB_SQUIRTLE"]}],
        "Route 22": [{"name": "Route 22 Early Rival",
                      "data_ids": ["TRAINER_RIVAL_ROUTE22_EARLY_BULBASAUR", "TRAINER_RIVAL_ROUTE22_EARLY_CHARMANDER",
                                   "TRAINER_RIVAL_ROUTE22_EARLY_SQUIRTLE"]},
                     {"name": "Route 22 Late Rival",
                      "data_ids": ["TRAINER_RIVAL_ROUTE22_LATE_BULBASAUR", "TRAINER_RIVAL_ROUTE22_LATE_CHARMANDER",
                                   "TRAINER_RIVAL_ROUTE22_LATE_SQUIRTLE"]}],
        "Viridian Forest": [{"name": "Bug Catcher Rick", "data_ids": ["TRAINER_BUG_CATCHER_RICK"]},
                            {"name": "Bug Catcher Doug", "data_ids": ["TRAINER_BUG_CATCHER_DOUG"]},
                            {"name": "Bug Catcher Anthony", "data_ids": ["TRAINER_BUG_CATCHER_ANTHONY"]},
                            {"name": "Bug Catcher Charlie", "data_ids": ["TRAINER_BUG_CATCHER_CHARLIE"]},
                            {"name": "Bug Catcher Sammy", "data_ids": ["TRAINER_BUG_CATCHER_SAMMY"]}],
        "Pewter Gym": [{"name": "Pewter Gym Trainers", "data_ids": ["TRAINER_CAMPER_LIAM", "TRAINER_LEADER_BROCK"]}],
        "Route 3": [{"name": "Lass Janice", "data_ids": ["TRAINER_LASS_JANICE"]},
                    {"name": "Bug Catcher Colton", "data_ids": ["TRAINER_BUG_CATCHER_COLTON"]},
                    {"name": "Youngster Ben", "data_ids": ["TRAINER_YOUNGSTER_BEN"]},
                    {"name": "Bug Catcher Greg", "data_ids": ["TRAINER_BUG_CATCHER_GREG"]},
                    {"name": "Youngster Calvin", "data_ids": ["TRAINER_YOUNGSTER_CALVIN"]},
                    {"name": "Lass Sally", "data_ids": ["TRAINER_LASS_SALLY"]},
                    {"name": "Bug Catcher James", "data_ids": ["TRAINER_BUG_CATCHER_JAMES"]},
                    {"name": "Lass Robin", "data_ids": ["TRAINER_LASS_ROBIN"]}],
        "Mt. Moon 1F": [{"name": "Bug Catcher Kent", "data_ids": ["TRAINER_BUG_CATCHER_KENT"]},
                        {"name": "Lass Iris", "data_ids": ["TRAINER_LASS_IRIS"]},
                        {"name": "Super Nerd Jovan", "data_ids": ["TRAINER_SUPER_NERD_JOVAN"]},
                        {"name": "Bug Catcher Robby", "data_ids": ["TRAINER_BUG_CATCHER_ROBBY"]},
                        {"name": "Lass Miriam", "data_ids": ["TRAINER_LASS_MIRIAM"]},
                        {"name": "Youngster Josh", "data_ids": ["TRAINER_YOUNGSTER_JOSH"]},
                        {"name": "Hiker Marcos", "data_ids": ["TRAINER_HIKER_MARCOS"]}],
        "Mt. Moon B2F": [{"name": "Team Rocket Grunt 1", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT"]},
                         {"name": "Team Rocket Grunt 4", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_4"]},
                         {"name": "Super Nerd Miguel", "data_ids": ["TRAINER_SUPER_NERD_MIGUEL"]}],
        "Mt. Moon B2F South": [{"name": "Team Rocket Grunt 2", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_2"]}],
        "Mt. Moon B2F Northeast": [{"name": "Team Rocket Grunt 3", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_3"]}],
        "Route 4 Northeast": [{"name": "Lass Crissy", "data_ids": ["TRAINER_LASS_CRISSY"]}],
        "Cerulean City": [{"name": "Cerulean City Rival",
                           "data_ids": ["TRAINER_RIVAL_CERULEAN_BULBASAUR", "TRAINER_RIVAL_CERULEAN_CHARMANDER",
                                        "TRAINER_RIVAL_CERULEAN_SQUIRTLE"]}],
        "Cerulean City Outskirts": [{"name": "Team Rocket Grunt 5", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_5"]}],
        "Route 24": [{"name": "Bug Catcher Cale", "data_ids": ["TRAINER_BUG_CATCHER_CALE"]},
                     {"name": "Lass Ali", "data_ids": ["TRAINER_LASS_ALI"]},
                     {"name": "Youngster Timmy", "data_ids": ["TRAINER_YOUNGSTER_TIMMY"]},
                     {"name": "Lass Reli", "data_ids": ["TRAINER_LASS_RELI"]},
                     {"name": "Camper Ethan", "data_ids": ["TRAINER_CAMPER_ETHAN"]},
                     {"name": "Team Rocket Grunt 6", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_6"]},
                     {"name": "Camper Shane", "data_ids": ["TRAINER_CAMPER_SHANE"]}],
        "Route 25": [{"name": "Hiker Franklin", "data_ids": ["TRAINER_HIKER_FRANKLIN"]},
                     {"name": "Hiker Wayne", "data_ids": ["TRAINER_HIKER_WAYNE"]},
                     {"name": "Youngster Joey", "data_ids": ["TRAINER_YOUNGSTER_JOEY"]},
                     {"name": "Youngster Dan", "data_ids": ["TRAINER_YOUNGSTER_DAN"]},
                     {"name": "Picnicker Kelsey", "data_ids": ["TRAINER_PICNICKER_KELSEY"]},
                     {"name": "Hiker Nob", "data_ids": ["TRAINER_HIKER_NOB"]},
                     {"name": "Camper Flint", "data_ids": ["TRAINER_CAMPER_FLINT"]},
                     {"name": "Youngster Chad", "data_ids": ["TRAINER_YOUNGSTER_CHAD"]},
                     {"name": "Lass Haley", "data_ids": ["TRAINER_LASS_HALEY"]}],
        "Cerulean Gym": [{"name": "Cerulean Gym Trainers",
                          "data_ids": ["TRAINER_SWIMMER_MALE_LUIS", "TRAINER_PICNICKER_DIANA",
                                       "TRAINER_LEADER_MISTY"]}],
        "Route 6": [{"name": "Bug Catcher Keigo", "data_ids": ["TRAINER_BUG_CATCHER_KEIGO"]},
                    {"name": "Camper Ricky", "data_ids": ["TRAINER_CAMPER_RICKY"]},
                    {"name": "Picnicker Nancy", "data_ids": ["TRAINER_PICNICKER_NANCY"]},
                    {"name": "Bug Catcher Elijah", "data_ids": ["TRAINER_BUG_CATCHER_ELIJAH"]},
                    {"name": "Picnicker Isabelle", "data_ids": ["TRAINER_PICNICKER_ISABELLE"]},
                    {"name": "Camper Jeff", "data_ids": ["TRAINER_CAMPER_JEFF"]}],
        "Route 11 West": [{"name": "Youngster Eddie", "data_ids": ["TRAINER_YOUNGSTER_EDDIE"]},
                          {"name": "Gamer Hugo", "data_ids": ["TRAINER_GAMER_HUGO"]},
                          {"name": "Engineer Bernie", "data_ids": ["TRAINER_ENGINEER_BERNIE"]},
                          {"name": "Youngster Dave", "data_ids": ["TRAINER_YOUNGSTER_DAVE"]},
                          {"name": "Youngster Dillon", "data_ids": ["TRAINER_YOUNGSTER_DILLON"]},
                          {"name": "Gamer Jasper", "data_ids": ["TRAINER_GAMER_JASPER"]},
                          {"name": "Engineer Braxton", "data_ids": ["TRAINER_ENGINEER_BRAXTON"]},
                          {"name": "Gamer Darian", "data_ids": ["TRAINER_GAMER_DARIAN"]},
                          {"name": "Youngster Yasu", "data_ids": ["TRAINER_YOUNGSTER_YASU"]},
                          {"name": "Gamer Dirk", "data_ids": ["TRAINER_GAMER_DIRK"]}],
        "S.S. Anne Deck": [{"name": "Sailor Trevor", "data_ids": ["TRAINER_SAILOR_TREVOR"]},
                           {"name": "Sailor Edmond", "data_ids": ["TRAINER_SAILOR_EDMOND"]}],
        "S.S. Anne B1F Room 1": [{"name": "Fisherman Barny", "data_ids": ["TRAINER_FISHERMAN_BARNY"]},
                                 {"name": "Sailor Phillip", "data_ids": ["TRAINER_SAILOR_PHILLIP"]}],
        "S.S. Anne B1F Room 2": [{"name": "Sailor Huey", "data_ids": ["TRAINER_SAILOR_HUEY"]}],
        "S.S. Anne B1F Room 3": [{"name": "Sailor Dylan", "data_ids": ["TRAINER_SAILOR_DYLAN"]}],
        "S.S. Anne B1F Room 4": [{"name": "Sailor Duncan", "data_ids": ["TRAINER_SAILOR_DUNCAN"]},
                                 {"name": "Sailor Leonard", "data_ids": ["TRAINER_SAILOR_LEONARD"]}],
        "S.S. Anne 1F Room 2": [{"name": "Lass Ann", "data_ids": ["TRAINER_LASS_ANN"]},
                                {"name": "Youngster Tyler", "data_ids": ["TRAINER_YOUNGSTER_TYLER"]}],
        "S.S. Anne 1F Room 5": [{"name": "Gentleman Arthur", "data_ids": ["TRAINER_GENTLEMAN_ARTHUR"]}],
        "S.S. Anne 1F Room 7": [{"name": "Gentleman Thomas", "data_ids": ["TRAINER_GENTLEMAN_THOMAS"]}],
        "S.S. Anne 2F Room 2": [{"name": "Fisherman Dale", "data_ids": ["TRAINER_FISHERMAN_DALE"]},
                                {"name": "Gentleman Brooks", "data_ids": ["TRAINER_GENTLEMAN_BROOKS"]}],
        "S.S. Anne 2F Room 4": [{"name": "Lass Dawn", "data_ids": ["TRAINER_LASS_DAWN"]},
                                {"name": "Gentleman Lamar", "data_ids": ["TRAINER_GENTLEMAN_LAMAR"]}],
        "S.S. Anne 2F Corridor": [{"name": "S.S. Anne Rival",
                                   "data_ids": ["TRAINER_RIVAL_SS_ANNE_BULBASAUR", "TRAINER_RIVAL_SS_ANNE_CHARMANDER",
                                                "TRAINER_RIVAL_SS_ANNE_SQUIRTLE"]}],
        "Vermilion Gym": [{"name": "Vermilion Gym Trainers",
                           "data_ids": ["TRAINER_SAILOR_DWAYNE", "TRAINER_ENGINEER_BAILY", "TRAINER_GENTLEMAN_TUCKER",
                                        "TRAINER_LEADER_LT_SURGE"]}],
        "Route 9": [{"name": "Picnicker Alicia", "data_ids": ["TRAINER_PICNICKER_ALICIA"]},
                    {"name": "Hiker Jeremy", "data_ids": ["TRAINER_HIKER_JEREMY"]},
                    {"name": "Camper Chris", "data_ids": ["TRAINER_CAMPER_CHRIS"]},
                    {"name": "Bug Catcher Brent", "data_ids": ["TRAINER_BUG_CATCHER_BRENT"]},
                    {"name": "Hiker Alan", "data_ids": ["TRAINER_HIKER_ALAN"]},
                    {"name": "Bug Catcher Conner", "data_ids": ["TRAINER_BUG_CATCHER_CONNER"]},
                    {"name": "Camper Drew", "data_ids": ["TRAINER_CAMPER_DREW"]},
                    {"name": "Hiker Brice", "data_ids": ["TRAINER_HIKER_BRICE"]},
                    {"name": "Picnicker Caitlin", "data_ids": ["TRAINER_PICNICKER_CAITLIN"]}],
        "Route 10 North": [{"name": "Picnicker Heidi", "data_ids": ["TRAINER_PICNICKER_HEIDI"]}],
        "Route 10 South": [{"name": "Picnicker Carol", "data_ids": ["TRAINER_PICNICKER_CAROL"]},
                           {"name": "Hiker Clark", "data_ids": ["TRAINER_HIKER_CLARK"]},
                           {"name": "Hiker Trent", "data_ids": ["TRAINER_HIKER_TRENT"]},
                           {"name": "PokeManiac Herman", "data_ids": ["TRAINER_POKEMANIAC_HERMAN"]}],
        "Route 10 Near Power Plant": [{"name": "PokeManiac Mark", "data_ids": ["TRAINER_POKEMANIAC_MARK"]}],
        "Rock Tunnel 1F Northeast": [{"name": "PokeManiac Ashton", "data_ids": ["TRAINER_POKEMANIAC_ASHTON"]}],
        "Rock Tunnel B1F Southeast": [{"name": "PokeManiac Winston", "data_ids": ["TRAINER_POKEMANIAC_WINSTON"]},
                                      {"name": "Picnicker Martha", "data_ids": ["TRAINER_PICNICKER_MARTHA"]},
                                      {"name": "PokeManiac Steve", "data_ids": ["TRAINER_POKEMANIAC_STEVE"]},
                                      {"name": "Hiker Allen", "data_ids": ["TRAINER_HIKER_ALLEN"]},
                                      {"name": "Hiker Eric", "data_ids": ["TRAINER_HIKER_ERIC"]}],
        "Rock Tunnel 1F Northwest": [{"name": "Hiker Lenny", "data_ids": ["TRAINER_HIKER_LENNY"]},
                                     {"name": "Hiker Oliver", "data_ids": ["TRAINER_HIKER_OLIVER"]},
                                     {"name": "Hiker Lucas", "data_ids": ["TRAINER_HIKER_LUCAS"]}],
        "Rock Tunnel B1F Northwest": [{"name": "Picnicker Sofia", "data_ids": ["TRAINER_PICNICKER_SOFIA"]},
                                      {"name": "Hiker Dudley", "data_ids": ["TRAINER_HIKER_DUDLEY"]},
                                      {"name": "PokeManiac Cooper", "data_ids": ["TRAINER_POKEMANIAC_COOPER"]}],
        "Rock Tunnel 1F South": [{"name": "Picnicker Leah", "data_ids": ["TRAINER_PICNICKER_LEAH"]},
                                 {"name": "Picnicker Ariana", "data_ids": ["TRAINER_PICNICKER_ARIANA"]},
                                 {"name": "Picnicker Dana", "data_ids": ["TRAINER_PICNICKER_DANA"]}],
        "Pokemon Tower 2F": [{"name": "Pokemon Tower Rival", "data_ids": ["TRAINER_RIVAL_POKEMON_TOWER_BULBASAUR",
                                                                          "TRAINER_RIVAL_POKEMON_TOWER_CHARMANDER",
                                                                          "TRAINER_RIVAL_POKEMON_TOWER_SQUIRTLE"]}],
        "Pokemon Tower 3F": [{"name": "Channeler Hope", "data_ids": ["TRAINER_CHANNELER_HOPE"]},
                             {"name": "Channeler Patricia", "data_ids": ["TRAINER_CHANNELER_PATRICIA"]},
                             {"name": "Channeler Carly", "data_ids": ["TRAINER_CHANNELER_CARLY"]}],
        "Pokemon Tower 4F": [{"name": "Channeler Laurel", "data_ids": ["TRAINER_CHANNELER_LAUREL"]},
                             {"name": "Channeler Jody", "data_ids": ["TRAINER_CHANNELER_JODY"]},
                             {"name": "Channeler Paula", "data_ids": ["TRAINER_CHANNELER_PAULA"]}],
        "Pokemon Tower 5F": [{"name": "Channeler Ruth", "data_ids": ["TRAINER_CHANNELER_RUTH"]},
                             {"name": "Channeler Tammy", "data_ids": ["TRAINER_CHANNELER_TAMMY"]},
                             {"name": "Channeler Karina", "data_ids": ["TRAINER_CHANNELER_KARINA"]},
                             {"name": "Channeler Janae", "data_ids": ["TRAINER_CHANNELER_JANAE"]}],
        "Pokemon Tower 6F": [{"name": "Channeler Angelica", "data_ids": ["TRAINER_CHANNELER_ANGELICA"]},
                             {"name": "Channeler Jennifer", "data_ids": ["TRAINER_CHANNELER_JENNIFER"]},
                             {"name": "Channeler Emilia", "data_ids": ["TRAINER_CHANNELER_EMILIA"]}],
        "Pokemon Tower 7F": [{"name": "Team Rocket Grunt 19", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_19"]},
                             {"name": "Team Rocket Grunt 20", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_20"]},
                             {"name": "Team Rocket Grunt 21", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_21"]}],
        "Route 8": [{"name": "Lass Julia", "data_ids": ["TRAINER_LASS_JULIA"]},
                    {"name": "Gamer Rich", "data_ids": ["TRAINER_GAMER_RICH"]},
                    {"name": "Super Nerd Glenn", "data_ids": ["TRAINER_SUPER_NERD_GLENN"]},
                    {"name": "Twins Eli & Anne", "data_ids": ["TRAINER_TWINS_ELI_ANNE"]},
                    {"name": "Lass Paige", "data_ids": ["TRAINER_LASS_PAIGE"]},
                    {"name": "Super Nerd Leslie", "data_ids": ["TRAINER_SUPER_NERD_LESLIE"]},
                    {"name": "Lass Andrea", "data_ids": ["TRAINER_LASS_ANDREA"]},
                    {"name": "Lass Megan", "data_ids": ["TRAINER_LASS_MEGAN"]},
                    {"name": "Biker Jaren", "data_ids": ["TRAINER_BIKER_JAREN"]},
                    {"name": "Biker Ricardo", "data_ids": ["TRAINER_BIKER_RICARDO"]},
                    {"name": "Gamer Stan", "data_ids": ["TRAINER_GAMER_STAN"]},
                    {"name": "Super Nerd Aidan", "data_ids": ["TRAINER_SUPER_NERD_AIDAN"]}],
        "Celadon Game Corner": [{"name": "Team Rocket Grunt 7", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_7"]}],
        "Rocket Hideout B1F North": [{"name": "Team Rocket Grunt 8", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_8"]},
                                     {"name": "Team Rocket Grunt 9", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_9"]}],
        "Rocket Hideout B1F Southeast": [{"name": "Team Rocket Grunt 12",
                                          "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_12"]}],
        "Rocket Hideout B1F Southwest": [{"name": "Team Rocket Grunt 10",
                                          "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_10"]},
                                         {"name": "Team Rocket Grunt 11",
                                          "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_11"]}],
        "Rocket Hideout B2F": [{"name": "Team Rocket Grunt 13", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_13"]}],
        "Rocket Hideout B3F": [{"name": "Team Rocket Grunt 14", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_14"]},
                               {"name": "Team Rocket Grunt 15", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_15"]}],
        "Rocket Hideout B4F West": [{"name": "Team Rocket Grunt 18", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_18"]}],
        "Rocket Hideout B4F East": [{"name": "Team Rocket Grunt 16", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_16"]},
                                    {"name": "Team Rocket Grunt 17", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_17"]},
                                    {"name": "Boss Giovanni 1", "data_ids": ["TRAINER_BOSS_GIOVANNI"]}],
        "Celadon Gym Trainers": [{"name": "Celadon Gym Trainers",
                                  "connections": ["Celadon Gym", "Celadon Gym Behind Trees"],
                                  "data_ids": ["TRAINER_LASS_KAY", "TRAINER_BEAUTY_BRIDGET", "TRAINER_COOLTRAINER_MARY",
                                               "TRAINER_LASS_LISA", "TRAINER_PICNICKER_TINA", "TRAINER_BEAUTY_LORI",
                                               "TRAINER_BEAUTY_TAMIA", "TRAINER_LEADER_ERIKA"]}],
        "Route 12 Center": [{"name": "Fisherman Ned", "data_ids": ["TRAINER_FISHERMAN_NED"]},
                            {"name": "Fisherman Chip", "data_ids": ["TRAINER_FISHERMAN_CHIP"]},
                            {"name": "Fisherman Hank", "data_ids": ["TRAINER_FISHERMAN_HANK"]},
                            {"name": "Fisherman Elliot", "data_ids": ["TRAINER_FISHERMAN_ELLIOT"]},
                            {"name": "Young Couple Gia & Jes", "data_ids": ["TRAINER_YOUNG_COUPLE_GIA_JES"]}],
        "Route 12 South": [{"name": "Rocker Luca", "data_ids": ["TRAINER_ROCKER_LUCA"]},
                           {"name": "Fisherman Andrew", "data_ids": ["TRAINER_FISHERMAN_ANDREW"]}],
        "Route 12 Behind North Tree": [{"name": "Camper Justin", "data_ids": ["TRAINER_CAMPER_JUSTIN"]}],
        "Route 13": [{"name": "Picnicker Alma", "data_ids": ["TRAINER_PICNICKER_ALMA"]},
                     {"name": "Bird Keeper Sebastian", "data_ids": ["TRAINER_BIRD_KEEPER_SEBASTIAN"]},
                     {"name": "Picnicker Susie", "data_ids": ["TRAINER_PICNICKER_SUSIE"]},
                     {"name": "Beauty Lola", "data_ids": ["TRAINER_BEAUTY_LOLA"]},
                     {"name": "Beauty Sheila", "data_ids": ["TRAINER_BEAUTY_SHEILA"]},
                     {"name": "Picnicker Valerie", "data_ids": ["TRAINER_PICNICKER_VALERIE"]},
                     {"name": "Picnicker Gwen", "data_ids": ["TRAINER_PICNICKER_GWEN"]},
                     {"name": "Bird Keeper Robert", "data_ids": ["TRAINER_BIRD_KEEPER_ROBERT"]},
                     {"name": "Bird Keeper Perry", "data_ids": ["TRAINER_BIRD_KEEPER_PERRY"]},
                     {"name": "Biker Jared", "data_ids": ["TRAINER_BIKER_JARED"]}],
        "Route 14": [{"name": "Bird Keeper Carter", "data_ids": ["TRAINER_BIRD_KEEPER_CARTER"]},
                     {"name": "Bird Keeper Mitch", "data_ids": ["TRAINER_BIRD_KEEPER_MITCH"]},
                     {"name": "Bird Keeper Marlon", "data_ids": ["TRAINER_BIRD_KEEPER_MARLON"]},
                     {"name": "Bird Keeper Beck", "data_ids": ["TRAINER_BIRD_KEEPER_BECK"]},
                     {"name": "Bird Keeper Donald", "data_ids": ["TRAINER_BIRD_KEEPER_DONALD"]},
                     {"name": "Bird Keeper Benny", "data_ids": ["TRAINER_BIRD_KEEPER_BENNY"]},
                     {"name": "Twins Kiri & Jan", "data_ids": ["TRAINER_TWINS_KIRI_JAN"]},
                     {"name": "Biker Gerald", "data_ids": ["TRAINER_BIKER_GERALD"]},
                     {"name": "Biker Malik", "data_ids": ["TRAINER_BIKER_MALIK"]},
                     {"name": "Biker Isaac", "data_ids": ["TRAINER_BIKER_ISAAC"]},
                     {"name": "Biker Lukas", "data_ids": ["TRAINER_BIKER_LUKAS"]}],
        "Route 15 South": [{"name": "Biker Ernest", "data_ids": ["TRAINER_BIKER_ERNEST"]},
                           {"name": "Biker Alex", "data_ids": ["TRAINER_BIKER_ALEX"]},
                           {"name": "Beauty Grace", "data_ids": ["TRAINER_BEAUTY_GRACE"]},
                           {"name": "Beauty Olivia", "data_ids": ["TRAINER_BEAUTY_OLIVIA"]},
                           {"name": "Picnicker Kindra", "data_ids": ["TRAINER_PICNICKER_KINDRA"]},
                           {"name": "Bird Keeper Chester", "data_ids": ["TRAINER_BIRD_KEEPER_CHESTER"]},
                           {"name": "Bird Keeper Edwin", "data_ids": ["TRAINER_BIRD_KEEPER_EDWIN"]},
                           {"name": "Picnicker Yazmin", "data_ids": ["TRAINER_PICNICKER_YAZMIN"]}],
        "Route 15 North": [{"name": "Picnicker Becky", "data_ids": ["TRAINER_PICNICKER_BECKY"]},
                           {"name": "Crush Kin Ron & Mya", "data_ids": ["TRAINER_CRUSH_KIN_RON_MYA"]},
                           {"name": "Picnicker Celia", "data_ids": ["TRAINER_PICNICKER_CELIA"]}],
        "Route 16 Northeast": [{"name": "Young Couple Lea & Jed", "data_ids": ["TRAINER_YOUNG_COUPLE_LEA_JED"]}],
        "Route 16 Southwest": [{"name": "Biker Lao", "data_ids": ["TRAINER_BIKER_LAO"]},
                               {"name": "Cue Ball Koji", "data_ids": ["TRAINER_CUE_BALL_KOJI"]},
                               {"name": "Cue Ball Luke", "data_ids": ["TRAINER_CUE_BALL_LUKE"]},
                               {"name": "Biker Hideo", "data_ids": ["TRAINER_BIKER_HIDEO"]},
                               {"name": "Biker Ruben", "data_ids": ["TRAINER_BIKER_RUBEN"]},
                               {"name": "Cue Ball Camron", "data_ids": ["TRAINER_CUE_BALL_CAMRON"]}],
        "Route 17": [{"name": "Cue Ball Isaiah", "data_ids": ["TRAINER_CUE_BALL_ISAIAH"]},
                     {"name": "Biker Virgil", "data_ids": ["TRAINER_BIKER_VIRGIL"]},
                     {"name": "Cue Ball Raul", "data_ids": ["TRAINER_CUE_BALL_RAUL"]},
                     {"name": "Biker Billy", "data_ids": ["TRAINER_BIKER_BILLY"]},
                     {"name": "Cue Ball Jamal", "data_ids": ["TRAINER_CUE_BALL_JAMAL"]},
                     {"name": "Biker Nikolas", "data_ids": ["TRAINER_BIKER_NIKOLAS"]},
                     {"name": "Cue Ball Zeek", "data_ids": ["TRAINER_CUE_BALL_ZEEK"]},
                     {"name": "Cue Ball Corey", "data_ids": ["TRAINER_CUE_BALL_COREY"]},
                     {"name": "Biker Jaxon", "data_ids": ["TRAINER_BIKER_JAXON"]},
                     {"name": "Biker William", "data_ids": ["TRAINER_BIKER_WILLIAM"]}],
        "Route 18 East": [{"name": "Bird Keeper Jacob", "data_ids": ["TRAINER_BIRD_KEEPER_JACOB"]},
                          {"name": "Bird Keeper Wilton", "data_ids": ["TRAINER_BIRD_KEEPER_WILTON"]},
                          {"name": "Bird Keeper Ramiro", "data_ids": ["TRAINER_BIRD_KEEPER_RAMIRO"]}],
        "Fuchsia Gym": [{"name": "Fuchsia Gym Trainers",
                         "data_ids": ["TRAINER_JUGGLER_NATE", "TRAINER_JUGGLER_KAYDEN", "TRAINER_JUGGLER_KIRK",
                                      "TRAINER_TAMER_EDGAR", "TRAINER_TAMER_PHIL", "TRAINER_JUGGLER_SHAWN",
                                      "TRAINER_LEADER_KOGA"]}],
        "Silph Co. 2F": [{"name": "Team Rocket Grunt 23", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_23"]},
                         {"name": "Team Rocket Grunt 24", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_24"]},
                         {"name": "Scientist Jerry", "data_ids": ["TRAINER_SCIENTIST_JERRY"]}],
        "Silph Co. 2F Southwest Room": [{"name": "Scientist Connor", "data_ids": ["TRAINER_SCIENTIST_CONNOR"]}],
        "Silph Co. 3F": [{"name": "Team Rocket Grunt 25", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_25"]}],
        "Silph Co. 3F West Room": [{"name": "Scientist Jose", "data_ids": ["TRAINER_SCIENTIST_JOSE"]}],
        "Silph Co. 4F": [{"name": "Team Rocket Grunt 26", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_26"]},
                         {"name": "Team Rocket Grunt 27", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_27"]}],
        "Silph Co. 4F North Room": [{"name": "Scientist Rodney", "data_ids": ["TRAINER_SCIENTIST_RODNEY"]}],
        "Silph Co. 5F": [{"name": "Team Rocket Grunt 28", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_28"]},
                         {"name": "Team Rocket Grunt 29", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_29"]},
                         {"name": "Juggler Dalton", "data_ids": ["TRAINER_JUGGLER_DALTON"]},
                         {"name": "Scientist Beau", "data_ids": ["TRAINER_SCIENTIST_BEAU"]}],
        "Silph Co. 6F": [{"name": "Team Rocket Grunt 30", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_30"]},
                         {"name": "Team Rocket Grunt 31", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_31"]},
                         {"name": "Scientist Taylor", "data_ids": ["TRAINER_SCIENTIST_TAYLOR"]}],
        "Silph Co. 7F": [{"name": "Team Rocket Grunt 33", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_33"]},
                         {"name": "Team Rocket Grunt 35", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_35"]},
                         {"name": "Scientist Joshua", "data_ids": ["TRAINER_SCIENTIST_JOSHUA"]}],
        "Silph Co. 7F Northwest Room": [{"name": "Silph Co. Rival",
                                         "data_ids": ["TRAINER_RIVAL_SILPH_BULBASAUR", "TRAINER_RIVAL_SILPH_CHARMANDER",
                                                      "TRAINER_RIVAL_SILPH_SQUIRTLE"]}],
        "Silph Co. 7F Southeast Room": [{"name": "Team Rocket Grunt 34", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_34"]}],
        "Silph Co. 8F": [{"name": "Team Rocket Grunt 32", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_32"]},
                         {"name": "Team Rocket Grunt 36", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_36"]},
                         {"name": "Scientist Parker", "data_ids": ["TRAINER_SCIENTIST_PARKER"]}],
        "Silph Co. 9F": [{"name": "Team Rocket Grunt 38", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_38"]},
                         {"name": "Scientist Ed", "data_ids": ["TRAINER_SCIENTIST_ED"]}],
        "Silph Co. 9F Northwest Room": [{"name": "Team Rocket Grunt 37", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_37"]}],
        "Silph Co. 10F": [{"name": "Team Rocket Grunt 39", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_39"]},
                          {"name": "Scientist Travis", "data_ids": ["TRAINER_SCIENTIST_TRAVIS"]}],
        "Silph Co. 11F East": [{"name": "Team Rocket Grunt 40", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_40"]}],
        "Silph Co. 11F West": [{"name": "Team Rocket Grunt 41", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_41"]}],
        "Silph Co. 11F President's Room": [{"name": "Boss Giovanni 2", "data_ids": ["TRAINER_BOSS_GIOVANNI_2"]}],
        "Saffron Dojo": [{"name": "Black Belt Hideki", "data_ids": ["TRAINER_BLACK_BELT_HIDEKI"]},
                         {"name": "Black Belt Hitoshi", "data_ids": ["TRAINER_BLACK_BELT_HITOSHI"]},
                         {"name": "Black Belt Mike", "data_ids": ["TRAINER_BLACK_BELT_MIKE"]},
                         {"name": "Black Belt Aaron", "data_ids": ["TRAINER_BLACK_BELT_AARON"]},
                         {"name": "Black Belt Koichi", "data_ids": ["TRAINER_BLACK_BELT_KOICHI"]}],
        "Saffron Gym Trainers": [{"name": "Saffron Gym Trainers",
                                  "connections": ["Saffron Gym Northwest", "Saffron Gym North", "Saffron Gym Northeast",
                                                  "Saffron Gym West", "Saffron Gym Center", "Saffron Gym East",
                                                  "Saffron Gym Southwest", "Saffron Gym Southeast"],
                                  "data_ids": ["TRAINER_PSYCHIC_CAMERON", "TRAINER_PSYCHIC_TYRON",
                                               "TRAINER_CHANNELER_STACY", "TRAINER_PSYCHIC_PRESTON",
                                               "TRAINER_CHANNELER_AMANDA", "TRAINER_CHANNELER_TASHA",
                                               "TRAINER_PSYCHIC_JOHAN", "TRAINER_LEADER_SABRINA"]}],
        "Route 19": [{"name": "Swimmer Richard", "data_ids": ["TRAINER_SWIMMER_MALE_RICHARD"]},
                     {"name": "Swimmer Reece", "data_ids": ["TRAINER_SWIMMER_MALE_REECE"]}],
        "Route 19 Water": [{"name": "Swimmer Tony", "data_ids": ["TRAINER_SWIMMER_MALE_TONY"]},
                           {"name": "Swimmer David", "data_ids": ["TRAINER_SWIMMER_MALE_DAVID"]},
                           {"name": "Swimmer Douglas", "data_ids": ["TRAINER_SWIMMER_MALE_DOUGLAS"]},
                           {"name": "Swimmer Matthew", "data_ids": ["TRAINER_SWIMMER_MALE_MATTHEW"]},
                           {"name": "Sis and Bro Lia & Luc", "data_ids": ["TRAINER_SIS_AND_BRO_LIA_LUC"]},
                           {"name": "Swimmer Axle", "data_ids": ["TRAINER_SWIMMER_MALE_AXLE"]},
                           {"name": "Swimmer Alice", "data_ids": ["TRAINER_SWIMMER_FEMALE_ALICE"]},
                           {"name": "Swimmer Anya", "data_ids": ["TRAINER_SWIMMER_FEMALE_ANYA"]},
                           {"name": "Swimmer Connie", "data_ids": ["TRAINER_SWIMMER_FEMALE_CONNIE"]}],
        "Route 20 East": [{"name": "Swimmer Barry", "data_ids": ["TRAINER_SWIMMER_MALE_BARRY"]},
                          {"name": "Swimmer Darrin", "data_ids": ["TRAINER_SWIMMER_MALE_DARRIN"]},
                          {"name": "Swimmer Shirley", "data_ids": ["TRAINER_SWIMMER_FEMALE_SHIRLEY"]},
                          {"name": "Swimmer Tiffany", "data_ids": ["TRAINER_SWIMMER_FEMALE_TIFFANY"]}],
        "Route 20 Near South Cave": [{"name": "Picnicker Irene", "data_ids": ["TRAINER_PICNICKER_IRENE"]}],
        "Route 20 West": [{"name": "Bird Keeper Roger", "data_ids": ["TRAINER_BIRD_KEEPER_ROGER"]},
                          {"name": "Swimmer Nora", "data_ids": ["TRAINER_SWIMMER_FEMALE_NORA"]},
                          {"name": "Swimmer Dean", "data_ids": ["TRAINER_SWIMMER_MALE_DEAN"]},
                          {"name": "Picnicker Missy", "data_ids": ["TRAINER_PICNICKER_MISSY"]},
                          {"name": "Swimmer Melissa", "data_ids": ["TRAINER_SWIMMER_FEMALE_MELISSA"]}],
        "Pokemon Mansion 1F": [{"name": "Youngster Johnson", "data_ids": ["TRAINER_YOUNGSTER_JOHNSON"]}],
        "Pokemon Mansion 2F": [{"name": "Burglar Arnie", "data_ids": ["TRAINER_BURGLAR_ARNIE"]}],
        "Pokemon Mansion 3F Southwest": [{"name": "Burglar Simon", "data_ids": ["TRAINER_BURGLAR_SIMON"]}],
        "Pokemon Mansion 3F Southeast": [{"name": "Scientist Braydon", "data_ids": ["TRAINER_SCIENTIST_BRAYDON"]}],
        "Pokemon Mansion 1F South": [{"name": "Scientist Ted", "data_ids": ["TRAINER_SCIENTIST_TED"]}],
        "Pokemon Mansion B1F": [{"name": "Burglar Lewis", "data_ids": ["TRAINER_BURGLAR_LEWIS"]},
                                {"name": "Scientist Ivan", "data_ids": ["TRAINER_SCIENTIST_IVAN"]}],
        "Cinnabar Gym": [{"name": "Cinnabar Gym Trainers",
                          "data_ids": ["TRAINER_BURGLAR_QUINN", "TRAINER_SUPER_NERD_ERIK", "TRAINER_SUPER_NERD_AVERY",
                                       "TRAINER_BURGLAR_RAMON", "TRAINER_SUPER_NERD_DEREK", "TRAINER_BURGLAR_DUSTY",
                                       "TRAINER_SUPER_NERD_ZAC", "TRAINER_LEADER_BLAINE"]}],
        "Route 21": [{"name": "Fisherman Wade", "data_ids": ["TRAINER_FISHERMAN_WADE"]},
                     {"name": "Fisherman Ronald", "data_ids": ["TRAINER_FISHERMAN_RONALD"]},
                     {"name": "Sis and Bro Lil & Ian", "data_ids": ["TRAINER_SIS_AND_BRO_LIL_IAN"]},
                     {"name": "Swimmer Spencer", "data_ids": ["TRAINER_SWIMMER_MALE_SPENCER"]},
                     {"name": "Fisherman Claude", "data_ids": ["TRAINER_FISHERMAN_CLAUDE"]},
                     {"name": "Fisherman Nolan", "data_ids": ["TRAINER_FISHERMAN_NOLAN"]},
                     {"name": "Swimmer Jack", "data_ids": ["TRAINER_SWIMMER_MALE_JACK"]},
                     {"name": "Swimmer Roland", "data_ids": ["TRAINER_SWIMMER_MALE_ROLAND"]},
                     {"name": "Swimmer Jerome", "data_ids": ["TRAINER_SWIMMER_MALE_JEROME"]}],
        "Viridian Gym": [{"name": "Viridian Gym Trainers",
                          "data_ids": ["TRAINER_TAMER_COLE", "TRAINER_BLACK_BELT_KIYO", "TRAINER_COOLTRAINER_SAMUEL",
                                       "TRAINER_COOLTRAINER_YUJI", "TRAINER_BLACK_BELT_ATSUSHI", "TRAINER_TAMER_JASON",
                                       "TRAINER_COOLTRAINER_WARREN", "TRAINER_BLACK_BELT_TAKASHI",
                                       "TRAINER_LEADER_GIOVANNI"]}],
        "Victory Road 1F North": [{"name": "Cooltrainer Naomi", "data_ids": ["TRAINER_COOLTRAINER_NAOMI"]},
                                  {"name": "Cooltrainer Rolando", "data_ids": ["TRAINER_COOLTRAINER_ROLANDO"]}],
        "Victory Road 2F Center": [{"name": "Black Belt Daisuke", "data_ids": ["TRAINER_BLACK_BELT_DAISUKE"]},
                                   {"name": "Juggler Nelson", "data_ids": ["TRAINER_JUGGLER_NELSON"]},
                                   {"name": "Tamer Vincent", "data_ids": ["TRAINER_TAMER_VINCENT"]},
                                   {"name": "Juggler Gregory", "data_ids": ["TRAINER_JUGGLER_GREGORY"]}],
        "Victory Road 3F North": [{"name": "Cooltrainer George", "data_ids": ["TRAINER_COOLTRAINER_GEORGE"]},
                                  {"name": "Cooltrainer Alexa", "data_ids": ["TRAINER_COOLTRAINER_ALEXA"]}],
        "Victory Road 2F Northwest": [{"name": "PokeManiac Dawson", "data_ids": ["TRAINER_POKEMANIAC_DAWSON"]}],
        "Victory Road 3F Southwest": [{"name": "Cooltrainer Colby", "data_ids": ["TRAINER_COOLTRAINER_COLBY"]},
                                      {"name": "Cooltrainer Caroline", "data_ids": ["TRAINER_COOLTRAINER_CAROLINE"]}],
        "Victory Road 3F Southeast": [{"name": "Cool Couple Ray & Tyra", "data_ids": ["TRAINER_COOL_COUPLE_RAY_TYRA"]}],
        "Elite Four": [{"name": "Elite Four",
                        "connections": ["Pokemon League Lorelei's Room", "Pokemon League Bruno's Room",
                                        "Pokemon League Agatha's Room", "Pokemon League Lance's Room",
                                        "Pokemon League Champion's Room"],
                        "data_ids": ["TRAINER_ELITE_FOUR_LORELEI", "TRAINER_ELITE_FOUR_BRUNO",
                                     "TRAINER_ELITE_FOUR_AGATHA", "TRAINER_ELITE_FOUR_LANCE",
                                     "TRAINER_CHAMPION_FIRST_BULBASAUR", "TRAINER_CHAMPION_FIRST_CHARMANDER",
                                     "TRAINER_CHAMPION_FIRST_SQUIRTLE"]}]
    }

    sevii_trainer_data = {
        "Treasure Beach Water": [{"name": "Swimmer Amara", "data_ids": ["TRAINER_SWIMMER_FEMALE_AMARA"]}],
        "Kindle Road South Water": [{"name": "Swimmer Abigail", "data_ids": ["TRAINER_SWIMMER_FEMALE_ABIGAIL"]}],
        "Kindle Road Center": [{"name": "Picnicker Claire", "data_ids": ["TRAINER_PICNICKER_CLAIRE"]},
                               {"name": "Crush Girl Tanya", "data_ids": ["TRAINER_CRUSH_GIRL_TANYA"]},
                               {"name": "Camper Bryce", "data_ids": ["TRAINER_CAMPER_BRYCE"]},
                               {"name": "Swimmer Garrett", "data_ids": ["TRAINER_SWIMMER_MALE_GARRETT"]},
                               {"name": "Crush Kin Mik & Kia", "data_ids": ["TRAINER_CRUSH_KIN_MIK_KIA"]},
                               {"name": "Black Belt Hugh", "data_ids": ["TRAINER_BLACK_BELT_HUGH"]},
                               {"name": "Black Belt Shea", "data_ids": ["TRAINER_BLACK_BELT_SHEA"]},
                               {"name": "Crush Girl Sharon", "data_ids": ["TRAINER_CRUSH_GIRL_SHARON"]}],
        "Kindle Road North Water": [{"name": "Swimmer Finn", "data_ids": ["TRAINER_SWIMMER_MALE_FINN"]},
                                    {"name": "Swimmer Maria", "data_ids": ["TRAINER_SWIMMER_FEMALE_MARIA"]},
                                    {"name": "Fisherman Tommy", "data_ids": ["TRAINER_FISHERMAN_TOMMY"]}],
        "Mt. Ember Exterior South": [{"name": "Team Rocket Grunt 43", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_43"]},
                                     {"name": "Team Rocket Grunt 44", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_44"]}],
        "Mt. Ember Exterior Center": [{"name": "Pokemon Ranger Beth", "data_ids": ["TRAINER_PKMN_RANGER_BETH"]},
                                      {"name": "Crush Girl Jocelyn", "data_ids": ["TRAINER_CRUSH_GIRL_JOCELYN"]},
                                      {"name": "Pokemon Ranger Logan", "data_ids": ["TRAINER_PKMN_RANGER_LOGAN"]}],
        "Three Island Town": [{"name": "Biker Goon 1", "data_ids": ["TRAINER_BIKER_GOON"]},
                              {"name": "Biker Goon 2", "data_ids": ["TRAINER_BIKER_GOON_2"]},
                              {"name": "Biker Goon 3", "data_ids": ["TRAINER_BIKER_GOON_3"]},
                              {"name": "Cue Ball Paxton", "data_ids": ["TRAINER_CUE_BALL_PAXTON"]}],
        "Bond Bridge": [{"name": "Twins Joy & Meg", "data_ids": ["TRAINER_TWINS_JOY_MEG"]},
                        {"name": "Aroma Lady Violet", "data_ids": ["TRAINER_AROMA_LADY_VIOLET"]},
                        {"name": "Tuber Alexis", "data_ids": ["TRAINER_TUBER_ALEXIS"]},
                        {"name": "Tuber Amira", "data_ids": ["TRAINER_TUBER_AMIRA"]},
                        {"name": "Aroma Lady Nikki", "data_ids": ["TRAINER_AROMA_LADY_NIKKI"]}],
        "Bond Bridge Water": [{"name": "Swimmer Tisha", "data_ids": ["TRAINER_SWIMMER_FEMALE_TISHA"]}],
        "Icefall Cave Back": [{"name": "Team Rocket Grunt 45", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_45"]}],
        "Five Isle Meadow": [{"name": "Team Rocket Grunt 49", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_49"]},
                             {"name": "Team Rocket Grunt 50", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_50"]},
                             {"name": "Team Rocket Grunt 51", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_51"]}],
        "Rocket Warehouse": [{"name": "Team Rocket Grunt 42", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_42"]},
                             {"name": "Team Rocket Grunt 47", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_47"]},
                             {"name": "Team Rocket Grunt 48", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_48"]},
                             {"name": "Team Rocket Admin 1", "data_ids": ["TRAINER_TEAM_ROCKET_ADMIN"]},
                             {"name": "Team Rocket Admin 2", "data_ids": ["TRAINER_TEAM_ROCKET_ADMIN_2"]},
                             {"name": "Scientist Gideon", "data_ids": ["TRAINER_SCIENTIST_GIDEON"]}],
        "Memorial Pillar": [{"name": "Bird Keeper Milo", "data_ids": ["TRAINER_BIRD_KEEPER_MILO"]},
                            {"name": "Bird Keeper Chaz", "data_ids": ["TRAINER_BIRD_KEEPER_CHAZ"]},
                            {"name": "Bird Keeper Harold", "data_ids": ["TRAINER_BIRD_KEEPER_HAROLD"]}],
        "Water Labyrinth": [{"name": "Pokemon Breeder Alize", "data_ids": ["TRAINER_PKMN_BREEDER_ALIZE"]}],
        "Resort Gorgeous Water": [{"name": "Painter Rayna", "data_ids": ["TRAINER_PAINTER_RAYNA"]},
                                  {"name": "Swimmer Toby", "data_ids": ["TRAINER_SWIMMER_MALE_TOBY"]}],
        "Resort Gorgeous Near Resort": [{"name": "Lady Jacki", "data_ids": ["TRAINER_LADY_JACKI"]},
                                        {"name": "Painter Celina", "data_ids": ["TRAINER_PAINTER_CELINA"]},
                                        {"name": "Lady Gillian", "data_ids": ["TRAINER_LADY_GILLIAN"]},
                                        {"name": "Youngster Destin", "data_ids": ["TRAINER_YOUNGSTER_DESTIN"]},
                                        {"name": "Painter Daisy", "data_ids": ["TRAINER_PAINTER_DAISY"]}],
        "Lost Cave B1F Room 1": [{"name": "Ruin Maniac Lawson", "data_ids": ["TRAINER_RUIN_MANIAC_LAWSON"]}],
        "Lost Cave B1F Room 4": [{"name": "Psychic Laura", "data_ids": ["TRAINER_PSYCHIC_LAURA"]}],
        "Lost Cave B1F Room 10": [{"name": "Lady Selphy", "data_ids": ["TRAINER_LADY_SELPHY"]}],
        "Water Path South": [{"name": "Juggler Edward", "data_ids": ["TRAINER_JUGGLER_EDWARD"]},
                             {"name": "Hiker Earl", "data_ids": ["TRAINER_HIKER_EARL"]}],
        "Water Path South Water": [{"name": "Swimmer Denise", "data_ids": ["TRAINER_SWIMMER_FEMALE_DENISE"]},
                                   {"name": "Swimmer Samir", "data_ids": ["TRAINER_SWIMMER_MALE_SAMIR"]}],
        "Water Path North": [{"name": "Twins Miu & Mia", "data_ids": ["TRAINER_TWINS_MIU_MIA"]},
                             {"name": "Aroma Lady Rose", "data_ids": ["TRAINER_AROMA_LADY_ROSE"]}],
        "Ruin Valley": [{"name": "Hiker Daryl", "data_ids": ["TRAINER_HIKER_DARYL"]},
                        {"name": "PokeManiac Hector", "data_ids": ["TRAINER_POKEMANIAC_HECTOR"]},
                        {"name": "Ruin Maniac Stanly", "data_ids": ["TRAINER_RUIN_MANIAC_STANLY"]},
                        {"name": "Ruin Maniac Foster", "data_ids": ["TRAINER_RUIN_MANIAC_FOSTER"]},
                        {"name": "Ruin Maniac Larry", "data_ids": ["TRAINER_RUIN_MANIAC_LARRY"]}],
        "Pattern Bush": [{"name": "Youngster Cordell", "data_ids": ["TRAINER_YOUNGSTER_CORDELL"]},
                         {"name": "Pokemon Breeder Bethany", "data_ids": ["TRAINER_PKMN_BREEDER_BETHANY"]},
                         {"name": "Bug Catcher Garret", "data_ids": ["TRAINER_BUG_CATCHER_GARRET"]},
                         {"name": "Lass Joana", "data_ids": ["TRAINER_LASS_JOANA"]},
                         {"name": "Youngster Nash", "data_ids": ["TRAINER_YOUNGSTER_NASH"]},
                         {"name": "Bug Catcher Vance", "data_ids": ["TRAINER_BUG_CATCHER_VANCE"]},
                         {"name": "Ruin Maniac Layton", "data_ids": ["TRAINER_RUIN_MANIAC_LAYTON"]},
                         {"name": "Picnicker Marcy", "data_ids": ["TRAINER_PICNICKER_MARCY"]},
                         {"name": "Bug Catcher Jonah", "data_ids": ["TRAINER_BUG_CATCHER_JONAH"]},
                         {"name": "Lass Dalia", "data_ids": ["TRAINER_LASS_DALIA"]},
                         {"name": "Pokemon Breeder Allison", "data_ids": ["TRAINER_PKMN_BREEDER_ALLISON"]},
                         {"name": "Camper Riley", "data_ids": ["TRAINER_CAMPER_RILEY"]}],
        "Green Path Water": [{"name": "Psychic Jaclyn", "data_ids": ["TRAINER_PSYCHIC_JACLYN"]}],
        "Outcast Island Water": [{"name": "Swimmer Nicole", "data_ids": ["TRAINER_SWIMMER_FEMALE_NICOLE"]},
                                 {"name": "Sis and Bro Ava & Geb", "data_ids": ["TRAINER_SIS_AND_BRO_AVA_GEB"]},
                                 {"name": "Swimmer Mymo", "data_ids": ["TRAINER_SWIMMER_MALE_MYMO"]},
                                 {"name": "Fisherman Tylor", "data_ids": ["TRAINER_FISHERMAN_TYLOR"]}],
        "Outcast Island": [{"name": "Team Rocket Grunt 46", "data_ids": ["TRAINER_TEAM_ROCKET_GRUNT_46"]}],
        "Canyon Entrance": [{"name": "Aroma Lady Miah", "data_ids": ["TRAINER_AROMA_LADY_MIAH"]},
                            {"name": "Juggler Mason", "data_ids": ["TRAINER_JUGGLER_MASON"]},
                            {"name": "Pokemon Ranger Nicolas", "data_ids": ["TRAINER_PKMN_RANGER_NICOLAS"]},
                            {"name": "Pokemon Ranger Madeline", "data_ids": ["TRAINER_PKMN_RANGER_MADELINE"]},
                            {"name": "Young Couple Eve & Jon", "data_ids": ["TRAINER_YOUNG_COUPLE_EVE_JON"]}],
        "Sevault Canyon": [{"name": "Cool Couple Lex & Nya", "data_ids": ["TRAINER_COOL_COUPLE_LEX_NYA"]},
                           {"name": "Tamer Evan", "data_ids": ["TRAINER_TAMER_EVAN"]},
                           {"name": "Pokemon Ranger Jackson", "data_ids": ["TRAINER_PKMN_RANGER_JACKSON"]},
                           {"name": "Pokemon Ranger Katelyn", "data_ids": ["TRAINER_PKMN_RANGER_KATELYN"]},
                           {"name": "Crush Girl Cyndy", "data_ids": ["TRAINER_CRUSH_GIRL_CYNDY"]},
                           {"name": "Cooltrainer Leroy", "data_ids": ["TRAINER_COOLTRAINER_LEROY"]},
                           {"name": "Cooltrainer Michelle", "data_ids": ["TRAINER_COOLTRAINER_MICHELLE"]}],
        "Tanoby Ruins Scufib Island": [{"name": "Ruin Maniac Brandon", "data_ids": ["TRAINER_RUIN_MANIAC_BRANDON"]}],
        "Tanoby Ruins Weepth Island": [{"name": "Gentleman Clifford", "data_ids": ["TRAINER_GENTLEMAN_CLIFFORD"]},
                                       {"name": "Painter Edna", "data_ids": ["TRAINER_PAINTER_EDNA"]}],
        "Tanoby Ruins Monean Island": [{"name": "Ruin Maniac Benjamin", "data_ids": ["TRAINER_RUIN_MANIAC_BENJAMIN"]}],
        "Trainer Tower Exterior South": [{"name": "Psychic Rodette", "data_ids": ["TRAINER_PSYCHIC_RODETTE"]},
                                         {"name": "Psychic Dario", "data_ids": ["TRAINER_PSYCHIC_DARIO"]}],
        "Elite Four Rematch": [{"name": "Elite Four Rematch",
                                "connections": ["Pokemon League Lorelei's Room", "Pokemon League Bruno's Room",
                                                "Pokemon League Agatha's Room", "Pokemon League Lance's Room",
                                                "Pokemon League Champion's Room"],
                                "data_ids": ["TRAINER_ELITE_FOUR_LORELEI_2", "TRAINER_ELITE_FOUR_BRUNO_2",
                                             "TRAINER_ELITE_FOUR_AGATHA_2", "TRAINER_ELITE_FOUR_LANCE_2",
                                             "TRAINER_CHAMPION_REMATCH_BULBASAUR",
                                             "TRAINER_CHAMPION_REMATCH_CHARMANDER",
                                             "TRAINER_CHAMPION_REMATCH_SQUIRTLE"]}]
    }

    kanto_wild_encounter_data = {
        "Route 1 Land Encounters": [{"name": "Route 1 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE1"]}],
        "Route 22 Land Encounters": [{"name": "Route 22 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE22"]}],
        "Route 2 Land Encounters": [{"name": "Route 2 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE2"]}],
        "Viridian Forest Land Encounters": [{"name": "Viridian Forest Land Scaling", "type": "Land",
                                             "data_ids": ["MAP_VIRIDIAN_FOREST"]}],
        "Route 3 Land Encounters": [{"name": "Route 3 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE3"]}],
        "Mt. Moon 1F Land Encounters": [{"name": "Mt. Moon 1F Land Scaling", "type": "Land",
                                         "data_ids": ["MAP_MT_MOON_1F"]}],
        "Mt. Moon B1F Land Encounters": [{"name": "Mt. Moon B1F Land Scaling", "type": "Land",
                                          "data_ids": ["MAP_MT_MOON_B1F"]}],
        "Mt. Moon B2F Land Encounters": [{"name": "Mt. Moon B2F Land Scaling", "type": "Land",
                                          "data_ids": ["MAP_MT_MOON_B2F"]}],
        "Route 4 Land Encounters": [{"name": "Route 4 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE4"]}],
        "Route 24 Land Encounters": [{"name": "Route 24 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE24"]}],
        "Route 25 Land Encounters": [{"name": "Route 25 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE25"]}],
        "Route 5 Land Encounters": [{"name": "Route 5 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE5"]}],
        "Route 6 Land Encounters": [{"name": "Route 6 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE6"]}],
        "Route 11 Land Encounters": [{"name": "Route 11 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE11"]}],
        "Diglett's Cave B1F Land Encounters": [{"name": "Diglett's Cave B1F Land Scaling", "type": "Land",
                                                "data_ids": ["MAP_DIGLETTS_CAVE_B1F"]}],
        "Route 9 Land Encounters": [{"name": "Route 9 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE9"]}],
        "Route 10 Land Encounters": [{"name": "Route 10 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE10"]}],
        "Rock Tunnel 1F Land Encounters": [{"name": "Rock Tunnel 1F Land Scaling", "type": "Land",
                                            "data_ids": ["MAP_ROCK_TUNNEL_1F"]}],
        "Rock Tunnel B1F Land Encounters": [{"name": "Rock Tunnel B1F Land Scaling", "type": "Land",
                                             "data_ids": ["MAP_ROCK_TUNNEL_B1F"]}],
        "Power Plant Land Encounters": [{"name": "Power Plant Land Scaling", "type": "Land",
                                         "data_ids": ["MAP_POWER_PLANT"]}],
        "Pokemon Tower 3F Land Encounters": [{"name": "Pokemon Tower 3F Land Scaling", "type": "Land",
                                              "data_ids": ["MAP_POKEMON_TOWER_3F"]}],
        "Pokemon Tower 4F Land Encounters": [{"name": "Pokemon Tower 4F Land Scaling", "type": "Land",
                                              "data_ids": ["MAP_POKEMON_TOWER_4F"]}],
        "Pokemon Tower 5F Land Encounters": [{"name": "Pokemon Tower 5F Land Scaling", "type": "Land",
                                              "data_ids": ["MAP_POKEMON_TOWER_5F"]}],
        "Pokemon Tower 6F Land Encounters": [{"name": "Pokemon Tower 6F Land Scaling", "type": "Land",
                                              "data_ids": ["MAP_POKEMON_TOWER_6F"]}],
        "Pokemon Tower 7F Land Encounters": [{"name": "Pokemon Tower 7F Land Scaling", "type": "Land",
                                              "data_ids": ["MAP_POKEMON_TOWER_7F"]}],
        "Route 8 Land Encounters": [{"name": "Route 8 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE8"]}],
        "Route 7 Land Encounters": [{"name": "Route 7 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE7"]}],
        "Route 12 Land Encounters": [{"name": "Route 12 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE12"]}],
        "Route 13 Land Encounters": [{"name": "Route 13 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE13"]}],
        "Route 14 Land Encounters": [{"name": "Route 14 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE14"]}],
        "Route 15 Land Encounters": [{"name": "Route 15 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE15"]}],
        "Route 16 Land Encounters": [{"name": "Route 16 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE16"]}],
        "Route 17 Land Encounters": [{"name": "Route 17 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE17"]}],
        "Route 18 Land Encounters": [{"name": "Route 18 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE18"]}],
        "Safari Zone Center Area Land Encounters": [{"name": "Safari Zone Center Area Land Scaling", "type": "Land",
                                                     "data_ids": ["MAP_SAFARI_ZONE_CENTER"]}],
        "Safari Zone East Area Land Encounters": [{"name": "Safari Zone East Area Land Scaling", "type": "Land",
                                                   "data_ids": ["MAP_SAFARI_ZONE_EAST"]}],
        "Safari Zone North Area Land Encounters": [{"name": "Safari Zone North Area Land Scaling", "type": "Land",
                                                    "data_ids": ["MAP_SAFARI_ZONE_NORTH"]}],
        "Safari Zone West Area Land Encounters": [{"name": "Safari Zone West Area Land Scaling", "type": "Land",
                                                   "data_ids": ["MAP_SAFARI_ZONE_WEST"]}],
        "Seafoam Islands 1F Land Encounters": [{"name": "Seafoam Islands 1F Land Scaling", "type": "Land",
                                                "data_ids": ["MAP_SEAFOAM_ISLANDS_1F"]}],
        "Seafoam Islands B1F Land Encounters": [{"name": "Seafoam Islands B1F Land Scaling", "type": "Land",
                                                 "data_ids": ["MAP_SEAFOAM_ISLANDS_B1F"]}],
        "Seafoam Islands B2F Land Encounters": [{"name": "Seafoam Islands B2F Land Scaling", "type": "Land",
                                                 "data_ids": ["MAP_SEAFOAM_ISLANDS_B2F"]}],
        "Seafoam Islands B3F Land Encounters": [{"name": "Seafoam Islands B3F Land Scaling", "type": "Land",
                                                 "data_ids": ["MAP_SEAFOAM_ISLANDS_B3F"]}],
        "Seafoam Islands B4F Land Encounters": [{"name": "Seafoam Islands B4F Land Scaling", "type": "Land",
                                                 "data_ids": ["MAP_SEAFOAM_ISLANDS_B4F"]}],
        "Pokemon Mansion 1F Land Encounters": [{"name": "Pokemon Mansion 1F Land Scaling", "type": "Land",
                                                "data_ids": ["MAP_POKEMON_MANSION_1F"]}],
        "Pokemon Mansion 2F Land Encounters": [{"name": "Pokemon Mansion 2F Land Scaling", "type": "Land",
                                                "data_ids": ["MAP_POKEMON_MANSION_2F"]}],
        "Pokemon Mansion 3F Land Encounters": [{"name": "Pokemon Mansion 3F Land Scaling", "type": "Land",
                                                "data_ids": ["MAP_POKEMON_MANSION_3F"]}],
        "Pokemon Mansion B1F Land Encounters": [{"name": "Pokemon Mansion B1F Land Scaling", "type": "Land",
                                                 "data_ids": ["MAP_POKEMON_MANSION_B1F"]}],
        "Route 21 Land Encounters": [{"name": "Route 21 Land Scaling", "type": "Land",
                                      "data_ids": ["MAP_ROUTE21_NORTH", "MAP_ROUTE21_SOUTH"]}],
        "Route 23 Land Encounters": [{"name": "Route 23 Land Scaling", "type": "Land", "data_ids": ["MAP_ROUTE23"]}],
        "Victory Road 1F Land Encounters": [{"name": "Victory Road 1F Land Scaling", "type": "Land",
                                             "data_ids": ["MAP_VICTORY_ROAD_1F"]}],
        "Victory Road 2F Land Encounters": [{"name": "Victory Road 2F Land Scaling", "type": "Land",
                                             "data_ids": ["MAP_VICTORY_ROAD_2F"]}],
        "Victory Road 3F Land Encounters": [{"name": "Victory Road 3F Land Scaling", "type": "Land",
                                             "data_ids": ["MAP_VICTORY_ROAD_3F"]}],
        "Cerulean Cave 1F Land Encounters": [{"name": "Cerulean Cave 1F Land Scaling", "type": "Land",
                                              "data_ids": ["MAP_CERULEAN_CAVE_1F"]}],
        "Cerulean Cave 2F Land Encounters": [{"name": "Cerulean Cave 2F Land Scaling", "type": "Land",
                                              "data_ids": ["MAP_CERULEAN_CAVE_2F"]}],
        "Cerulean Cave B1F Land Encounters": [{"name": "Cerulean Cave B1F Land Scaling", "type": "Land",
                                               "data_ids": ["MAP_CERULEAN_CAVE_B1F"]}],
        "Pallet/Cinnabar/Rt 19,20,21 Water Encounters": [{"name": "Pallet/Cinnabar/Rt 19,20,21 Water Scaling",
                                                          "type": "Water",
                                                          "connections": ["Pallet Town Water Encounters",
                                                                          "Cinnabar Island Water Encounters",
                                                                          "Route 19 Water Encounters",
                                                                          "Route 20 Water Encounters",
                                                                          "Route 21 Water Encounters"],
                                                          "data_ids": ["MAP_PALLET_TOWN", "MAP_CINNABAR_ISLAND",
                                                                       "MAP_ROUTE19", "MAP_ROUTE20",
                                                                       "MAP_ROUTE21_NORTH", "MAP_ROUTE21_SOUTH"]}],
        "Viridian/Rt 22 Water Encounters": [{"name": "Viridian/Rt 22 Water Scaling", "type": "Water",
                                             "connections": ["Viridian City Water Encounters",
                                                             "Route 22 Water Encounters"],
                                             "data_ids": ["MAP_VIRIDIAN_CITY", "MAP_ROUTE22"]}],
        "Cerulean/Rt 4,24 Water Encounters": [{"name": "Cerulean/Rt 4,24 Water Scaling", "type": "Water",
                                               "connections": ["Cerulean City Water Encounters",
                                                               "Route 4 Water Encounters", "Route 24 Water Encounters"],
                                               "data_ids": ["MAP_CERULEAN_CITY", "MAP_ROUTE4", "MAP_ROUTE24"]}],
        "Route 25 Water Encounters": [{"name": "Route 25 Water Scaling", "type": "Water", "data_ids": ["MAP_ROUTE25"]}],
        "Route 6 Water Encounters": [{"name": "Route 6 Water Scaling", "type": "Water", "data_ids": ["MAP_ROUTE6"]}],
        "Vermilion/Rt 11 Water Encounters": [{"name": "Vermilion/Rt 11 Water Scaling", "type": "Water",
                                              "connections": ["Vermilion City Water Encounters",
                                                              "Route 11 Water Encounters"],
                                              "data_ids": ["MAP_VERMILION_CITY", "MAP_ROUTE11"]}],
        "S.S. Anne Exterior Water Encounters": [{"name": "S.S. Anne Exterior Water Scaling", "type": "Water",
                                                 "data_ids": ["MAP_SSANNE_EXTERIOR"]}],
        "Route 10 Water Encounters": [{"name": "Route 10 Water Scaling", "type": "Water", "data_ids": ["MAP_ROUTE10"]}],
        "Celadon City Water Encounters": [{"name": "Celadon City Water Scaling", "type": "Water",
                                           "data_ids": ["MAP_CELADON_CITY"]}],
        "Rt 12,13 Water Encounters": [{"name": "Rt 12,13 Water Scaling", "type": "Water",
                                       "connections": ["Route 12 Water Encounters", "Route 13 Water Encounters"],
                                       "data_ids": ["MAP_ROUTE12", "MAP_ROUTE13"]}],
        "Fuchsia City Water Encounters": [{"name": "Fuchsia City Water Scaling", "type": "Water",
                                           "data_ids": ["MAP_FUCHSIA_CITY"]}],
        "Safari Zone Center Area Water Encounters": [{"name": "Safari Zone Center Area Water Scaling", "type": "Water",
                                                      "data_ids": ["MAP_SAFARI_ZONE_CENTER"]}],
        "Safari Zone East Area Water Encounters": [{"name": "Safari Zone East Area Water Scaling", "type": "Water",
                                                    "data_ids": ["MAP_SAFARI_ZONE_EAST"]}],
        "Safari Zone North Area Water Encounters": [{"name": "Safari Zone North Area Water Scaling", "type": "Water",
                                                     "data_ids": ["MAP_SAFARI_ZONE_NORTH"]}],
        "Safari Zone West Area Water Encounters": [{"name": "Safari Zone West Area Water Scaling", "type": "Water",
                                                    "data_ids": ["MAP_SAFARI_ZONE_WEST"]}],
        "Seafoam Islands B3F Water Encounters": [{"name": "Seafoam Islands B3F Water Scaling", "type": "Water",
                                                  "data_ids": ["MAP_SEAFOAM_ISLANDS_B3F"]}],
        "Seafoam Islands B4F Water Encounters": [{"name": "Seafoam Islands B4F Water Scaling", "type": "Water",
                                                  "data_ids": ["MAP_SEAFOAM_ISLANDS_B4F"]}],
        "Route 23 Water Encounters": [{"name": "Route 23 Water Scaling", "type": "Water", "data_ids": ["MAP_ROUTE23"]}],
        "Cerulean Cave 1F Water Encounters": [{"name": "Cerulean Cave 1F Water Scaling", "type": "Water",
                                               "data_ids": ["MAP_CERULEAN_CAVE_1F"]}],
        "Cerulean Cave B1F Water Encounters": [{"name": "Cerulean Cave B1F Water Scaling", "type": "Water",
                                                "data_ids": ["MAP_CERULEAN_CAVE_B1F"]}],
        "Fishing Encounters": [{"name": "Fishing Scaling", "type": "Fishing",
                                "connections": ["Pallet Town Fishing Encounters", "Viridian City Fishing Encounters",
                                                "Cerulean City Fishing Encounters", "Vermilion City Fishing Encounters",
                                                "Celadon City Fishing Encounters", "Fuchsia City Fishing Encounters",
                                                "Cinnabar Island Fishing Encounters",
                                                "S.S. Anne Exterior Fishing Encounters",
                                                "Safari Zone Center Area Fishing Encounters",
                                                "Safari Zone East Area Fishing Encounters",
                                                "Safari Zone North Area Fishing Encounters",
                                                "Safari Zone West Area Fishing Encounters",
                                                "Seafoam Islands B3F Fishing Encounters",
                                                "Seafoam Islands B4F Fishing Encounters",
                                                "Cerulean Cave 1F Fishing Encounters",
                                                "Cerulean Cave B1F Fishing Encounters",
                                                "Route 4 Fishing Encounters", "Route 6 Fishing Encounters",
                                                "Route 10 Fishing Encounters", "Route 11 Fishing Encounters",
                                                "Route 12 Fishing Encounters", "Route 13 Fishing Encounters",
                                                "Route 19 Fishing Encounters", "Route 20 Fishing Encounters",
                                                "Route 21 Fishing Encounters", "Route 22 Fishing Encounters",
                                                "Route 23 Fishing Encounters", "Route 24 Fishing Encounters",
                                                "Route 25 Fishing Encounters"],
                                "data_ids": ["MAP_PALLET_TOWN", "MAP_VIRIDIAN_CITY", "MAP_CERULEAN_CITY",
                                             "MAP_VERMILION_CITY", "MAP_CELADON_CITY", "MAP_FUCHSIA_CITY",
                                             "MAP_CINNABAR_ISLAND", "MAP_SSANNE_EXTERIOR", "MAP_SAFARI_ZONE_CENTER",
                                             "MAP_SAFARI_ZONE_EAST", "MAP_SAFARI_ZONE_NORTH", "MAP_SAFARI_ZONE_WEST",
                                             "MAP_SEAFOAM_ISLANDS_B3F", "MAP_SEAFOAM_ISLANDS_B4F",
                                             "MAP_CERULEAN_CAVE_1F", "MAP_CERULEAN_CAVE_B1F", "MAP_ROUTE4",
                                             "MAP_ROUTE6", "MAP_ROUTE10", "MAP_ROUTE11", "MAP_ROUTE12", "MAP_ROUTE13",
                                             "MAP_ROUTE19", "MAP_ROUTE20", "MAP_ROUTE21_NORTH", "MAP_ROUTE21_SOUTH",
                                             "MAP_ROUTE22", "MAP_ROUTE23", "MAP_ROUTE24", "MAP_ROUTE25"]}]
    }

    sevii_wild_encounter_data = {
        "Treasure Beach Land Encounters": [{"name": "Treasure Beach Land Scaling", "type": "Land",
                                            "data_ids": ["MAP_ONE_ISLAND_TREASURE_BEACH"]}],
        "Kindle Road Land Encounters": [{"name": "Kindle Road Land Scaling", "type": "Land",
                                         "data_ids": ["MAP_ONE_ISLAND_KINDLE_ROAD"]}],
        "Mt. Ember Exterior Land Encounters": [{"name": "Mt. Ember Exterior Land Scaling", "type": "Land",
                                                "data_ids": ["MAP_MT_EMBER_EXTERIOR"]}],
        "Mt. Ember Summit Path 1F Land Encounters": [{"name": "Mt. Ember Summit Path 1F Land Scaling", "type": "Land",
                                                      "data_ids": ["MAP_MT_EMBER_SUMMIT_PATH_1F"]}],
        "Mt. Ember Summit Path 2F Land Encounters": [{"name": "Mt. Ember Summit Path 2F Land Scaling", "type": "Land",
                                                      "data_ids": ["MAP_MT_EMBER_SUMMIT_PATH_2F"]}],
        "Mt. Ember Summit Path 3F Land Encounters": [{"name": "Mt. Ember Summit Path 3F Land Scaling", "type": "Land",
                                                      "data_ids": ["MAP_MT_EMBER_SUMMIT_PATH_3F"]}],
        "Mt. Ember Ruby Path 1F Land Encounters": [{"name": "Mt. Ember Ruby Path 1F Land Scaling", "type": "Land",
                                                    "data_ids": ["MAP_MT_EMBER_RUBY_PATH_1F"]}],
        "Mt. Ember Ruby Path B1F Land Encounters": [{"name": "Mt. Ember Ruby Path B1F Land Scaling", "type": "Land",
                                                     "data_ids": ["MAP_MT_EMBER_RUBY_PATH_B1F"]}],
        "Mt. Ember Ruby Path B1F Return Land Encounters": [{"name": "Mt. Ember Ruby Path B1F Return Land Scaling",
                                                            "type": "Land",
                                                            "data_ids": ["MAP_MT_EMBER_RUBY_PATH_B1F_STAIRS"]}],
        "Mt. Ember Ruby Path B2F Land Encounters": [{"name": "Mt. Ember Ruby Path B2F Land Scaling", "type": "Land",
                                                     "data_ids": ["MAP_MT_EMBER_RUBY_PATH_B2F"]}],
        "Mt. Ember Ruby Path B2F Return Land Encounters": [{"name": "Mt. Ember Ruby Path B2F Return Land Scaling",
                                                            "type": "Land",
                                                            "data_ids": ["MAP_MT_EMBER_RUBY_PATH_B2F_STAIRS"]}],
        "Mt. Ember Ruby Path B3F Land Encounters": [{"name": "Mt. Ember Ruby Path B3F Land Scaling", "type": "Land",
                                                     "data_ids": ["MAP_MT_EMBER_RUBY_PATH_B3F"]}],
        "Cape Brink Land Encounters": [{"name": "Cape Brink Land Scaling", "type": "Land",
                                        "data_ids": ["MAP_TWO_ISLAND_CAPE_BRINK"]}],
        "Three Isle Port Land Encounters": [{"name": "Three Isle Port Land Scaling", "type": "Land",
                                             "data_ids": ["MAP_THREE_ISLAND_PORT"]}],
        "Bond Bridge Land Encounters": [{"name": "Bond Bridge Land Scaling", "type": "Land",
                                         "data_ids": ["MAP_THREE_ISLAND_BOND_BRIDGE"]}],
        "Berry Forest Land Encounters": [{"name": "Berry Forest Land Scaling", "type": "Land",
                                          "data_ids": ["MAP_THREE_ISLAND_BERRY_FOREST"]}],
        "Icefall Cave Front Land Encounters": [{"name": "Icefall Cave Front Land Scaling", "type": "Land",
                                                "data_ids": ["MAP_FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE"]}],
        "Icefall Cave 1F Land Encounters": [{"name": "Icefall Cave 1F Land Scaling", "type": "Land",
                                             "data_ids": ["MAP_FOUR_ISLAND_ICEFALL_CAVE_1F"]}],
        "Icefall Cave B1F Land Encounters": [{"name": "Icefall Cave B1F Land Scaling", "type": "Land",
                                              "data_ids": ["MAP_FOUR_ISLAND_ICEFALL_CAVE_B1F"]}],
        "Icefall Cave Back Land Encounters": [{"name": "Icefall Cave Back Land Scaling", "type": "Land",
                                               "data_ids": ["MAP_FOUR_ISLAND_ICEFALL_CAVE_BACK"]}],
        "Five Isle Meadow Land Encounters": [{"name": "Five Isle Meadow Land Scaling", "type": "Land",
                                              "data_ids": ["MAP_FIVE_ISLAND_MEADOW"]}],
        "Memorial Pillar Land Encounters": [{"name": "Memorial Pillar Land Scaling", "type": "Land",
                                             "data_ids": ["MAP_FIVE_ISLAND_MEMORIAL_PILLAR"]}],
        "Lost Cave B1F Room 1 Land Encounters": [{"name": "Lost Cave Room 1 Land Scaling", "type": "Land",
                                                  "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM1"]}],
        "Lost Cave B1F Room 2 Land Encounters": [{"name": "Lost Cave Room 2 Land Scaling", "type": "Land",
                                                  "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM2"]}],
        "Lost Cave B1F Room 3 Land Encounters": [{"name": "Lost Cave Room 3 Land Scaling", "type": "Land",
                                                  "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM3"]}],
        "Lost Cave B1F Room 4 Land Encounters": [{"name": "Lost Cave Room 4 Land Scaling", "type": "Land",
                                                  "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM4"]}],
        "Lost Cave B1F Room 5 Land Encounters": [{"name": "Lost Cave Room 5 Land Scaling", "type": "Land",
                                                  "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM5"]}],
        "Lost Cave B1F Room 6 Land Encounters": [{"name": "Lost Cave Room 6 Land Scaling", "type": "Land",
                                                  "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM6"]}],
        "Lost Cave B1F Room 7 Land Encounters": [{"name": "Lost Cave Room 7 Land Scaling", "type": "Land",
                                                  "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM7"]}],
        "Lost Cave B1F Room 8 Land Encounters": [{"name": "Lost Cave Room 8 Land Scaling", "type": "Land",
                                                  "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM8"]}],
        "Lost Cave B1F Room 9 Land Encounters": [{"name": "Lost Cave Room 9 Land Scaling", "type": "Land",
                                                  "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM9"]}],
        "Lost Cave B1F Room 10 Land Encounters": [{"name": "Lost Cave Room 10 Land Scaling", "type": "Land",
                                                   "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM10"]}],
        "Lost Cave B1F Room 11 Land Encounters": [{"name": "Lost Cave Room 11 Land Scaling", "type": "Land",
                                                   "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM11"]}],
        "Lost Cave B1F Room 12 Land Encounters": [{"name": "Lost Cave Room 12 Land Scaling", "type": "Land",
                                                   "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM12"]}],
        "Lost Cave B1F Room 13 Land Encounters": [{"name": "Lost Cave Room 13 Land Scaling", "type": "Land",
                                                   "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM13"]}],
        "Lost Cave B1F Room 14 Land Encounters": [{"name": "Lost Cave Room 14 Land Scaling", "type": "Land",
                                                   "data_ids": ["MAP_FIVE_ISLAND_LOST_CAVE_ROOM14"]}],
        "Water Path Land Encounters": [{"name": "Water Path Land Scaling", "type": "Land",
                                        "data_ids": ["MAP_SIX_ISLAND_WATER_PATH"]}],
        "Ruin Valley Land Encounters": [{"name": "Ruin Valley Land Scaling", "type": "Land",
                                         "data_ids": ["MAP_SIX_ISLAND_RUIN_VALLEY"]}],
        "Pattern Bush Land Encounters": [{"name": "Pattern Bush Land Scaling", "type": "Land",
                                          "data_ids": ["MAP_SIX_ISLAND_PATTERN_BUSH"]}],
        "Altering Cave Land Encounters": [{"name": "Altering Cave Land Scaling", "type": "Land",
                                           "data_ids": ["MAP_SIX_ISLAND_ALTERING_CAVE"]}],
        "Canyon Entrance Land Encounters": [{"name": "Canyon Entrance Land Scaling", "type": "Land",
                                             "data_ids": ["MAP_SEVEN_ISLAND_SEVAULT_CANYON_ENTRANCE"]}],
        "Sevault Canyon Land Encounters": [{"name": "Sevault Canyon Land Scaling", "type": "Land",
                                            "data_ids": ["MAP_SEVEN_ISLAND_SEVAULT_CANYON"]}],
        "Monean Chamber Land Encounters": [{"name": "Monean Chamber Land Scaling", "type": "Land",
                                            "data_ids": ["MAP_SEVEN_ISLAND_TANOBY_RUINS_MONEAN_CHAMBER"]}],
        "Liptoo Chamber Land Encounters": [{"name": "Liptoo Chamber Land Scaling", "type": "Land",
                                            "data_ids": ["MAP_SEVEN_ISLAND_TANOBY_RUINS_LIPTOO_CHAMBER"]}],
        "Weepth Chamber Land Encounters": [{"name": "Weepth Chamber Land Scaling", "type": "Land",
                                            "data_ids": ["MAP_SEVEN_ISLAND_TANOBY_RUINS_WEEPTH_CHAMBER"]}],
        "Dilford Chamber Land Encounters": [{"name": "Dilford Chamber Land Scaling", "type": "Land",
                                             "data_ids": ["MAP_SEVEN_ISLAND_TANOBY_RUINS_DILFORD_CHAMBER"]}],
        "Scufib Chamber Land Encounters": [{"name": "Scufib Chamber Land Scaling", "type": "Land",
                                            "data_ids": ["MAP_SEVEN_ISLAND_TANOBY_RUINS_SCUFIB_CHAMBER"]}],
        "Rixy Chamber Land Encounters": [{"name": "Rixy Chamber Land Scaling", "type": "Land",
                                          "data_ids": ["MAP_SEVEN_ISLAND_TANOBY_RUINS_RIXY_CHAMBER"]}],
        "Viapos Chamber Land Encounters": [{"name": "Viapos Chamber Land Scaling", "type": "Land",
                                            "data_ids": ["MAP_SEVEN_ISLAND_TANOBY_RUINS_VIAPOIS_CHAMBER"]}],
        "One Island Water Encounters": [{"name": "One Island Water Scaling", "type": "Water",
                                         "connections": ["One Island Town Water Encounters",
                                                         "Treasure Beach Water Encounters",
                                                         "Kindle Road Water Encounters"],
                                         "data_ids": ["MAP_ONE_ISLAND", "MAP_ONE_ISLAND_TREASURE_BEACH",
                                                      "MAP_ONE_ISLAND_KINDLE_ROAD"]}],
        "Cape Brink Water Encounters": [{"name": "Cape Brink Water Scaling", "type": "Water",
                                         "data_ids": ["MAP_TWO_ISLAND_CAPE_BRINK"]}],
        "Bond Bridge Water Encounters": [{"name": "Bond Bridge Water Scaling", "type": "Water",
                                          "data_ids": ["MAP_THREE_ISLAND_BOND_BRIDGE"]}],
        "Berry Forest Water Encounters": [{"name": "Berry Forest Water Scaling", "type": "Water",
                                           "data_ids": ["MAP_THREE_ISLAND_BERRY_FOREST"]}],
        "Four Island Town Water Encounters": [{"name": "Four Island Town Water Scaling", "type": "Water",
                                               "data_ids": ["MAP_FOUR_ISLAND"]}],
        "Icefall Cave Front Water Encounters": [{"name": "Icefall Cave Front Water Scaling", "type": "Water",
                                                 "data_ids": ["MAP_FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE"]}],
        "Icefall Cave Back Water Encounters": [{"name": "Icefall Cave Back Water Scaling", "type": "Water",
                                                "data_ids": ["MAP_FOUR_ISLAND_ICEFALL_CAVE_BACK"]}],
        "Five Island Water Encounters": [{"name": "Five Island Water Scaling", "type": "Water",
                                          "connections": ["Five Island Town Water Encounters",
                                                          "Five Isle Meadow Water Encounters",
                                                          "Memorial Pillar Water Encounters",
                                                          "Water Labyrinth Water Encounters",
                                                          "Resort Gorgeous Water Encounters"],
                                          "data_ids": ["MAP_FIVE_ISLAND", "MAP_FIVE_ISLAND_MEADOW",
                                                       "MAP_FIVE_ISLAND_MEMORIAL_PILLAR",
                                                       "MAP_FIVE_ISLAND_WATER_LABYRINTH",
                                                       "MAP_FIVE_ISLAND_RESORT_GORGEOUS"]}],
        "Water Path Water Encounters": [{"name": "Water Path Water Scaling", "type": "Water",
                                         "data_ids": ["MAP_SIX_ISLAND_WATER_PATH"]}],
        "Ruin Valley Water Encounters": [{"name": "Ruin Valley Water Scaling", "type": "Water",
                                          "data_ids": ["MAP_SIX_ISLAND_RUIN_VALLEY"]}],
        "Six Island Water Encounters": [{"name": "Six Island Water Scaling", "type": "Water",
                                         "connections": ["Green Path Water Encounters",
                                                         "Outcast Island Water Encounters"],
                                         "data_ids": ["MAP_SIX_ISLAND_GREEN_PATH", "MAP_SIX_ISLAND_OUTCAST_ISLAND"]}],
        "Seven Island Water Encounters": [{"name": "Seven Island Water Scaling", "type": "Water",
                                           "connections": ["Tanoby Ruins Water Encounters",
                                                           "Trainer Tower Exterior Water Encounters"],
                                           "data_ids": ["MAP_SEVEN_ISLAND_TANOBY_RUINS",
                                                        "MAP_SEVEN_ISLAND_TRAINER_TOWER"]}],
        "Fishing Encounters": [{"name": "Fishing Scaling", "type": "Fishing",
                                "connections": ["Berry Forest Fishing Encounters",
                                                "Icefall Cave Front Fishing Encounters",
                                                "Icefall Cave Back Fishing Encounters",
                                                "One Island Town Fishing Encounters",
                                                "Treasure Beach Fishing Encounters",
                                                "Kindle Road Fishing Encounters", "Cape Brink Fishing Encounters",
                                                "Bond Bridge Fishing Encounters", "Four Island Town Fishing Encounters",
                                                "Five Island Town Fishing Encounters",
                                                "Five Isle Meadow Fishing Encounters",
                                                "Memorial Pillar Fishing Encounters",
                                                "Water Labyrinth Fishing Encounters",
                                                "Resort Gorgeous Fishing Encounters", "Water Path Fishing Encounters",
                                                "Ruin Valley Fishing Encounters", "Green Path Fishing Encounters",
                                                "Outcast Island Fishing Encounters", "Tanoby Ruins Fishing Encounters",
                                                "Trainer Tower Exterior Fishing Encounters"],
                                "data_ids": ["MAP_THREE_ISLAND_BERRY_FOREST", "MAP_FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE",
                                             "MAP_FOUR_ISLAND_ICEFALL_CAVE_BACK", "MAP_ONE_ISLAND",
                                             "MAP_ONE_ISLAND_TREASURE_BEACH", "MAP_ONE_ISLAND_KINDLE_ROAD",
                                             "MAP_TWO_ISLAND_CAPE_BRINK", "MAP_THREE_ISLAND_BOND_BRIDGE",
                                             "MAP_FOUR_ISLAND", "MAP_FIVE_ISLAND", "MAP_FIVE_ISLAND_MEADOW",
                                             "MAP_FIVE_ISLAND_MEMORIAL_PILLAR", "MAP_FIVE_ISLAND_WATER_LABYRINTH",
                                             "MAP_FIVE_ISLAND_RESORT_GORGEOUS", "MAP_SIX_ISLAND_WATER_PATH",
                                             "MAP_SIX_ISLAND_RUIN_VALLEY", "MAP_SIX_ISLAND_GREEN_PATH",
                                             "MAP_SIX_ISLAND_OUTCAST_ISLAND", "MAP_SEVEN_ISLAND_TANOBY_RUINS",
                                             "MAP_SEVEN_ISLAND_TRAINER_TOWER"]}]
    }

    kanto_static_encounter_data = {
        "Route 4 Pokemon Center 1F": [{"name": "Gift Magikarp", "data_ids": ["GIFT_POKEMON_MAGIKARP"]}],
        "Power Plant": [{"name": "Static Electrode 1", "data_ids": ["STATIC_POKEMON_ELECTRODE_1"]},
                        {"name": "Static Electrode 2", "data_ids": ["STATIC_POKEMON_ELECTRODE_2"]},
                        {"name": "Legendary Zapdos", "data_ids": ["LEGENDARY_POKEMON_ZAPDOS"]}],
        "Pokemon Tower Ghost Encounter": [{"name": "Static Marowak", "data_ids": ["STATIC_POKEMON_MAROWAK"]}],
        "Celadon Game Corner Prize Room": [{"name": "Prize Pokemon 1", "data_ids": ["CELADON_PRIZE_POKEMON_1"]},
                                           {"name": "Prize Pokemon 2", "data_ids": ["CELADON_PRIZE_POKEMON_2"]},
                                           {"name": "Prize Pokemon 3", "data_ids": ["CELADON_PRIZE_POKEMON_3"]},
                                           {"name": "Prize Pokemon 4", "data_ids": ["CELADON_PRIZE_POKEMON_4"]},
                                           {"name": "Prize Pokemon 5", "data_ids": ["CELADON_PRIZE_POKEMON_5"]}],
        "Celadon Condominiums Roof Room": [{"name": "Gift Eevee", "data_ids": ["GIFT_POKEMON_EEVEE"]}],
        "Route 12 Snorlax Area": [{"name": "Static Snorlax 1", "data_ids": ["STATIC_POKEMON_ROUTE12_SNORLAX"]}],
        "Route 16 Snorlax Area": [{"name": "Static Snorlax 2", "data_ids": ["STATIC_POKEMON_ROUTE16_SNORLAX"]}],
        "Saffron Dojo": [{"name": "Gift Hitmonchan", "data_ids": ["GIFT_POKEMON_HITMONCHAN"]},
                         {"name": "Gift Hitmonlee", "data_ids": ["GIFT_POKEMON_HITMONLEE"]}],
        "Silph Co. 7F Northwest Room": [{"name": "Gift Lapras", "data_ids": ["GIFT_POKEMON_LAPRAS"]}],
        "Seafoam Islands B4F Near Articuno": [{"name": "Legendary Articuno",
                                               "data_ids": ["LEGENDARY_POKEMON_ARTICUNO"]}],
        "Pokemon Lab Experiment Room": [{"name": "Gift Omanyte", "data_ids": ["GIFT_POKEMON_OMANYTE"]},
                                        {"name": "Gift Kabuto", "data_ids": ["GIFT_POKEMON_KABUTO"]},
                                        {"name": "Gift Aerodactyl", "data_ids": ["GIFT_POKEMON_AERODACTYL"]}],
        "Cerulean Cave B1F Water": [{"name": "Legendary Mewtwo", "data_ids": ["LEGENDARY_POKEMON_MEWTWO"]}],
        "Navel Rock Summit": [{"name": "Legendary Ho-Oh", "data_ids": ["LEGENDARY_POKEMON_HO_OH"]}],
        "Navel Rock Base": [{"name": "Legendary Lugia", "data_ids": ["LEGENDARY_POKEMON_LUGIA"]}],
        "Birth Island Exterior": [{"name": "Legendary Deoxys", "data_ids": ["LEGENDARY_POKEMON_DEOXYS"]}]
    }

    sevii_static_encounter_data = {
        "Mt. Ember Summit": [{"name": "Legendary Moltres", "data_ids": ["LEGENDARY_POKEMON_MOLTRES"]}],
        "Berry Forest": [{"name": "Static Hypno", "data_ids": ["STATIC_POKEMON_HYPNO"]}]
    }

    def create_scaling_data(region: str, data, tag: str) -> ScalingData:
        scaling_data = ScalingData(
            data["name"],
            region,
            data["type"] if "type" in data else None,
            data["connections"] if "connections" in data else None,
            data["data_ids"],
            frozenset([tag, "Scaling"])
        )
        return scaling_data

    def update_scaling_data(scaling_data: ScalingData, connections: List[str], data_ids: List[str]) -> None:
        scaling_data.connections.extend(connections)
        scaling_data.data_ids.extend(data_ids)

    for region, trainers in kanto_trainer_data.items():
        for trainer in trainers:
            scaling_data = create_scaling_data(region, trainer, "Trainer")
            world.scaling_data.append(scaling_data)

    for region, wild_encounters in kanto_wild_encounter_data.items():
        for wild_encounter in wild_encounters:
            scaling_data = create_scaling_data(region, wild_encounter, "Wild")
            world.scaling_data.append(scaling_data)

    for region, static_encounters in kanto_static_encounter_data.items():
        for static_encounter in static_encounters:
            scaling_data = create_scaling_data(region, static_encounter, "Static")
            world.scaling_data.append(scaling_data)

    if not world.options.kanto_only:
        for region, trainers in sevii_trainer_data.items():
            for trainer in trainers:
                scaling_data = next((data for data in world.scaling_data
                                     if data.name == trainer["name"]), None)
                if scaling_data is not None:
                    update_scaling_data(scaling_data, trainer["connections"], trainer["data_ids"])
                else:
                    scaling_data = create_scaling_data(region, trainer, "Trainer")
                    world.scaling_data.append(scaling_data)

        for region, wild_encounters in sevii_wild_encounter_data.items():
            for wild_encounter in wild_encounters:
                scaling_data = next((data for data in world.scaling_data
                                     if data.name == wild_encounter["name"]), None)
                if scaling_data is not None:
                    update_scaling_data(scaling_data, wild_encounter["connections"], wild_encounter["data_ids"])
                else:
                    scaling_data = create_scaling_data(region, wild_encounter, "Wild")
                    world.scaling_data.append(scaling_data)

        for region, static_encounters in sevii_static_encounter_data.items():
            for static_encounter in static_encounters:
                scaling_data = next((data for data in world.scaling_data
                                     if data.name == static_encounter["name"]), None)
                if scaling_data is not None:
                    update_scaling_data(scaling_data, static_encounter["connections"], static_encounter["data_ids"])
                else:
                    scaling_data = create_scaling_data(region, static_encounter, "Static")
                    world.scaling_data.append(scaling_data)


def level_scaling(multiworld):
    battle_events = ["Route 22 - Early Rival Battle", "Pewter Gym - Gym Leader Battle",
                     "Cerulean Gym - Gym Leader Battle", "Vermilion Gym - Gym Leader Battle",
                     "Celadon Gym - Gym Leader Battle", "Fuchsia Gym - Gym Leader Battle",
                     "Saffron Gym - Gym Leader Battle", "Cinnabar Gym - Gym Leader Battle",
                     "Viridian Gym - Gym Leader Battle", "Champion's Room - Champion Battle",
                     "Champion's Room - Champion Rematch Battle", "Pokemon Tower 7F - Hostage",
                     "Silph Co. 11F - Giovanni Battle", "Berry Forest - Hypno Battle",
                     "Icefall Cave Back - Team Rocket Grunt Battle"]

    level_scaling_required = False
    state = CollectionState(multiworld)
    locations = {loc for loc in multiworld.get_filled_locations()
                 if loc.item.advancement or loc.game == "Pokemon FireRed and LeafGreen" and "Scaling" in loc.tags}
    collected_locations = set()
    spheres = []

    for world in multiworld.get_game_worlds("Pokemon FireRed and LeafGreen"):
        if world.options.level_scaling != LevelScaling.option_off:
            level_scaling_required = True
        else:
            world.finished_level_scaling.set()

    if not level_scaling_required:
        return

    while len(locations) > 0:
        new_spheres: List[Set] = []
        new_battle_events = set()
        battle_events_found = True

        while battle_events_found:
            battle_events_found = False
            events_found = True
            sphere = set()
            old_sphere = set()
            distances = {}

            while events_found:
                events_found = False

                for world in multiworld.get_game_worlds("Pokemon FireRed and LeafGreen"):
                    if world.options.level_scaling != LevelScaling.option_spheres_and_distance:
                        continue
                    regions = {multiworld.get_region("Menu", world.player)}
                    checked_regions = set()
                    distance = 0
                    while regions:
                        update_regions = True
                        while update_regions:
                            update_regions = False
                            same_distance_regions = set()
                            for region in regions:
                                keys = ["Encounter", "Encounters", "Trainers"]
                                encounter_regions = {e.connected_region for e in region.exits
                                                     if e.access_rule(state)
                                                     and any(key in e.connected_region.name for key in keys)}
                                same_distance_regions.update(encounter_regions)
                            regions_len = len(regions)
                            regions.update(same_distance_regions)
                            if len(regions) > regions_len:
                                update_regions = True
                        next_regions = set()
                        for region in regions:
                            if not getattr(region, "distance") or distance < region.distance:
                                region.distance = distance
                            next_regions.update({e.connected_region for e in region.exits if e.connected_region not in
                                                 checked_regions and e.access_rule(state)})
                        checked_regions.update(regions)
                        regions = next_regions
                        distance += 1

                for location in locations:
                    def can_reach():
                        if location.can_reach(state):
                            return True
                        return False

                    if can_reach():
                        sphere.add(location)
                        parent_region = location.parent_region

                        if getattr(parent_region, "distance", None) is None:
                            distance = 0
                        else:
                            distance = parent_region.distance

                        if distance not in distances:
                            distances[distance] = {location}
                        else:
                            distances[distance].add(location)

                locations -= sphere
                old_sphere ^= sphere

                for location in old_sphere:
                    if location.is_event and location.item and location not in collected_locations:
                        if location.name not in battle_events:
                            collected_locations.add(location)
                            state.collect(location.item, True, location)
                            events_found = True
                        else:
                            new_battle_events.add(location)
                            battle_events_found = True

                old_sphere |= sphere

            if sphere:
                for distance in sorted(distances.keys()):
                    new_spheres.append(distances[distance])

            for event in new_battle_events:
                if event.item and event not in collected_locations:
                    collected_locations.add(event)
                    state.collect(event.item, True, event)

        if len(new_spheres) > 0:
            for sphere in new_spheres:
                spheres.append(sphere)

                for location in sphere:
                    if location.item and location not in collected_locations:
                        collected_locations.add(location)
                        state.collect(location.item, True, location)
        else:
            spheres.append(locations)
            break

    for world in multiworld.get_game_worlds("Pokemon FireRed and LeafGreen"):
        if world.options.level_scaling == LevelScaling.option_off:
            continue

        game_version = world.options.game_version.current_key
        e4_rematch_adjustment = 63 / 51
        e4_base_level = 51

        for sphere in spheres:
            scaling_locations = [loc for loc in sphere if loc.player == world.player and "Scaling" in loc.tags]
            trainer_locations = [loc for loc in scaling_locations if "Trainer" in loc.tags]
            encounter_locations = [loc for loc in scaling_locations if "Static" in loc.tags or "Wild" in loc.tags]

            trainer_locations.sort(key=lambda loc: world.trainer_name_list.index(loc.name))
            encounter_locations.sort(key=lambda loc: world.encounter_name_list.index(loc.name))

            for trainer_location in trainer_locations:
                new_base_level = world.trainer_level_list.pop(0)
                old_base_level = world.trainer_name_level_dict[trainer_location.name]

                if trainer_location.name == "Elite Four":
                    e4_base_level = new_base_level
                elif trainer_location.name == "Elite Four Rematch":
                    new_base_level = max(new_base_level, round(e4_base_level * e4_rematch_adjustment))

                for data_id in trainer_location.data_ids:
                    trainer_data = world.modified_trainers[data_id]
                    for pokemon in trainer_data.party.pokemon:
                        new_level = round(min((new_base_level * pokemon.level / old_base_level),
                                              (new_base_level + pokemon.level - old_base_level)))
                        new_level = bound(new_level, 1, 100)
                        pokemon.level = new_level

            for encounter_location in encounter_locations:
                new_base_level = world.encounter_level_list.pop(0)
                old_base_level = world.encounter_name_level_dict[encounter_location.name]

                for data_id in encounter_location.data_ids:
                    if "Static" in encounter_location.tags:
                        pokemon_data = None

                        if data_id in world.modified_misc_pokemon:
                            pokemon_data = world.modified_misc_pokemon[data_id]
                        elif data_id in world.modified_legendary_pokemon:
                            pokemon_data = world.modified_legendary_pokemon[data_id]

                        pokemon_data.level[game_version] = new_base_level
                    elif "Wild" in encounter_location.tags:
                        data_ids = data_id.split()
                        map_data = world.modified_maps[data_ids[0]]
                        encounters = (map_data.land_encounters if "Land" in encounter_location.tags else
                                      map_data.water_encounters if "Water" in encounter_location.tags else
                                      map_data.fishing_encounters)
                        encounter_data = encounters.slots[game_version][int(data_ids[1])]
                        new_max_level = round(max((new_base_level * encounter_data.max_level / old_base_level),
                                                  (new_base_level + encounter_data.max_level - old_base_level)))
                        new_min_level = round(max((new_base_level * encounter_data.min_level / old_base_level),
                                                  (new_base_level + encounter_data.min_level - old_base_level)))
                        new_max_level = bound(new_max_level, 1, 100)
                        new_min_level = bound(new_min_level, 1, 100)
                        encounter_data.max_level = new_max_level
                        encounter_data.min_level = new_min_level

        world.finished_level_scaling.set()

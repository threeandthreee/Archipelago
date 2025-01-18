from typing import NamedTuple


class WeaponData(NamedTuple):
    name: str
    offset: int


CLANK_ZAPPER = WeaponData("Clank Zapper", 9)
BOMB_GLOVE = WeaponData("Bomb Glove", 12)
VISIBOMB_GUN = WeaponData("Visibomb Gun", 14)
SHEEPINATOR = WeaponData("Sheepinator", 16)
DECOY_GLOVE = WeaponData("Decoy Glove", 17)
TESLA_CLAW = WeaponData("Tesla Claw", 18)
CHOPPER = WeaponData("Chopper", 22)
PULSE_RIFLE = WeaponData("Pulse Rifle", 23)
SEEKER_GUN = WeaponData("Seeker Gun", 24)
HOVERBOMB_GUN = WeaponData("Hoverbomb Gun", 25)
BLITZ_GUN = WeaponData("Blitz Gun", 26)
MINIROCKET_TUBE = WeaponData("Minirocket Tube", 27)
PLASMA_COIL = WeaponData("Plasma Coil", 28)
LAVA_GUN = WeaponData("Lava Gun", 29)
LANCER = WeaponData("Lancer", 30)
SYNTHENOID = WeaponData("Synthenoid", 31)
SPIDERBOT_GLOVE = WeaponData("Spiderbot Glove", 32)
BOUNCER = WeaponData("Bouncer", 37)
MINITURRET_GLOVE = WeaponData("Miniturret Glove", 41)
GRAVITY_BOMB = WeaponData("Gravity Bomb", 42)
ZODIAC = WeaponData("Zodiac", 43)
RYNO_II = WeaponData("RYNO II", 44)
SHIELD_CHARGER = WeaponData("Shield Charger", 45)
WALLOPER = WeaponData("Walloper", 53)


def get_all() -> list[WeaponData]:
    return [
        CLANK_ZAPPER,
        BOMB_GLOVE,
        VISIBOMB_GUN,
        SHEEPINATOR,
        DECOY_GLOVE,
        TESLA_CLAW,
        CHOPPER,
        PULSE_RIFLE,
        SEEKER_GUN,
        HOVERBOMB_GUN,
        BLITZ_GUN,
        MINIROCKET_TUBE,
        PLASMA_COIL,
        LAVA_GUN,
        LANCER,
        SYNTHENOID,
        SPIDERBOT_GLOVE,
        BOUNCER,
        MINITURRET_GLOVE,
        GRAVITY_BOMB,
        ZODIAC,
        RYNO_II,
        SHIELD_CHARGER,
        WALLOPER
    ]
from .Names import ItemName

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import MMX3World

WEAKNESS_UNCHARGED_DMG = 0x03
WEAKNESS_CHARGED_DMG = 0x05

boss_weaknesses = {
    "Blizzard Buffalo": [
        [[ItemName.parasitic_bomb], 0x08, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.parasitic_bomb], 0x11, WEAKNESS_CHARGED_DMG],
    ],
    "Toxic Seahorse": [
        [[ItemName.frost_shield], 0x0D, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.frost_shield], 0x16, WEAKNESS_CHARGED_DMG+2],
        [[ItemName.frost_shield], 0x21, WEAKNESS_CHARGED_DMG],
    ],
    "Tunnel Rhino": [
        [[ItemName.acid_burst], 0x07, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.acid_burst], 0x10, WEAKNESS_CHARGED_DMG],
        [[ItemName.acid_burst], 0x18, WEAKNESS_UNCHARGED_DMG-1],
    ],
    "Volt Catfish": [
        [[ItemName.tornado_fang], 0x0E, WEAKNESS_CHARGED_DMG],
        [[ItemName.tornado_fang], 0x17, WEAKNESS_CHARGED_DMG+2],
    ],
    "Crush Crawfish": [
        [[ItemName.triad_thunder], 0x09, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.triad_thunder], 0x12, WEAKNESS_CHARGED_DMG+1],
        [[ItemName.triad_thunder], 0x1B, WEAKNESS_UNCHARGED_DMG],
    ],
    "Neon Tiger": [
        [[ItemName.spinning_blade], 0x0A, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.spinning_blade], 0x12, WEAKNESS_CHARGED_DMG],
    ],
    "Gravity Beetle": [
        [[ItemName.ray_splasher], 0x1C, WEAKNESS_UNCHARGED_DMG],
    ],
    "Blast Hornet": [
        [[ItemName.gravity_well], 0x0C, 0x03],
        [[ItemName.gravity_well], 0x15, 0x03],
    ],
    "Hotareeca": [
        [None, 0x00, 0x02],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x06, 0x03],
        [None, 0x1D, 0x04],
        [None, 0x1F, 0x05],
        [None, 0x20, 0x03],
    ],
    "Worm Seeker-R": [
        [None, 0x00, 0x02],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x06, 0x03],
        [None, 0x1D, 0x04],
        [None, 0x1F, 0x05],
        [None, 0x20, 0x03],
    ],
    "Hell Crusher": [
        [None, 0x00, 0x02],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x06, 0x03],
        [None, 0x1D, 0x04],
        [None, 0x1F, 0x05],
        [None, 0x20, 0x03],
    ],
    "Shurikein": [
        [None, 0x00, 0x02],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x06, 0x03],
        [None, 0x1D, 0x04],
        [None, 0x1F, 0x05],
        [None, 0x20, 0x03],
    ],
    "Bit": [
        [[ItemName.triad_thunder], 0x09, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.triad_thunder], 0x12, WEAKNESS_CHARGED_DMG+1],
        [[ItemName.triad_thunder], 0x1B, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.frost_shield], 0x0D, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.frost_shield], 0x16, WEAKNESS_CHARGED_DMG+2],
        [[ItemName.frost_shield], 0x21, WEAKNESS_CHARGED_DMG],
    ],
    "Byte": [
        [[ItemName.tornado_fang], 0x0E, WEAKNESS_CHARGED_DMG],
        [[ItemName.tornado_fang], 0x17, WEAKNESS_CHARGED_DMG+2],
        [[ItemName.ray_splasher], 0x1C, WEAKNESS_UNCHARGED_DMG],
    ],
    "Vile": [
        [[ItemName.ray_splasher], 0x1C, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.spinning_blade], 0x0A, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.spinning_blade], 0x12, WEAKNESS_CHARGED_DMG],
    ],
    "Press Disposer": [
        [[ItemName.tornado_fang], 0x0E, WEAKNESS_CHARGED_DMG],
        [[ItemName.tornado_fang], 0x17, WEAKNESS_CHARGED_DMG+2],
        [[ItemName.ray_splasher], 0x1C, WEAKNESS_UNCHARGED_DMG],
    ],
    "Godkarmachine": [
        [[ItemName.ray_splasher], 0x1C, WEAKNESS_UNCHARGED_DMG],
    ],
    "Dr. Doppler's Lab 2 Boss": [
        [None]
    ],
    "Volt Kurageil": [
        [[ItemName.triad_thunder], 0x09, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.triad_thunder], 0x12, WEAKNESS_CHARGED_DMG+1],
        [[ItemName.triad_thunder], 0x1B, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.frost_shield], 0x0D, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.frost_shield], 0x16, WEAKNESS_CHARGED_DMG+2],
        [[ItemName.frost_shield], 0x21, WEAKNESS_CHARGED_DMG],
    ],
    "Vile Goliath": [
        [[ItemName.parasitic_bomb], 0x08, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.parasitic_bomb], 0x11, WEAKNESS_CHARGED_DMG],
        [[ItemName.tornado_fang], 0x0E, WEAKNESS_CHARGED_DMG],
        [[ItemName.tornado_fang], 0x17, WEAKNESS_CHARGED_DMG+2],
    ],
    "Doppler": [
        [[ItemName.acid_burst], 0x07, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.acid_burst], 0x10, WEAKNESS_CHARGED_DMG],
        [[ItemName.acid_burst], 0x18, WEAKNESS_UNCHARGED_DMG-1],
    ],
    "Sigma": [
        [[ItemName.frost_shield], 0x0D, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.frost_shield], 0x16, WEAKNESS_CHARGED_DMG+2],
        [[ItemName.frost_shield], 0x21, WEAKNESS_CHARGED_DMG],
        [[ItemName.spinning_blade], 0x0A, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.spinning_blade], 0x12, WEAKNESS_CHARGED_DMG],
    ],
    "Kaiser Sigma": [
        [None, 0x00, 0x02],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x06, 0x03],
        [None, 0x1D, 0x04],
        [None, 0x1F, 0x05],
        [None, 0x20, 0x03],
    ],
}

weapon_id = {
    0x00: "Lemon",
    0x01: "Charged Shot (Level 1)",
    0x02: "Z-Saber (Slash)",
    0x03: "Charged Shot (Level 2)",
    0x04: "Z-Saber (Beam)",
    0x05: "Z-Saber (Beam slashes)",
    0x06: "Lemon (Dash)",
    0x07: "Uncharged Acid Burst",
    0x08: "Uncharged Parasitic Bomb",
    0x09: "Uncharged Triad Thunder (Contact)",
    0x0A: "Uncharged Spinning Blade",
    0x0C: "Gravity Well",
    0x0D: "Uncharged Frost Shield",
    0x0E: "Uncharged Tornado Fang",
    0x10: "Charged Acid Burst",
    0x11: "Charged Parasitic Bomb",
    0x12: "Charged Triad Thunder",
    0x13: "Charged Spinning Blade",
    0x15: "Gravity Well",
    0x16: "Charged Frost Shield (On hand)",
    0x17: "Charged Tornado Fang",
    0x18: "Acid Burst (Small uncharged bubbles)",
    0x1B: "Uncharged Triad Thunder (Thunder)",
    0x1C: "Ray Splasher",
    0x1D: "Charged Shot (Level 3)",
    0x1F: "Charged Shot (Level 4, Main projectile)",
    0x20: "Charged Shot (Level 4, Secondary projectile)",
    0x21: "Charged Frost Shield (Lotus)"
}

damage_templates = {
    "Allow Buster": [
        0x01, 0x01, 0x04, 0x02, 0x04, 0x02, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x00, 0x80, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x00, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x02, 0x80, 0x04,
        0x02, 0x80, 0x80, 0x80, 0x80, 0x80
    ],
    "Allow Upgraded Buster": [
        0x80, 0x80, 0x06, 0x80, 0x03, 0x02, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x00, 0x80, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x00, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x01, 0x80, 0x02,
        0x01, 0x80, 0x80, 0x80, 0x80, 0x80
    ],
    "Only Weakness": [
        0x80, 0x80, 0x04, 0x80, 0x02, 0x02, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x00, 0x80, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x00, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,
        0x80, 0x80, 0x80, 0x80, 0x80, 0x80
    ],
}

boss_weakness_data = {
    "Blast Hornet": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x02,0x01,0x03,0x01,0x80,0x01,
        0x02,0x01,0x01,0x03,0x01,0x03,0x01,0x80,
        0x01,0x02,0x03,0x01,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Blizzard Buffalo": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x80,0x00,0x01,0x80,0x01,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x80,
        0x01,0x02,0x03,0x01,0x80,0x02,0x04,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Gravity Beetle": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x01,0x80,0x01,
        0x01,0x01,0x01,0x01,0x05,0x00,0x01,0x80,
        0x01,0x02,0x03,0x01,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Toxic Seahorse": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x01,0x80,0x02,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x80,
        0x01,0x02,0x03,0x01,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Volt Catfish": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x80,0x01,0x80,0x00,0x01,0x01,0x80,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x01,
        0x01,0x02,0x03,0x80,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Crush Crawfish": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x80,0x01,0x80,0x01,0x00,0x01,0x80,0x01,
        0x01,0x80,0x01,0x80,0x01,0x00,0x01,0x80,
        0x01,0x01,0x03,0x02,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Tunnel Rhino": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x80,0x80,0x01,0x01,0x00,0x01,0x80,0x80,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x80,
        0x01,0x02,0x03,0x80,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Neon Tiger": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x80,0x00,0x01,0x80,0x01,
        0x01,0x01,0x01,0x01,0x80,0x00,0x01,0x80,
        0x01,0x02,0x03,0x01,0x80,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Bit": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x01,0x80,0x01,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x80,
        0x01,0x02,0x03,0x01,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Byte": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x01,0x01,0x01,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x01,
        0x01,0x02,0x03,0x01,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Vile": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x80,0x01,0x01,0x00,0x01,0x80,0x80,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x80,
        0x01,0x02,0x03,0x80,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Vile Goliath": [
        0x01,0x02,0x10,0x03,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x01,0x01,0x01,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x01,
        0x01,0x02,0x03,0x01,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Hell Crusher": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x01,0x01,0x01,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x01,
        0x01,0x02,0x03,0x01,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Shurikein": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x03,
        0x80,0x80,0x01,0x01,0x00,0x01,0x80,0x80,
        0x05,0x01,0x02,0x01,0x02,0x00,0x01,0x80,
        0x02,0x02,0x03,0x80,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Hotareeca": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x01,0x80,0x01,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x80,
        0x01,0x02,0x03,0x01,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Worm Seeker-R": [
        0x03,0x05,0x1E,0x09,0x80,0x04,0x05,0x09,
        0x02,0x0F,0x09,0x05,0x00,0x0F,0x80,0x09,
        0x09,0x02,0x80,0x1E,0x09,0x00,0x0F,0x80,
        0x05,0x05,0x09,0x05,0x05,0x09,0x0F,0x12,
        0x09,0x09,0x1E,0x09,0x06,0x7F,
    ],
    "Volt Kurageil": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x01,0x80,0x01,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x80,
        0x01,0x02,0x03,0x01,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Godkarmachine": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x01,0x80,0x01,
        0x01,0x02,0x01,0x01,0x01,0x00,0x01,0x80,
        0x01,0x02,0x03,0x01,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Press Disposer": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x01,0x01,0x01,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x01,
        0x01,0x02,0x03,0x01,0x01,0x01,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Doppler": [
        0x01,0x02,0x10,0x03,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x01,0x01,0x01,
        0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x01,
        0x01,0x02,0x03,0x01,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Sigma": [
        0x01,0x01,0x10,0x02,0x08,0x04,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x01,0x80,0x01,
        0x01,0x01,0x01,0x01,0x01,0x00,0x04,0x80,
        0x01,0x02,0x03,0x01,0x01,0x02,0x80,0x03,
        0x02,0x01,0x02,0x01,0x01,0x00,
    ],
    "Kaiser Sigma": [
        0x80,0x01,0x10,0x02,0x08,0x04,0x80,0x80,
        0x80,0x80,0x80,0x80,0x00,0x80,0x80,0x80,
        0x80,0x80,0x80,0x80,0x80,0x00,0x80,0x80,
        0x80,0x02,0x03,0x80,0x80,0x02,0x80,0x03,
        0x02,0x80,0x02,0x01,0x01,0x00,
    ]
}

boss_excluded_weapons = {
    "Blast Hornet": [
    ],
    "Blizzard Buffalo": [
        "Charged Triad Thunder",
    ],
    "Gravity Beetle": [
    ],
    "Toxic Seahorse": [
    ],
    "Volt Catfish": [
    ],
    "Crush Crawfish": [
    ],
    "Tunnel Rhino": [
    ],
    "Neon Tiger": [
    ],
    "Bit": [
    ],
    "Byte": [
        "Charged Triad Thunder",
    ],
    "Vile": [
        "Charged Triad Thunder",
    ],
    "Vile Goliath": [
    ],
    "Hell Crusher": [
        "Charged Tornado Fang",
    ],
    "Shurikein": [
    ],
    "Hotareeca": [
        "Acid Burst",
        "Charged Acid Burst",
        "Charged Frost Shield",
        "Charged Triad Thunder",
    ],
    "Worm Seeker-R": [
        "Charged Parasitic Bomb",
    ],
    "Volt Kurageil": [
        "Charged Frost Shield",
        "Charged Triad Thunder",
    ],
    "Godkarmachine": [
        "Charged Triad Thunder",
    ],
    "Press Disposer": [
        "Charged Frost Shield",
        "Charged Tornado Fang",
    ],
    "Doppler": [
    ],
    "Sigma": [
        "Charged Parasitic Bomb",
    ],
    "Kaiser Sigma": [
        "Charged Tornado Fang",
        "Charged Frost Shield",
        "Charged Parasitic Bomb",
    ]
}

blast_hornet_data = {
    "Gravity Well": [
        [[ItemName.gravity_well], 0x0C, 0x03],
        [[ItemName.gravity_well], 0x15, 0x03],
    ]
}
weapons = {
    "Buster": [
        [None, 0x00, 0x02],
        [None, 0x01, 0x03],
        [None, 0x03, 0x04],
        [None, 0x06, 0x03],
        [None, 0x1D, 0x04],
        [None, 0x1F, 0x05],
        [None, 0x20, 0x03],
    ],
    "Acid Burst": [
        [[ItemName.acid_burst], 0x07, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.acid_burst], 0x10, WEAKNESS_CHARGED_DMG],
        [[ItemName.acid_burst], 0x18, WEAKNESS_UNCHARGED_DMG-1],
    ],
    "Parasitic Bomb": [
        [[ItemName.parasitic_bomb], 0x08, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.parasitic_bomb], 0x11, WEAKNESS_CHARGED_DMG],
    ],
    "Triad Thunder": [
        [[ItemName.triad_thunder], 0x09, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.triad_thunder], 0x12, WEAKNESS_CHARGED_DMG+1],
        [[ItemName.triad_thunder], 0x1B, WEAKNESS_UNCHARGED_DMG],
    ],
    "Spinning Blade": [
        [[ItemName.spinning_blade], 0x0A, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.spinning_blade], 0x13, WEAKNESS_CHARGED_DMG],
    ],
    "Ray Splasher": [
        [[ItemName.ray_splasher], 0x1C, WEAKNESS_UNCHARGED_DMG],
    ],
    "Frost Shield": [
        [[ItemName.frost_shield], 0x0D, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.frost_shield], 0x16, WEAKNESS_CHARGED_DMG+2],
        [[ItemName.frost_shield], 0x21, WEAKNESS_CHARGED_DMG],
    ],
    "Tornado Fang": [
        [[ItemName.tornado_fang], 0x0E, WEAKNESS_CHARGED_DMG],
        [[ItemName.tornado_fang], 0x17, WEAKNESS_CHARGED_DMG+2],
    ],
}

weapons_chaotic = {
    "Lemon": [
        [None, 0x00, 0x02],
    ],
    "Lemon (Dash)": [
        [None, 0x06, 0x03],
    ],
    "Charged Shot (Level 1)": [
        [["Check Charge 1"], 0x01, 0x03],
    ],
    "Charged Shot (Level 2)": [
        [["Check Charge 1"], 0x03, 0x04],
    ],
    "Charged Shot (Level 3)": [
        [["Check Charge 2"], 0x1D, 0x04],
        [["Check Charge 2"], 0x20, 0x03],
    ],
    "Charged Shot (Level 4)": [
        [["Check Charge 2"], 0x1F, 0x05],
        [["Check Charge 2"], 0x20, 0x03],
    ],
    "Acid Burst": [
        [[ItemName.acid_burst], 0x07, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.acid_burst], 0x18, WEAKNESS_UNCHARGED_DMG-1],
    ],
    "Charged Acid Burst": [
        [["Check Charge 2", ItemName.acid_burst], 0x10, WEAKNESS_CHARGED_DMG],
    ],
    "Parasitic Bomb": [
        [[ItemName.parasitic_bomb], 0x08, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Parasitic Bomb": [
        [["Check Charge 2", ItemName.parasitic_bomb], 0x11, WEAKNESS_CHARGED_DMG],
    ],
    "Triad Thunder": [
        [[ItemName.triad_thunder], 0x09, WEAKNESS_UNCHARGED_DMG],
        [[ItemName.triad_thunder], 0x1B, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Triad Thunder": [
        [["Check Charge 2", ItemName.triad_thunder], 0x12, WEAKNESS_CHARGED_DMG],
    ],
    "Spinning Blade": [
        [[ItemName.spinning_blade], 0x0A, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Spinning Blade": [
        [["Check Charge 2", ItemName.spinning_blade], 0x13, WEAKNESS_CHARGED_DMG],
    ],
    "Ray Splasher": [
        [[ItemName.ray_splasher], 0x1C, WEAKNESS_UNCHARGED_DMG],
    ],
    "Frost Shield": [
        [[ItemName.frost_shield], 0x0D, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Frost Shield": [
        [["Check Charge 2", ItemName.frost_shield], 0x16, WEAKNESS_CHARGED_DMG],
        [["Check Charge 2", ItemName.frost_shield], 0x21, WEAKNESS_CHARGED_DMG],
    ],
    "Tornado Fang": [
        [[ItemName.tornado_fang], 0x0E, WEAKNESS_UNCHARGED_DMG],
    ],
    "Charged Tornado Fang": [
        [["Check Charge 2", ItemName.tornado_fang], 0x17, WEAKNESS_CHARGED_DMG],
    ],
}


def handle_weaknesses(world: "MMX3World"):
    shuffle_type = world.options.boss_weakness_rando.value
    strictness_type = world.options.boss_weakness_strictness.value
    boss_weakness_plando = world.options.boss_weakness_plando.value

    if shuffle_type != "vanilla":
        weapon_list = weapons.keys()
        if shuffle_type == 2 or shuffle_type == 3:
            weapon_list = weapons_chaotic.keys()
        weapon_list = list(weapon_list)
    
    for boss in boss_weaknesses.keys():
        if boss == "Dr. Doppler's Lab 2 Boss":
            continue
        world.boss_weaknesses[boss] = []

        if strictness_type == 0:
            damage_table = boss_weakness_data[boss].copy()
        elif strictness_type == 1:
            damage_table = damage_templates["Allow Buster"].copy()
        elif strictness_type == 2:
            damage_table = damage_templates["Allow Upgraded Buster"].copy()
            world.boss_weaknesses[boss].append(weapons_chaotic["Charged Shot (Level 3)"][0])
            world.boss_weaknesses[boss].append(weapons_chaotic["Charged Shot (Level 3)"][1])
            world.boss_weaknesses[boss].append(weapons_chaotic["Charged Shot (Level 4)"][0])
            world.boss_weaknesses[boss].append(weapons_chaotic["Charged Shot (Level 4)"][1])
        else:
            damage_table = damage_templates["Only Weakness"].copy()

        if shuffle_type != "vanilla":
            if boss == "Blast Hornet":
                world.boss_weaknesses[boss].append(blast_hornet_data["Gravity Well"][0])
                damage_table[0x0C] = 0x03
                damage_table[0x15] = 0x03

        if boss in boss_weakness_plando.keys():
            if shuffle_type != "vanilla":
                chosen_weapon = boss_weakness_plando[boss]
                if chosen_weapon not in boss_excluded_weapons[boss]:
                    data = weapons_chaotic[chosen_weapon].copy()
                    for entry in data:
                        world.boss_weaknesses[boss].append(entry)
                        damage = entry[2]
                        damage_table[entry[1]] = damage
                    world.boss_weakness_data[boss] = damage_table.copy()
                    continue

                print (f"[{world.multiworld.player_name[world.player]}] Weakness plando failed for {boss}, contains an excluded weapon. Choosing an alternate weapon...")

        if shuffle_type != "vanilla":
            copied_weapon_list = weapon_list.copy()
            for weapon in boss_excluded_weapons[boss]:
                if weapon in copied_weapon_list:
                    copied_weapon_list.remove(weapon)

        if shuffle_type == 1:
            chosen_weapon = world.random.choice(copied_weapon_list)
            data = weapons[chosen_weapon]
            for entry in data:
                world.boss_weaknesses[boss].append(entry)
                damage = entry[2]
                damage_table[entry[1]] = damage

        elif shuffle_type >= 2:
            for _ in range(shuffle_type - 1):
                chosen_weapon = world.random.choice(copied_weapon_list)
                data = weapons_chaotic[chosen_weapon].copy()
                copied_weapon_list.remove(chosen_weapon)
                for entry in data:
                    world.boss_weaknesses[boss].append(entry)
                    damage = entry[2]
                    damage_table[entry[1]] = damage
            world.boss_weakness_data[boss] = damage_table.copy()

        else:
            for entry in boss_weaknesses[boss]:
                world.boss_weaknesses[boss].append(entry)
                damage = entry[2]
                damage_table[entry[1]] = damage

        world.boss_weakness_data[boss] = damage_table.copy()

    if world.options.doppler_lab_2_boss == "volt_kurageil":
        world.boss_weaknesses["Dr. Doppler's Lab 2 Boss"] = world.boss_weaknesses["Volt Kurageil"].copy()
    else:
        world.boss_weaknesses["Dr. Doppler's Lab 2 Boss"] = list()
        for weakness in world.boss_weaknesses["Vile"]:
            world.boss_weaknesses["Dr. Doppler's Lab 2 Boss"].append(weakness)
        for weakness in world.boss_weaknesses["Vile Goliath"]:
            world.boss_weaknesses["Dr. Doppler's Lab 2 Boss"].append(weakness)
cards = [
    # Type 0
    "Card (Edward)",
    "Card (Annoyer)",
    "Card (Seer)",
    "Card (Shieldy)",
    "Card (Slime)",
    "Card (PewLaser)",
    "Card (Suburbian)",
    "Card (Watcher)",
    "Card (Silverfish)",
    "Card (Gas Guy)",
    # Type 10
    "Card (Mitra)",
    "Card (Miao)",
    "Card (Windmill)",
    "Card (Mushroom)",
    "Card (Dog)",
    "Card (Rock)",
    "Card (Fisherman)",
    "Card (Walker)",
    "Card (Mover)",
    "Card (Slasher)",
    # Type 20
    "Card (Rogue)",
    "Card (Chaser)",
    "Card (Fire Pillar)",
    "Card (Contorts)",
    "Card (Lion)",
    "Card (Arthur and Javiera)",
    "Card (Frog)",
    "Card (Person)",
    "Card (Wall)",
    "Card (Blue Cube King)",
    # Type 30
    "Card (Orange Cube King)",
    "Card (Dust Maid)",
    "Card (Dasher)",
    "Card (Burst Plant)",
    "Card (Manager)",
    "Card (Sage)",
    "Card (Young)",
    "Card (Carved Rock)",
    "Card (City Man)",
    "Card (Intra)",
    # Type 40
    "Card (Torch)",
    "Card (Triangle NPC)",
    "Card (Killer)",
    "Card (Goldman)",
    "Card (Broom)",
    "Card (Rank)",
    "Card (Follower)",
    "Card (Rock Creature)",
    # Type 49
    "Card (Null)",
]

postgame_cards = [
    "Card (Young)",
    "Card (Carved Rock)",
    "Card (City Man)",
    "Card (Intra)",
    "Card (Torch)",
    "Card (Triangle NPC)",
    "Card (Killer)",
    "Card (Broom)",
    "Card (Rank)",
    "Card (Follower)",
    "Card (Rock Creature)",
    "Card (Null)",
]

secret_items = [
    "Golden Poop",
    "Spam Can",
    "Glitch",
    "Heart",
    "Electric Monster",
    "Cat Statue",
    "Melos",
    "Marina",
    "Black Cube",
    "Red Cube",
    "Green Cube",
    "Blue Cube",
    "White Cube",
    "Golden Broom",
]

early_secret_items = [
    "Golden Poop",
    "Heart",
]

secret_items_secret_paths = [
    "Glitch",
    "Spam Can",
    "Electric Monster"
]

small_key_item_count = {
    "Small Key (Apartment)": 4,
    "Small Key (Temple of the Seeing One)": 3,
    "Small Key (Circus)": 4,
    "Small Key (Mountain Cavern)": 4,
    "Small Key (Hotel)": 7,
    "Small Key (Red Cave)": 6,
    "Small Key (Street)": 1
}

big_keys = [
    "Green Key",
    "Red Key",
    "Blue Key",
]

key_rings = [
    "Key Ring (Apartment)",
    "Key Ring (Temple of the Seeing One)",
    "Key Ring (Circus)",
    "Key Ring (Mountain Cavern)",
    "Key Ring (Hotel)",
    "Key Ring (Red Cave)",
    "Key Ring (Street)"
]

statue_items = [
    "Temple of the Seeing One Statue",
    "Red Cave Statue",
    "Mountain Cavern Statue",
]

non_secret_filler_items = [
    "Heal",
    "Big Heal"
]

nexus_gate_items = {
    "Nexus Gate (Apartment)": "Apartment floor 1",
    "Nexus Gate (Beach)": "Beach",
    "Nexus Gate (Temple of the Seeing One)": "Bedroom exit",
    "Nexus Gate (Blue)": "Blue",
    "Nexus Gate (Cell)": "Cell",
    "Nexus Gate (Circus)": "Circus",
    "Nexus Gate (Cliffs)": "Cliff",
    "Nexus Gate (Mountain Cavern)": "Crowd exit",
    "Nexus Gate (Fields)": "Fields",
    "Nexus Gate (Deep Forest)": "Forest",
    "Nexus Gate (GO)": "Go bottom",
    "Nexus Gate (Happy)": "Happy",
    "Nexus Gate (Hotel)": "Hotel floor 4",
    "Nexus Gate (Overworld)": "Overworld",
    "Nexus Gate (Red Cave)": "Red Cave exit",
    "Nexus Gate (Red Sea)": "Red Sea",
    "Nexus Gate (Young Town)": "Suburb",
    "Nexus Gate (Space)": "Space",
    "Nexus Gate (Terminal)": "Terminal",
    "Nexus Gate (Windmill)": "Windmill entrance",
}

trap_items = [
    "Person Trap",
    "Gas Trap"
]

# This array must maintain a consistent order because the IDs are generated from it.
all_items = [
    "Broom",
    "Jump Shoes",
    "Widen",
    "Extend",
    "Swap",
    # Cards
    *cards,
    # Secrets
    *secret_items,
    # Keys
    *small_key_item_count.keys(),
    *big_keys,
    "Health Cicada",
    "Cardboard Box",
    "Biking Shoes",
    "Progressive Red Cave",
    *statue_items,
    "Progressive Swap",
    *non_secret_filler_items,
    *nexus_gate_items.keys(),
    *trap_items,
    *key_rings
]

progression_items = [
    "Broom",
    "Widen",
    "Extend",
    "Swap",
    "Jump Shoes",
    *cards,
    *small_key_item_count.keys(),
    *big_keys,
    "Cardboard Box",
    "Biking Shoes",
    "Progressive Red Cave",
    *statue_items,
    "Progressive Swap",
    *nexus_gate_items.keys(),
    *key_rings
]

useful_items = [
    "Health Cicada",
]

filler_items = [
    *secret_items,
    *non_secret_filler_items,
]

brooms = [
    "Broom",
    "Widen",
    "Extend"
]

item_groups = {
    "Cards": cards,
    "Nexus Gates": nexus_gate_items.keys(),
    "Keys": small_key_item_count.keys(),
    "Key Rings": small_key_item_count.keys(),
    "Big Keys": big_keys,
    "Statues": statue_items,
    "Brooms": brooms,
}

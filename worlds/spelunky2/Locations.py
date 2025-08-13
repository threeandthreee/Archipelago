from typing import NamedTuple, Optional
from BaseClasses import Location


class Spelunky2Location(Location):
    game = "Spelunky 2"


class Spelunky2LocationData(NamedTuple):
    address: int
    region: str


place_entries = {
    "Dwelling Journal Entry": Spelunky2LocationData(1, "Dwelling"),
    "Jungle Journal Entry": Spelunky2LocationData(2, "Jungle"),
    "Volcana Journal Entry": Spelunky2LocationData(3, "Volcana"),
    "Olmec's Lair Journal Entry": Spelunky2LocationData(4, "Olmec's Lair"),
    "Tide Pool Journal Entry": Spelunky2LocationData(5, "Tide Pool"),
    "Abzu Journal Entry": Spelunky2LocationData(6, "Tide Pool"),
    "Temple of Anubis Journal Entry": Spelunky2LocationData(7, "Temple"),
    "The City of Gold Journal Entry": Spelunky2LocationData(8, "Temple"),
    "Duat Journal Entry": Spelunky2LocationData(9, "Temple"),
    "Ice Caves Journal Entry": Spelunky2LocationData(10, "Ice Caves"),
    "Neo Babylon Journal Entry": Spelunky2LocationData(11, "Ice Caves"),
    "Tiamat's Throne Journal Entry": Spelunky2LocationData(12, "Neo Babylon"),
    "Sunken City Journal Entry": Spelunky2LocationData(13, "Sunken City"),
    "Eggplant World Journal Entry": Spelunky2LocationData(14, "Sunken City"),
    "Hundun's Hideaway Journal Entry": Spelunky2LocationData(15, "Sunken City"),
    "Cosmic Ocean Journal Entry": Spelunky2LocationData(16, "Cosmic Ocean")
}

people_entries = {
    # Excluding this until I figure out how they'll be implemented
    # "Ana Spelunky Journal Entry": Spelunky2LocationData(17, "Menu"),
    # "Margaret Tunnel Journal Entry": Spelunky2LocationData(18, "Menu"),
    # "Colin Northward Journal Entry": Spelunky2LocationData(19, "Menu"),
    # "Roffy D. Sloth Journal Entry": Spelunky2LocationData(20, "Menu"),
    "Alto Singh Journal Entry": Spelunky2LocationData(21, "Dwelling"),
    "Liz Mutton Journal Entry": Spelunky2LocationData(22, "Jungle"),
    "Nekka the Eagle Journal Entry": Spelunky2LocationData(23, "Jungle"),
    "LISE Project Journal Entry": Spelunky2LocationData(24, "Volcana"),
    "Coco Von Diamonds Journal Entry": Spelunky2LocationData(25, "Volcana"),
    "Manfred Tunnel Journal Entry": Spelunky2LocationData(26, "Olmec's Lair"),
    "Little Jay Journal Entry": Spelunky2LocationData(27, "Tide Pool"),
    "Tina Flan Journal Entry": Spelunky2LocationData(28, "Tide Pool"),
    "Valerie Crump Journal Entry": Spelunky2LocationData(29, "Temple"),
    "Au Journal Entry": Spelunky2LocationData(30, "Temple"),
    "Demi Von Diamonds Journal Entry": Spelunky2LocationData(31, "Ice Caves"),
    "Pilot Journal Entry": Spelunky2LocationData(32, "Ice Caves"),
    "Princess Airyn Journal Entry": Spelunky2LocationData(33, "Neo Babylon"),
    "Dirk Yamaoka Journal Entry": Spelunky2LocationData(34, "Sunken City"),
    "Guy Spelunky Journal Entry": Spelunky2LocationData(35, "Neo Babylon"),
    "Classic Guy Journal Entry": Spelunky2LocationData(36, "Sunken City"),
    "Terra Tunnel Journal Entry": Spelunky2LocationData(37, "Menu"),  # Can be in either Jungle or Volcana
    "Hired Hand Journal Entry": Spelunky2LocationData(38, "Dwelling"),
    "Eggplant Child Journal Entry": Spelunky2LocationData(39, "Ice Caves"),
    "Shopkeeper Journal Entry": Spelunky2LocationData(40, "Dwelling"),
    "Tun Journal Entry": Spelunky2LocationData(41, "Menu"),  # Can be in either Jungle or Volcana - Can be met in Dwelling by random chance
    "Yang Journal Entry": Spelunky2LocationData(42, "Dwelling"),
    "Madame Tusk Journal Entry": Spelunky2LocationData(43, "Tide Pool"),
    "Tusk's Bodyguard Journal Entry": Spelunky2LocationData(44, "Tide Pool"),
    "Waddler Journal Entry": Spelunky2LocationData(45, "Olmec's Lair"),
    "Caveman Shopkeeper Journal Entry": Spelunky2LocationData(46, "Dwelling"),
    "Ghist Shopkeeper Journal Entry": Spelunky2LocationData(47, "Tide Pool"),
    "Van Horsing Journal Entry": Spelunky2LocationData(48, "Volcana"),
    "Parsley Journal Entry": Spelunky2LocationData(49, "Jungle"),
    "Parsnip Journal Entry": Spelunky2LocationData(50, "Jungle"),
    "Parmesan Journal Entry": Spelunky2LocationData(51, "Jungle"),
    "Sparrow Journal Entry": Spelunky2LocationData(52, "Menu"),  # Can be in either Jungle or Volcana
    "Beg Journal Entry": Spelunky2LocationData(53, "Menu"),  # Depends on how many altars you encounter - Logic assumes you find 2 altars within the first 2 worlds
    "Eggplant King Journal Entry": Spelunky2LocationData(54, "Sunken City"),
}

bestiary_entries = {
    # Dwelling
    "Snake Journal Entry": Spelunky2LocationData(55, "Dwelling"),
    "Spider Journal Entry": Spelunky2LocationData(56, "Dwelling"),
    "Bat Journal Entry": Spelunky2LocationData(57, "Dwelling"),
    "Caveman Journal Entry": Spelunky2LocationData(58, "Dwelling"),
    "Skeleton Journal Entry": Spelunky2LocationData(59, "Dwelling"),
    "Horned Lizard Journal Entry": Spelunky2LocationData(60, "Dwelling"),
    "Cave Mole Journal Entry": Spelunky2LocationData(61, "Dwelling"),
    "Quillback Journal Entry": Spelunky2LocationData(62, "Dwelling"),

    # Jungle
    "Mantrap Journal Entry": Spelunky2LocationData(63, "Jungle"),
    "Tiki Man Journal Entry": Spelunky2LocationData(64, "Jungle"),
    "Witch Doctor Journal Entry": Spelunky2LocationData(65, "Jungle"),
    "Mosquito Journal Entry": Spelunky2LocationData(66, "Jungle"),
    "Monkey Journal Entry": Spelunky2LocationData(67, "Jungle"),
    "Hang Spider Journal Entry": Spelunky2LocationData(68, "Jungle"),
    "Giant Spider Journal Entry": Spelunky2LocationData(69, "Jungle"),

    # Volcana
    "Magmar Journal Entry": Spelunky2LocationData(70, "Volcana"),
    "Robot Journal Entry": Spelunky2LocationData(71, "Volcana"),
    "Fire Bug Journal Entry": Spelunky2LocationData(72, "Volcana"),
    "Imp Journal Entry": Spelunky2LocationData(73, "Volcana"),
    "Lavamander Journal Entry": Spelunky2LocationData(74, "Volcana"),
    "Vampire Journal Entry": Spelunky2LocationData(75, "Volcana"),
    "Vlad Journal Entry": Spelunky2LocationData(76, "Volcana"),

    # Olmec's Lair
    "Olmec Journal Entry": Spelunky2LocationData(77, "Olmec's Lair"),

    # Tide Pool
    "Jiangshi Journal Entry": Spelunky2LocationData(78, "Tide Pool"),
    "Jiangshi Assassin Journal Entry": Spelunky2LocationData(79, "Tide Pool"),
    "Flying Fish Journal Entry": Spelunky2LocationData(80, "Tide Pool"),
    "Octopy Journal Entry": Spelunky2LocationData(81, "Tide Pool"),
    "Hermit Crab Journal Entry": Spelunky2LocationData(82, "Tide Pool"),
    "Pangxie Journal Entry": Spelunky2LocationData(83, "Tide Pool"),
    "Great Humphead Journal Entry": Spelunky2LocationData(84, "Tide Pool"),
    "Kingu Journal Entry": Spelunky2LocationData(85, "Tide Pool"),

    # Temple
    "Crocman Journal Entry": Spelunky2LocationData(86, "Temple"),
    "Cobra Journal Entry": Spelunky2LocationData(87, "Temple"),
    "Mummy Journal Entry": Spelunky2LocationData(88, "Temple"),
    "Sorceress Journal Entry": Spelunky2LocationData(89, "Temple"),
    "Cat Mummy Journal Entry": Spelunky2LocationData(90, "Temple"),
    "Necromancer Journal Entry": Spelunky2LocationData(91, "Temple"),
    "Anubis Journal Entry": Spelunky2LocationData(92, "Temple"),
    "Ammit Journal Entry": Spelunky2LocationData(93, "Temple"),
    "Apep Journal Entry": Spelunky2LocationData(94, "Temple"),
    "Anubis II Journal Entry": Spelunky2LocationData(95, "Temple"),
    "Osiris Journal Entry": Spelunky2LocationData(96, "Temple"),

    # Ice Caves
    "UFO Journal Entry": Spelunky2LocationData(97, "Ice Caves"),
    "Alien Journal Entry": Spelunky2LocationData(98, "Ice Caves"),
    "Yeti Journal Entry": Spelunky2LocationData(99, "Ice Caves"),
    "Yeti King Journal Entry": Spelunky2LocationData(100, "Ice Caves"),
    "Yeti Queen Journal Entry": Spelunky2LocationData(101, "Ice Caves"),
    "Lamahu Journal Entry": Spelunky2LocationData(102, "Ice Caves"),
    "Proto Shopkeeper Journal Entry": Spelunky2LocationData(103, "Ice Caves"),

    # Neo Babylon
    "Olmite Journal Entry": Spelunky2LocationData(104, "Neo Babylon"),
    "Lamassu Journal Entry": Spelunky2LocationData(105, "Neo Babylon"),
    "Tiamat Journal Entry": Spelunky2LocationData(106, "Neo Babylon"),

    # Sunken City
    "Tadpole Journal Entry": Spelunky2LocationData(107, "Sunken City"),
    "Frog Journal Entry": Spelunky2LocationData(108, "Sunken City"),
    "Fire Frog Journal Entry": Spelunky2LocationData(109, "Sunken City"),
    "Goliath Frog Journal Entry": Spelunky2LocationData(110, "Sunken City"),
    "Grub Journal Entry": Spelunky2LocationData(111, "Sunken City"),
    "Giant Fly Journal Entry": Spelunky2LocationData(112, "Sunken City"),
    "Hundun Journal Entry": Spelunky2LocationData(113, "Sunken City"),
    "Eggplant Minister Journal Entry": Spelunky2LocationData(114, "Sunken City"),
    "Eggplup Journal Entry": Spelunky2LocationData(115, "Sunken City"),

    # Cosmic Ocean
    "Celestial Jelly Journal Entry": Spelunky2LocationData(116, "Cosmic Ocean"),

    # Miscellaneous
    "Scorpion Journal Entry": Spelunky2LocationData(117, "Temple"), # Can be obtained earlier, but Temple is most likely since it has so many pots
    "Bee Journal Entry": Spelunky2LocationData(118, "Jungle"),
    "Queen Bee Journal Entry": Spelunky2LocationData(119, "Jungle"),
    "Scarab Journal Entry": Spelunky2LocationData(120, "Dwelling"),
    "Golden Monkey Journal Entry": Spelunky2LocationData(121, "Menu"),
    "Leprechaun Journal Entry": Spelunky2LocationData(122, "Menu"),  # Can be in either Jungle or Volcana
    "Monty Journal Entry": Spelunky2LocationData(123, "Dwelling"),
    "Percy Journal Entry": Spelunky2LocationData(124, "Dwelling"),
    "Poochi Journal Entry": Spelunky2LocationData(125, "Dwelling"),
    "Ghist Journal Entry": Spelunky2LocationData(126, "Tide Pool"),  # Can spawn randomly earlier, but is guaranteed in Tide Pool (4-2)
    "Ghost Journal Entry": Spelunky2LocationData(127, "Dwelling"),
    "Cave Turkey Journal Entry": Spelunky2LocationData(128, "Dwelling"),
    "Rock Dog Journal Entry": Spelunky2LocationData(129, "Volcana"),
    "Axolotl Journal Entry": Spelunky2LocationData(130, "Tide Pool"),
    "Qilin Journal Entry": Spelunky2LocationData(131, "Neo Babylon"),
    "Mech Rider Journal Entry": Spelunky2LocationData(132, "Ice Caves")
}

item_entries = {
    # For the most part, regions will be where the earliest guaranteed drop is, i.e. Jetpack is in Temple because Anubis II always drops one
    # The exception for this are things that are very common, like bomb bags
    # The alternative is having almost everything in logic from the start since crates can produce basically any item
    "Rope Pile Journal Entry": Spelunky2LocationData(133, "Dwelling"),
    "Bomb Bag Journal Entry": Spelunky2LocationData(134, "Dwelling"),
    "Bomb Box Journal Entry": Spelunky2LocationData(135, "Dwelling"),
    "Paste Journal Entry": Spelunky2LocationData(136, "Jungle"),
    "Spectacles Journal Entry": Spelunky2LocationData(137, "Dwelling"),
    "Climbing Gloves Journal Entry": Spelunky2LocationData(138, "Dwelling"),
    "Pitcher's Mitt Journal Entry": Spelunky2LocationData(139, "Dwelling"),
    "Spring Shoes Journal Entry": Spelunky2LocationData(140, "Dwelling"),
    "Spike Shoes Journal Entry": Spelunky2LocationData(141, "Ice Caves"),  # Guaranteed drop from Yeti Queen
    "Compass Journal Entry": Spelunky2LocationData(142, "Dwelling"),
    "Alien Compass Journal Entry": Spelunky2LocationData(143, "Ice Caves"),
    "Parachute Journal Entry": Spelunky2LocationData(144, "Olmec's Lair"),  # Guaranteed in the back layer
    "Udjat Eye Journal Entry": Spelunky2LocationData(145, "Dwelling"),
    "Kapala Journal Entry": Spelunky2LocationData(146, "Neo Babylon"),  # Guaranteed altar on 6-3. There's also a guaranteed altar in Duat but not much you can sacrifice there
    "Hedjet Journal Entry": Spelunky2LocationData(147, "Jungle"),
    "Crown Journal Entry": Spelunky2LocationData(148, "Volcana"),
    "Eggplant Crown Journal Entry": Spelunky2LocationData(149, "Neo Babylon"),
    "True Crown Journal Entry": Spelunky2LocationData(150, "Neo Babylon"),  # Same reason as the Kapala, except you'd need to have found at least 2 altars prior to this
    "Ankh Journal Entry": Spelunky2LocationData(151, "Olmec's Lair"),
    "Tablet of Destiny Journal Entry": Spelunky2LocationData(152, "Menu"),  # Can be dropped from either Kingu or Osiris, so can't tie it to either Tide Pool or Temple
    "Skeleton Key Journal Entry": Spelunky2LocationData(153, "Dwelling"),
    "Royal Jelly Journal Entry": Spelunky2LocationData(154, "Jungle"),
    "Cape Journal Entry": Spelunky2LocationData(155, "Volcana"),
    "Vlad's Cape Journal Entry": Spelunky2LocationData(156, "Volcana"),
    "Jetpack Journal Entry": Spelunky2LocationData(157, "Temple"),  # Guaranteed drop from Anubis II
    "Telepack Journal Entry": Spelunky2LocationData(158, "Jungle"),  # Assumes black market
    "Hoverpack Journal Entry": Spelunky2LocationData(159, "Jungle"),  # Assumes black market
    "Powerpack Journal Entry": Spelunky2LocationData(160, "Jungle"),  # Assumes black market
    "Webgun Journal Entry": Spelunky2LocationData(161, "Dwelling"),
    "Shotgun Journal Entry": Spelunky2LocationData(162, "Dwelling"),
    "Freeze Ray Journal Entry": Spelunky2LocationData(163, "Ice Caves"),  # 10% drop from Yeti King, the most likely place to get it in isolation
    "Clone Gun Journal Entry": Spelunky2LocationData(164, "Tide Pool"),
    "Crossbow Journal Entry": Spelunky2LocationData(165, "Dwelling"),  # Yang carries one
    "Camera Journal Entry": Spelunky2LocationData(166, "Tide Pool"),  # Guaranteed drop from Giant Humphead
    "Teleporter Journal Entry": Spelunky2LocationData(167, "Jungle"),  # Assumes black market
    "Mattock Journal Entry": Spelunky2LocationData(168, "Menu"),  # From Moon Challenge
    "Boomerang Journal Entry": Spelunky2LocationData(169, "Jungle"),  # From Tiki Men
    "Machete Journal Entry": Spelunky2LocationData(170, "Dwelling"),
    "Excalibur Journal Entry": Spelunky2LocationData(171, "Tide Pool"),
    "Broken Sword Journal Entry": Spelunky2LocationData(172, "Tide Pool"),
    "Plasma Cannon Journal Entry": Spelunky2LocationData(173, "Ice Caves"),  # In the Mothership
    "Scepter Journal Entry": Spelunky2LocationData(174, "Temple"),
    "Hou Yi's Bow Journal Entry": Spelunky2LocationData(175, "Menu"),  # Same deal as the Tablet, but with Jungle and Volcana
    "Arrow of Light Journal Entry": Spelunky2LocationData(176, "Sunken City"),
    "Wooden Shield Journal Entry": Spelunky2LocationData(177, "Jungle"),  # From Tiki Men
    "Metal Shield Journal Entry": Spelunky2LocationData(178, "Tide Pool"),  # Uncommon drop from Pangxie
    "Idol Journal Entry": Spelunky2LocationData(179, "Dwelling"),
    "The Tusk Idol Journal Entry": Spelunky2LocationData(180, "Tide Pool"),
    "Curse Pot Journal Entry": Spelunky2LocationData(181, "Dwelling"),
    "Ushabti Journal Entry": Spelunky2LocationData(182, "Neo Babylon"),
    "Eggplant Journal Entry": Spelunky2LocationData(183, "Ice Caves"),  # Required to have by this point normally if going for Eggplant World
    "Cooked Turkey Journal Entry": Spelunky2LocationData(184, "Dwelling"),
    "Elixir Journal Entry": Spelunky2LocationData(185, "Temple"),
    "Four-Leaf Clover Journal Entry": Spelunky2LocationData(186, "Menu"),  # Guaranteed on Black Market and Vlad's Castle levels
}

trap_entries = {
    "Spikes Journal Entry": Spelunky2LocationData(187, "Dwelling"),
    "Arrow Trap Journal Entry": Spelunky2LocationData(188, "Dwelling"),
    "Totem Trap Journal Entry": Spelunky2LocationData(189, "Dwelling"),
    "Log Trap Journal Entry": Spelunky2LocationData(190, "Dwelling"),
    "Spear Trap Journal Entry": Spelunky2LocationData(191, "Jungle"),
    "Thorny Vine Journal Entry": Spelunky2LocationData(192, "Jungle"),
    "Bear Trap Journal Entry": Spelunky2LocationData(193, "Jungle"),
    "Powder Box Journal Entry": Spelunky2LocationData(194, "Volcana"),
    "Falling Platform Journal Entry": Spelunky2LocationData(195, "Volcana"),
    "Spikeball Journal Entry": Spelunky2LocationData(196, "Volcana"),
    "Lion Trap Journal Entry": Spelunky2LocationData(197, "Tide Pool"),
    "Giant Clam Journal Entry": Spelunky2LocationData(198, "Tide Pool"),
    "Sliding Wall Journal Entry": Spelunky2LocationData(199, "Tide Pool"),
    "Crush Trap Journal Entry": Spelunky2LocationData(200, "Temple"),
    "Giant Crush Trap Journal Entry": Spelunky2LocationData(201, "Temple"),
    "Boulder Journal Entry": Spelunky2LocationData(202, "Ice Caves"),
    "Spring Trap Journal Entry": Spelunky2LocationData(203, "Ice Caves"),
    "Landmine Journal Entry": Spelunky2LocationData(204, "Ice Caves"),
    "Laser Trap Journal Entry": Spelunky2LocationData(205, "Neo Babylon"),
    "Spark Trap Journal Entry": Spelunky2LocationData(206, "Neo Babylon"),
    "Frog Trap Journal Entry": Spelunky2LocationData(207, "Sunken City"),
    "Sticky Trap Journal Entry": Spelunky2LocationData(208, "Sunken City"),
    "Bone Drop Journal Entry": Spelunky2LocationData(209, "Sunken City"),
    "Egg Sac Journal Entry": Spelunky2LocationData(210, "Sunken City"),
}

location_data_table = {

    **place_entries,
    **people_entries,
    **bestiary_entries,
    **item_entries,
    **trap_entries,
}



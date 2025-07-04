import typing


from BaseClasses import Item, ItemClassification
from typing import Optional

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification

class JigsawItem(Item):
    game: str = "Jigsaw"
    
    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        self.name = name
        self.classification = classification
        self.player = player
        self.code = code
        self.location = None

item_table = {
    f"{i} Puzzle Piece{'s' if i > 1 else ''}": ItemData(234782000 + (i - 1), 
        ItemClassification.progression if i >= 25 else ItemClassification.progression_skip_balancing)
    for i in range(1, 501)
}

item_table["1 Fake Puzzle Piece"] = ItemData(234785000 + (1 - 1), ItemClassification.trap)


encouragements = [
    "Good job!", "Wowza!", "You rock!", "Nailed it!", "Heck yes!",
    "Bravo!", "Go you!", "Yayyy!", "Woohoo!", "So cool!",
    "Impressive!", "Boom!", "Love it!", "Sweet!", "Well done!",
    "That’s it!", "Yes, queen!", "You did it!", "Legendary!", "Whoa, nice!",
    "High five!", "Keep it up!", "Fantastic!", "Yesss!", "Great work!",
    "A+ effort!", "Magic!", "Crushed it!", "Woot!", "Right on!",
    "Champ!", "Boss move!", "Epic!", "Amazeballs!", "Power move!",
    "Sharp thinking!", "You shine!", "Look at you!", "Solid!", "Dreamy!",
    "Splendid!", "Too good!", "Zing!", "Way to go!", "On fire!",
    "Clean win!", "Style points!", "Whiz!", "Ace!", "Wowsers!",
    "Bang on!", "Proud of you!", "Keep slaying!", "All-star!", "Superstar!",
    "Smooth!", "Perfection!", "Slick!", 
    "King stuff!", "Top tier!", "A real one!", "Chef's kiss!", "Ultra win!",
    "Zesty!", "Delightful!", "Gold star!", "Rockstar!", "Flawless!",
    "10/10!", "Nice touch!", "Iconic!", "Gorgeous!", "So proud!",
    "Showstopper!", "Crème de la crème!", "Vibes!", "Hyped!", "Joyful!",
    "No cap!", "Peak form!", "Fire!", "Deluxe!", "Snappy!",
    "Bold move!", "Thrilling!", "Masterful!", "Super clean!", "Yum!",
    "Vivid!", "Radiant!", "Gleaming!", "Lush!", "Nifty!",
    "Killer move!", "No flaws!", "Powerhouse!", "Beaming!", "Crisp!",
    "Well played!", "Niiice!", "Unreal!", "Prime!", "Legend stuff!"
]


for i, phrase in enumerate(encouragements):
    item_id = 234781999 - i
    item_table[phrase] = ItemData(item_id, ItemClassification.filler)



item_groups = {
    "Puzzle Pieces": [key for key in item_table.keys() if "Puzzle Piece" in key]
}
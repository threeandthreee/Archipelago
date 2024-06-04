# WARNING: THIS FILE HAS BEEN GENERATED!
# Modifications to this file will not be kept.
# If you need to change something here, check out codegen.py and the templates directory.


from worlds.crosscode import prog_items
from .items import single_items_dict, items_dict
from .types.items import ItemData, ProgressiveItemChain, ProgressiveChainEntry

progressive_chains: dict[str, ProgressiveItemChain] = {
    "areaItemsAll": ProgressiveItemChain(
        display_name="Area Unlock",
        items=[
            ProgressiveChainEntry(item=items_dict['Green Leaf Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Mine Pass', 1]),
            ProgressiveChainEntry(item=items_dict['Blue Ice Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Yellow Sand Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Red Flame Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Green Seed Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Purple Bolt Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Azure Drop Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Star Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Meteor Shade', 1]),
        ],
    ),
    "areaItemsOverworld": ProgressiveItemChain(
        display_name="Overworld Area Unlock",
        items=[
            ProgressiveChainEntry(item=items_dict['Green Leaf Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Blue Ice Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Red Flame Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Green Seed Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Star Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Meteor Shade', 1]),
        ],
    ),
    "areaItemsDungeons": ProgressiveItemChain(
        display_name="Dungeon Unlock",
        items=[
            ProgressiveChainEntry(item=items_dict['Mine Pass', 1]),
            ProgressiveChainEntry(item=items_dict['Yellow Sand Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Purple Bolt Shade', 1]),
            ProgressiveChainEntry(item=items_dict['Azure Drop Shade', 1]),
        ],
    ),
}

progressive_items: dict[str, ItemData] = {
    'areaItemsAll': items_dict['Progressive Area Unlock', 1],
    'areaItemsOverworld': items_dict['Progressive Overworld Area Unlock', 1],
    'areaItemsDungeons': items_dict['Progressive Dungeon Unlock', 1],
}
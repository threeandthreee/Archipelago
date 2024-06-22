"""
Types related to JSON data
"""

import typing
from typing import TypedDict, NotRequired

class ExportChestInfo(TypedDict):
    name: str
    mwids: list[int]

class ExportCutsceneInfo(TypedDict):
    path: str
    mwids: list[int]

class ExportElementInfo(TypedDict):
    mwids: list[int]

class ExportQuestInfo(TypedDict):
    mwids: list[int]

class ExportRoomInfo(TypedDict):
    chests: NotRequired[dict[str, ExportChestInfo]]
    cutscenes: NotRequired[dict[str, list[ExportCutsceneInfo]]]
    elements: NotRequired[dict[str, ExportElementInfo]]
    quests: NotRequired[dict[str, ExportQuestInfo]]

class ExportInfo(TypedDict):
    items: dict[str, ExportRoomInfo]
    quests: dict[str, typing.Any]

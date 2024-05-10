import typing
from dataclasses import dataclass, field

from BaseClasses import Location, Region

from .condition import Condition

@dataclass
class AccessInfo:
    region: typing.Dict[str, str]
    cond: typing.Optional[list[Condition]] = None
    clearance: str = "Default"

@dataclass
class LocationData:
    name: str
    code: typing.Optional[int]
    area: typing.Optional[str] = None

class CrossCodeLocation(Location):
    game: str = "CrossCode"
    data: LocationData
    access: AccessInfo
    region: str

    def __init__(self, player: int, data: LocationData, access: AccessInfo, mode, region_dict: dict[str, Region], event_from_location=False):
        event_from_location = event_from_location and data.code is not None

        super(CrossCodeLocation, self).__init__(
            player,
            data.name if not event_from_location else data.name + " (Event)",
            data.code if not event_from_location else None,
            region_dict[access.region[mode]]
        )

        self.data = data
        self.access = access
        self.event = False
        self.region = access.region[mode]

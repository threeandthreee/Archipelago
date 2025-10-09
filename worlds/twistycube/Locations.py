import typing

from BaseClasses import Location

class LocData(typing.NamedTuple):
    id: int
    region: str
    reqs: dict


class TwistyCubeLocation(Location):
    game: str = "Twisty Cube"

    def __init__(self, player: int, name: str, address: typing.Optional[int], reqs, parent):
        super().__init__(player, name, address, parent)
        self.reqs = reqs
        
location_table = {f"{i} Correct": LocData(267780000 + i, "Board", i) for i in range(1, 6*4*4+1)}

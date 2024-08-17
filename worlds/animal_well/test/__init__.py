from test.bases import WorldTestBase
from .. import AnimalWellWorld


class AWTestBase(WorldTestBase):
    game = "ANIMAL WELL"
    world: AnimalWellWorld

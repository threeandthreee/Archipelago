from typing import ClassVar

from test.bases import WorldTestBase


class AnodyneTestBase(WorldTestBase):
    game = "Anodyne"
    player: ClassVar[int] = 1

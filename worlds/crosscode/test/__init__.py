from test.bases import WorldTestBase
from .. import CrossCodeWorld
from ..types.world import WorldData
from ..types.pools import Pools

class CrossCodeTestBase(WorldTestBase):
    world: CrossCodeWorld
    game = "CrossCode"

    world_data: WorldData
    pools: Pools

    def setUp(self):
        super().setUp()
        if self.auto_construct:
            self.world_data = self.world.world_data
            self.pools = self.world.pools

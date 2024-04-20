from worlds.AutoWorld import LogicMixin, World
from . import Locations
from .Locations import dragons


class LogicFunctions(LogicMixin):
    def _ff6wc_has_enough_characters(self, world, player):
        return self.has_group("characters", player, world.CharacterCount[player])

    def _ff6wc_has_enough_espers(self, world, player):
        return self.has_group("espers", player, world.EsperCount[player])

    def _ff6wc_has_enough_dragons(self, world, player):
        return self.has_group("dragons", player, world.DragonCount[player])

    def _ff6wc_has_enough_bosses(self, world, player):
        return self.has("Busted!", player, world.BossCount[player])
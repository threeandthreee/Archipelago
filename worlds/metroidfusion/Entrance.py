from BaseClasses import Entrance
from entrance_rando import ERPlacementState

first_location_tops = [
    "Operations Deck Elevator Top Destination",
]

first_location_bottoms = [
    "Operations Deck Elevator Bottom Destination",
    "Sector 2 Hub Destination"
]

class FusionEntrance(Entrance):
    def can_connect_to(self, other: Entrance, dead_end: bool, er_state: "ERPlacementState") -> bool:
        reachable_locations = self.parent_region.multiworld.get_reachable_locations(er_state.collection_state, self.player)
        if self.name == "Sector Hub Elevator 1 Top Destination":
            if len(reachable_locations) == 0:
                if other.name not in first_location_bottoms:
                    return False
        if self.name == "Sector Hub Elevator Bottom Destination":
            if len(reachable_locations) == 0:
                if other.name not in first_location_tops:
                    return False
        return super().can_connect_to(other, dead_end, er_state)
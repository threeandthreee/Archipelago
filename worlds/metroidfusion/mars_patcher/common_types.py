from typing import Annotated, TypeAlias

from .auto_generated_types import Areaid, Typeu8

AreaId: TypeAlias = Areaid
RoomId: TypeAlias = Typeu8

AreaRoomPair = tuple[AreaId, RoomId]

MinimapId: TypeAlias = Annotated[int, "0 <= value < 10"]

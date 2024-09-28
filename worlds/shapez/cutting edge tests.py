import worlds
from worlds.shapez import ShapezWorld

print(len(str(ShapezWorld.get_data_package_data()).encode()))
print(len(str(worlds.network_data_package).encode()))

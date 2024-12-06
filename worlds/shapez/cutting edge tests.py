# import worlds
# from worlds.shapez import ShapezWorld

# print(len(str(ShapezWorld.get_data_package_data()).encode()))
# print(len(str(worlds.network_data_package).encode()))

for y in ["none", "ac", "acr", "ic", "ic ar", "ac ir", "icr"]:
    for z in ["none", "av", "imp"]:
        for x in range(16):
            print(" ".join([x.__str__(), y, z, "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"]))

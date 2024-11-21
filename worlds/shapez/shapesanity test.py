import time

from worlds.shapez import locations

start = time.time()

print(f"len of shapesanity_simple is {len(locations.shapesanity_simple)}")
locations.init_shapesanity_pool()

# print(shapesanity_simple.keys())
# print(shapesanity_1_4.keys())
# print(shapesanity_two_sided.keys())
# print(shapesanity_three_parts.keys())
# print(shapesanity_four_parts.keys())
l = [len(locations.shapesanity_simple), len(locations.shapesanity_1_4), len(locations.shapesanity_two_sided),
     len(locations.shapesanity_three_parts), len(locations.shapesanity_four_parts)]
print(l, sum(l))
print(time.time() - start)

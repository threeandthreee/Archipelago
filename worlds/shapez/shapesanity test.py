import time

from worlds.shapez.locations import shapesanity_simple, shapesanity_1_4, shapesanity_two_sided, shapesanity_four_parts, \
    shapesanity_three_parts, init_shapesanity_pool

start = time.time()
init_shapesanity_pool()

print(shapesanity_simple.keys())
print(shapesanity_1_4.keys())
print(shapesanity_two_sided.keys())
print(shapesanity_three_parts.keys())
print(shapesanity_four_parts.keys())
l = [len(shapesanity_simple), len(shapesanity_1_4), len(shapesanity_two_sided),
     len(shapesanity_three_parts), len(shapesanity_four_parts)]
print(l, sum(l))
print(time.time() - start)

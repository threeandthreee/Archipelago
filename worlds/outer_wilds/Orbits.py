from random import Random
from typing import Dict, List


# Example output: (
#     ["TH", "BH", "GD", "DB", "HGT"],
#     {"HGT":30, "TH":60, "BH":90, "GD":120, "DB":150, "SS":180, "AR":210, "HL":240, "OPC":270},
#     {"ET":"up", "AT":"down", "TH":"left", "BH":"right"}
# )
def generate_random_orbits(random: Random) -> (List[str], Dict[str, int], Dict[str, str]):
    planet_order = ["HGT", "TH", "BH", "GD", "DB"]
    random.shuffle(planet_order)

    # We want vanilla/flat orbits, angled orbits and vertical orbits to all be reasonably likely,
    # and we want to avoid collisions that would potentially make a location unreachable
    # or kill the player in sudden, unpredictable ways. Specific tests we did include:
    # - While not exhaustively tested, The Interloper is unlikely to be an issue since I'm not
    # changing the Interloper itself, I'm not randomizing where each planet starts along its orbit,
    # the vanilla orbits don't collide with it, and any angle besides 0 and 180 prevents collisions.
    # - The Stranger and Dreamworld have a fixed position 45 degrees above the vanilla orbital plane,
    # about the same distance from the sun as Brittle Hollow's vanilla orbit. A planet at 60 degrees
    # may become visible in the Dreamworld "sky", but won't cause any problems.
    # - The black void where Dark Bramble rooms are created has a fixed position at 90 degrees below
    # the Sun. If all orbits are vertical, GD and DB (and the map satellite) intersect this void.

    # Thus, we use multiples of 30 both to avoid the Stranger and to get a decent variety of
    # angles without it being too obvious that we're only using a fixed set of choices.
    possible_angles = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    # And the 2 outermost orbits need to be non-vertical to avoid the DB void.
    # This rule is the main reason we have to choose planet_order and orbit_angles together.
    non_vertical_angles = [a for a in possible_angles if a != 90 and a != 270]

    orbit_angles: Dict[str, int] = {}
    for index, planet in enumerate(planet_order):
        if index < 3:
            orbit_angles[planet] = random.choice(possible_angles)
        else:
            orbit_angles[planet] = random.choice(non_vertical_angles)

    # No subtle constraints for the satellite orbits
    for satellite in ["SS", "AR", "HL", "OPC"]:
        orbit_angles[satellite] = random.choice(possible_angles)

    # Rotations could be generated separately from order and angles, but since we have to
    # generate the order and angles together, keeping all three together feels simpler.

    # These are static properties of Unity's Vector3 class, e.g. Vector3.up is (0, 1, 0)
    possible_axis_directions = ["up", "down", "left", "right", "forward", "back", "zero"]

    # I couldn't get the HGT as a whole to change rotation, but each of the Ember and Ash Twins
    # can change rotation, so for this part of the code those are two separate "planets".
    # GD and DB do not rotate, and I've heard GD's islands would stop working if it did rotate.
    # The satellites' axes can also be changed, but it's not noticeable enough to bother.
    rotation_axes: Dict[str, str] = {}
    for planet in ["ET", "AT", "TH", "BH"]:
        rotation_axes[planet] = random.choice(possible_axis_directions)

    return planet_order, orbit_angles, rotation_axes


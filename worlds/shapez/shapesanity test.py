from typing import List, Dict


def color_to_needed_building(color_list: List[str]) -> str:
    for next_color in color_list:
        if next_color in ["Yellow", "Purple", "Cyan", "White", "y", "p", "c", "w"]:
            return "Mixed"
    for next_color in color_list:
        if next_color not in ["Uncolored", "u"]:
            return "Painted"
    return "Uncolored"


shapesanity_simple: Dict[str, str] = {}
shapesanity_1_4: Dict[str, str] = {}
shapesanity_two_sided: Dict[str, str] = {}
shapesanity_three_parts: Dict[str, str] = {}
shapesanity_four_parts: Dict[str, str] = {}

# same shapes && same color
for color in ["Red", "Blue", "Green", "Yellow", "Purple", "Cyan", "White", "Uncolored"]:
    color_region = color_to_needed_building([color])
    shapesanity_simple[f"Shapesanity {color} Circle"] = f"Shapesanity Full {color_region}"
    shapesanity_simple[f"Shapesanity {color} Square"] = f"Shapesanity Full {color_region}"
    shapesanity_simple[f"Shapesanity {color} Star"] = f"Shapesanity Full {color_region}"
    shapesanity_simple[f"Shapesanity {color} Windmill"] = f"Shapesanity East Windmill {color_region}"
for shape in ["Circle", "Square", "Star", "Windmill"]:
    for color in ["Red", "Blue", "Green", "Yellow", "Purple", "Cyan", "White", "Uncolored"]:
        color_region = color_to_needed_building([color])
        shapesanity_simple[f"Shapesanity Half {color} {shape}"] \
            = f"Shapesanity Half {color_region}"
        shapesanity_simple[f"Shapesanity {color} {shape} Piece"] \
            = f"Shapesanity Piece {color_region}"
        shapesanity_simple[f"Shapesanity Cut Out {color} {shape}"] \
            = f"Shapesanity Stitched {color_region}"
        shapesanity_simple[f"Shapesanity Cornered {color} {shape}"] \
            = f"Shapesanity Stitched {color_region}"
# one color && 4 shapes (including empty)
for first_color in ["r", "g", "b", "y", "p", "c"]:
    for second_color in ["g", "b", "y", "p", "c", "w"]:
        if not first_color == second_color:
            for third_color in ["b", "y", "p", "c", "w", "u"]:
                if third_color not in [first_color, second_color]:
                    for fourth_color in ["y", "p", "c", "w", "u"]:
                        if fourth_color not in [first_color, second_color, third_color]:
                            colors = [first_color, second_color, third_color, fourth_color]
                            for shape in ["Circle", "Square", "Star"]:
                                shapesanity_1_4[f"Shapesanity {''.join(sorted(colors))} {shape}"] \
                                    = f"Shapesanity Colorful Full {color_to_needed_building(colors)}"
                            shapesanity_1_4[f"Shapesanity {''.join(sorted(colors))} Windmill"] \
                                = f"Shapesanity Colorful East Windmill {color_to_needed_building(colors)}"
                    fourth_color = "-"
                    colors = [first_color, second_color, third_color, fourth_color]
                    for shape in ["Circle", "Square", "Windmill", "Star"]:
                        shapesanity_1_4[f"Shapesanity {''.join(sorted(colors))} {shape}"] \
                            = f"Shapesanity Stitched {color_to_needed_building(colors)}"
for color in ["Red", "Blue", "Green", "Yellow", "Purple", "Cyan", "White", "Uncolored"]:
    for first_shape in ["C", "R"]:
        for second_shape in ["R", "W"]:
            if not first_shape == second_shape:
                for third_shape in ["W", "S"]:
                    if not third_shape == second_shape:
                        for fourth_shape in ["S", "-"]:
                            if not fourth_shape == third_shape:
                                shapes = [first_shape, second_shape, third_shape, fourth_shape]
                                # one shape && 4 colors (including empty)
                                shapesanity_1_4[f"Shapesanity {color} {''.join(sorted(shapes))}"] \
                                    = f"Shapesanity Stitched {color_to_needed_building([color])}"
for first_shape in ["C", "R", "W", "S"]:
    for second_shape in ["C", "R", "W", "S"]:
        for first_color in ["r", "g", "b", "y", "p", "c", "w", "u"]:
            for second_color in ["r", "g", "b", "y", "p", "c", "w", "u"]:
                first_combo = first_shape+first_color
                second_combo = second_shape+second_color
                if not first_combo == second_combo:  # 2 different shapes || 2 different colors
                    color_region = color_to_needed_building([first_color, second_color])
                    ordered_combo = " ".join(sorted([first_combo, second_combo]))
                    # No empty corner && (2 different shapes || 2 different colors)
                    if first_shape == second_shape:
                        shapesanity_two_sided[f"Shapesanity 3-1 {first_combo} {second_combo}"] \
                            = f"Shapesanity Colorful Full {color_region}"
                        if first_shape == "W":
                            shapesanity_two_sided[f"Shapesanity Half-Half {ordered_combo}"] \
                                = f"Shapesanity East Windmill {color_region}"
                        else:
                            shapesanity_two_sided[f"Shapesanity Half-Half {ordered_combo}"] \
                                = f"Shapesanity Colorful Full {color_region}"
                        shapesanity_two_sided[f"Shapesanity Checkered {ordered_combo}"] \
                            = f"Shapesanity Colorful Full {color_region}"
                        shapesanity_two_sided[f"Shapesanity Adjacent Singles {ordered_combo}"] \
                            = f"Shapesanity Colorful Half {color_region}"
                    else:
                        shapesanity_two_sided[f"Shapesanity 3-1 {first_combo} {second_combo}"] \
                            = f"Shapesanity Stitched {color_region}"
                        shapesanity_two_sided[f"Shapesanity Half-Half {ordered_combo}"] \
                            = f"Shapesanity Half-Half {color_region}"
                        shapesanity_two_sided[f"Shapesanity Checkered {ordered_combo}"] \
                            = f"Shapesanity Stitched {color_region}"
                        shapesanity_two_sided[f"Shapesanity Adjacent Singles {ordered_combo}"] \
                            = f"Shapesanity Stitched {color_region}"
                    # 2 empty corners && (2 different shapes || 2 different colors)
                    shapesanity_two_sided[f"Shapesanity Cornered Singles {ordered_combo}"] \
                        = f"Shapesanity Stitched {color_region}"
                    # 1 empty corner && (2 different shapes || 2 different colors)
                    shapesanity_two_sided[f"Shapesanity Adjacent 2-1 {first_combo} {second_combo}"] \
                        = f"Shapesanity Stitched {color_region}"
                    shapesanity_two_sided[f"Shapesanity Cornered 2-1 {first_combo} {second_combo}"] \
                        = f"Shapesanity Stitched {color_region}"
                    # Now 3-part shapes
                    for third_shape in ["C", "R", "W", "S"]:
                        for third_color in ["r", "g", "b", "y", "p", "c", "w", "u"]:
                            third_combo = third_shape+third_color
                            if third_combo not in [first_combo, second_combo]:
                                colors = [first_color, second_color, third_color]
                                color_region = color_to_needed_building(colors)
                                ordered_two = " ".join(sorted([second_combo, third_combo]))
                                if not (first_color == second_color == third_color or
                                        first_shape == second_shape == third_shape):
                                    ordered_all = " ".join(sorted([first_combo, second_combo, third_combo]))
                                    shapesanity_three_parts[f"Shapesanity Singles {ordered_all}"] \
                                        = f"Shapesanity Stitched {color_region}"
                                if not second_shape == third_shape:
                                    shapesanity_three_parts[f"Shapesanity Adjacent 2-1-1 {first_combo} {ordered_two}"] \
                                        = f"Shapesanity Stitched {color_region}"
                                    shapesanity_three_parts[f"Shapesanity Cornered 2-1-1 {first_combo} {ordered_two}"] \
                                        = f"Shapesanity Stitched {color_region}"
                                elif first_shape == second_shape:
                                    shapesanity_three_parts[f"Shapesanity Adjacent 2-1-1 {first_combo} {ordered_two}"] \
                                        = f"Shapesanity Colorful Full {color_region}"
                                    shapesanity_three_parts[f"Shapesanity Cornered 2-1-1 {first_combo} {ordered_two}"] \
                                        = f"Shapesanity Colorful Full {color_region}"
                                else:
                                    shapesanity_three_parts[f"Shapesanity Adjacent 2-1-1 {first_combo} {ordered_two}"] \
                                        = f"Shapesanity Colorful Half-Half {color_region}"
                                    shapesanity_three_parts[f"Shapesanity Cornered 2-1-1 {first_combo} {ordered_two}"] \
                                        = f"Shapesanity Stitched {color_region}"
                                # Now 4-part shapes
                                for fourth_shape in ["C", "R", "W", "S"]:
                                    for fourth_color in ["r", "g", "b", "y", "p", "c", "w", "u"]:
                                        fourth_combo = fourth_shape+fourth_color
                                        if fourth_combo not in [first_combo, second_combo, third_combo]:
                                            if not (first_color == second_color == third_color == fourth_color or
                                                    first_shape == second_shape == third_shape == fourth_shape):
                                                colors = [first_color, second_color, third_color, fourth_color]
                                                color_region = color_to_needed_building(colors)
                                                ordered_all = " ".join(sorted([first_combo, second_combo,
                                                                               third_combo, fourth_combo]))
                                                if ((first_shape == second_shape and third_shape == fourth_shape)
                                                    or (first_shape == third_shape and second_shape == fourth_shape)
                                                    or (first_shape == fourth_shape and third_shape == second_shape)):
                                                    shapesanity_four_parts[f"Shapesanity Singles {ordered_all}"] \
                                                        = f"Shapesanity Colorful Half-Half {color_region}"
                                                else:
                                                    shapesanity_four_parts[f"Shapesanity Singles {ordered_all}"] \
                                                        = f"Shapesanity Stitched {color_region}"

print(shapesanity_simple.keys())
print(shapesanity_1_4.keys())
print(shapesanity_two_sided.keys())
print(shapesanity_three_parts.keys())
print(shapesanity_four_parts.keys())
l = [len(shapesanity_simple), len(shapesanity_1_4), len(shapesanity_two_sided),
     len(shapesanity_three_parts), len(shapesanity_four_parts)]
print(l, sum(l))

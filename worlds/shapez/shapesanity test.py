def color_to_needed_building(color1: str, color2: str = "Uncolored") -> str:
    if color1 in ["Uncolored", "u"] and color2 in ["Uncolored", "u"]:
        return "Uncolored"
    elif (color1 in ["Yellow", "Purple", "Cyan", "White", "y", "p", "c", "w"] or
          color2 in ["Yellow", "Purple", "Cyan", "White", "y", "p", "c", "w"]):
        return "Mixed"
    else:
        return "Painted"


def color_list_to_needed_building(color_list: list[str]) -> str:
    for next_color in color_list:
        if next_color in ["y", "p", "c", "w"]:
            return "Mixed"
    return "Painted"


shapesanity_simple: dict[str, str] = {}
shapesanity_medium: dict[str, str] = {}
shapesanity_complex: dict[str, str] = {}

for shape in ["Circle", "Square", "Star"]:
    for color in ["Red", "Blue", "Green", "Yellow", "Purple", "Cyan", "White", "Uncolored"]:
        # same shapes && same color
        shapesanity_simple[f"Shapesanity {color} {shape}"] \
            = f"Shapesanity Unprocessed {color_to_needed_building(color)}"
        shapesanity_simple[f"Shapesanity Half {color} {shape}"] \
            = f"Shapesanity Cut {color_to_needed_building(color)}"
        shapesanity_simple[f"Shapesanity {color} {shape} Piece"] \
            = f"Shapesanity Cut Rotated {color_to_needed_building(color)}"
        shapesanity_simple[f"Shapesanity Cut Out {color} {shape}"] \
            = f"Shapesanity Stitched {color_to_needed_building(color)}"
        shapesanity_simple[f"Shapesanity Cornered {color} {shape}"] \
            = f"Shapesanity Stitched {color_to_needed_building(color)}"
for color in ["Red", "Blue", "Green", "Yellow", "Purple", "Cyan", "White", "Uncolored"]:
    shapesanity_simple[f"Shapesanity {color} Windmill"] \
        = f"Shapesanity Stitched {color_to_needed_building(color)}"
    shapesanity_simple[f"Shapesanity Half {color} Windmill"] \
        = f"Shapesanity Cut {color_to_needed_building(color)}"
    shapesanity_simple[f"Shapesanity {color} Windmill Piece"] \
        = f"Shapesanity Cut Rotated {color_to_needed_building(color)}"
    shapesanity_simple[f"Shapesanity Cut Out {color} Windmill"] \
        = f"Shapesanity Stitched {color_to_needed_building(color)}"
    shapesanity_simple[f"Shapesanity Cornered {color} Windmill"] \
        = f"Shapesanity Stitched {color_to_needed_building(color)}"
for shape in ["Circle", "Square", "Windmill", "Star"]:
    for first_color in ["r", "g", "b", "y", "p", "c"]:
        for second_color in ["g", "b", "y", "p", "c", "w"]:
            if not first_color == second_color:
                for third_color in ["b", "y", "p", "c", "w", "u"]:
                    if third_color not in [first_color, second_color]:
                        for fourth_color in ["y", "p", "c", "w", "u", "-"]:
                            if fourth_color not in [first_color, second_color, third_color]:
                                colors = [first_color, second_color, third_color, fourth_color]
                                # one color && 4 shapes (including empty)
                                shapesanity_medium[f"Shapesanity {''.join(sorted(colors))} {shape}"] \
                                    = f"Shapesanity Stitched {color_list_to_needed_building(colors)}"
for color in ["Red", "Blue", "Green", "Yellow", "Purple", "Cyan", "White", "Uncolored"]:
    for first_shape in ["C", "R"]:
        for second_shape in ["R", "W"]:
            if not first_shape == second_shape:
                for third_shape in ["W", "S"]:
                    if third_shape not in [first_shape, second_shape]:
                        for fourth_shape in ["S", "-"]:
                            if fourth_shape not in [first_shape, second_shape, third_shape]:
                                shapes = [first_shape, second_shape, third_shape, fourth_shape]
                                # one shape && 4 colors (including empty)
                                shapesanity_medium[f"Shapesanity {color} {''.join(sorted(shapes))}"] \
                                    = f"Shapesanity Stitched {color_to_needed_building(color)}"
for first_shape in ["C", "R", "W", "S"]:
    for second_shape in ["C", "R", "W", "S"]:
        for first_color in ["r", "g", "b", "y", "p", "c", "w", "u"]:
            for second_color in ["r", "g", "b", "y", "p", "c", "w", "u"]:
                first_combo = first_shape+first_color
                second_combo = second_shape+second_color
                if not first_combo == second_combo:  # 2 different shapes || 2 different colors
                    if first_combo < second_combo:
                        ordered_combo = f"{first_combo} {second_combo}"
                    else:
                        ordered_combo = f"{second_combo} {first_combo}"
                    # No empty corner && (2 different shapes || 2 different colors)
                    shapesanity_complex[f"Shapesanity 3-1 {first_combo} {second_combo}"] \
                        = f"Shapesanity Stitched {color_to_needed_building(first_color, second_color)}"
                    if first_shape == "W" and second_shape == "W":  # Full windmill
                        shapesanity_complex[f"Shapesanity Half-Half {ordered_combo}"] \
                            = f"Shapesanity Stitched {color_to_needed_building(first_color, second_color)}"
                    else:
                        shapesanity_complex[f"Shapesanity Half-Half {ordered_combo}"] \
                            = f"Shapesanity Half-Half {color_to_needed_building(first_color, second_color)}"
                    shapesanity_complex[f"Shapesanity Checkered {ordered_combo}"] \
                        = f"Shapesanity Stitched {color_to_needed_building(first_color, second_color)}"
                    # 2 empty corners && (2 different shapes || 2 different colors)
                    shapesanity_complex[f"Shapesanity Cornered {ordered_combo}"] \
                        = f"Shapesanity Stitched {color_to_needed_building(first_color, second_color)}"
                    shapesanity_complex[f"Shapesanity Adjacent {ordered_combo}"] \
                        = f"Shapesanity Stitched {color_to_needed_building(first_color, second_color)}"
                    # 1 empty corner && (2 different shapes || 2 different colors)
                    shapesanity_complex[f"Shapesanity Adjacent 2-1 {first_combo} {second_combo}"] \
                        = f"Shapesanity Stitched {color_to_needed_building(first_color, second_color)}"
                    shapesanity_complex[f"Shapesanity Cornered 2-1 {first_combo} {second_combo}"] \
                        = f"Shapesanity Stitched {color_to_needed_building(first_color, second_color)}"

print(shapesanity_simple.keys())
print(shapesanity_medium.keys())
print(shapesanity_complex.keys())
l = [len(shapesanity_simple), len(shapesanity_medium), len(shapesanity_complex)]
print(l, sum(l))

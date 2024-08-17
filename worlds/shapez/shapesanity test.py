def color_to_needed_building(color1: str, color2: str = "Uncolored") -> str:
    if color1 in ["Uncolored", "u"] and color2 in ["Uncolored", "u"]:
        return "Uncolored"
    elif (color1 in ["Yellow", "Purple", "Cyan", "White", "y", "p", "c", "w"] or
          color2 in ["Yellow", "Purple", "Cyan", "White", "y", "p", "c", "w"]):
        return "Mixed"
    else:
        return "Painted"


shapesanity_simple: dict[str, str] = {}
shapesanity_complex: dict[str, str] = {}

for shape in ["Circle", "Square", "Windmill", "Star"]:
    for color in ["Red", "Blue", "Green", "Yellow", "Purple", "Cyan", "White", "Uncolored"]:
        shapesanity_simple[f"Shapesanity {color} {shape}"] = f"Shapesanity Unprocessed {color_to_needed_building(color)}"
        shapesanity_simple[f"Shapesanity Half {color} {shape}"] = f"Shapesanity Cut {color_to_needed_building(color)}"
        shapesanity_simple[f"Shapesanity {color} {shape} Piece"] = f"Shapesanity Cut Rotated {color_to_needed_building(color)}"
        shapesanity_simple[f"Shapesanity Cut Out {color} {shape}"] \
            = f"Shapesanity Stitched {color_to_needed_building(color)}"
        shapesanity_simple[f"Shapesanity Cornered {color} {shape}"] \
            = f"Shapesanity Stitched {color_to_needed_building(color)}"
for first_shape in ["C", "R", "W", "S"]:
    for second_shape in ["C", "R", "W", "S"]:
        for first_color in ["r", "g", "b", "y", "p", "c", "w", "u"]:
            for second_color in ["r", "g", "b", "y", "p", "c", "w", "u"]:
                first_combo = first_shape+first_color
                second_combo = second_shape+second_color
                if not first_combo == second_combo:
                    if first_combo < second_combo:
                        ordered_combo = f"{first_combo} {second_combo}"
                    else:
                        ordered_combo = f"{second_combo} {first_combo}"
                    shapesanity_complex[f"Shapesanity 3-1 {first_combo} {second_combo}"] \
                        = f"Shapesanity Stitched {color_to_needed_building(first_color, second_color)}"
                    shapesanity_complex[f"Shapesanity Half-Half {ordered_combo}"] \
                        = f"Shapesanity Half-Half {color_to_needed_building(first_color, second_color)}"
                    shapesanity_complex[f"Shapesanity Checkered {ordered_combo}"] \
                        = f"Shapesanity Stitched {color_to_needed_building(first_color, second_color)}"

print(shapesanity_simple)
print(shapesanity_complex)
print(len(shapesanity_simple), len(shapesanity_complex))

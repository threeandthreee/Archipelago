
class SpeciesEntry:
    type_1: str
    type_2: str
    base_hp: int
    base_attack: int
    base_defense: int
    base_sp_attack: int
    base_sp_defense: int
    base_speed: int
    catch_rate: int
    gender_ratio: int
    # starts with 0 for base evolutions
    evolution_stage: int
    # (primary, secondary, hidden)
    abilities: tuple[str, str, str]
    # tuple(method, parameter, evolve into)
    evolutions: list[tuple[str, int, str]]
    # tuple(level, move name)
    level_up_moves: list[tuple[int, str]]
    # TM number (internal order is TM1-95 HM1-6)
    tm_hm_moves: set[str]

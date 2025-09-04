PLANTS_IDS = {
    "TREE": 1,
    "BERRIES": 2,
}
ANIMALS_IDS = {
    "RABBIT": 1,
}
HUMANS_IDS = {
    "HUMAN": 1,
}

TERRAINS_IDS = {
    "WATER": 0,
    "GRASS": 1,
}

KINDS = {
    "TERRAIN": TERRAINS_IDS,
    "PLANT": PLANTS_IDS,
    "ANIMAL": ANIMALS_IDS,
    "HUMAN": HUMANS_IDS,
}


def get_id(group_name:str, kind_name:str):
    try:
        group = KINDS[group_name.upper()]
        return group.get(kind_name.upper())
    except (AttributeError, KeyError):
        raise ValueError(f"Invalid kind name '{kind_name}' for group '{group_name}'")






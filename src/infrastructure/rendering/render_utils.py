
KIND_BITS = 8
ID_BITS = 16
ID_MASK = (1 << ID_BITS) - 1

SPRITE_IDS_DICTIONARY = {
    "GRASS": 1,
    "WATER": 2,
    "TREE": 3,
    "BERRIES": 4,
    "RABBIT": 5,
    "HUMAN": 6,
}

KIND_DICTIONARY= {
    "TILE": 0,
    "PLANT": 1,
    "ANIMAL": 2,
    "HUMAN": 3
}


def get_kind_id(kind_name):
    return KIND_DICTIONARY[kind_name.upper()]

def get_sprite_id(sprite_name):
    return SPRITE_IDS_DICTIONARY[sprite_name.upper()]

def get_alive_val(is_alive:bool):
    return 1 if is_alive else 0


def render_uid(kind_id: int, organism_id: int) -> int:
    if not (0 <= kind_id < (1 << KIND_BITS)):
        raise ValueError(f"Kind number is out of range: {kind_id}")
    if not (0 <= organism_id < (1 << ID_BITS)):
        raise ValueError(f"Local id number is out of range: {organism_id}")

    return kind_id << ID_BITS | organism_id & ID_MASK


def unpack_render_uid(uid:int) -> tuple[int, int]:
    return uid >> ID_BITS, uid & ID_MASK

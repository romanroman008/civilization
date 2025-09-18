
   # kind(1)

PLANTS_IDS = {
    "tree": 1,
    "berries": 2,
}
ANIMALS_IDS = {
    "rabbit": 1,
}
HUMANS_IDS = {
    "human": 1,
}

TERRAINS_IDS = {
    "water": 1,
    "grass": 2,
}

GROUP_DICT = {
    "terrain": TERRAINS_IDS,
    "plant": PLANTS_IDS,
    "animal": ANIMALS_IDS,
    "human": HUMANS_IDS,
}

GROUP_IDS = {
    "terrain": 1,
    "plant": 2,
    "animal": 3,
    "human": 4,
}

GROUP_BITS = 3
KIND_BITS = 8
KIND_MASK = (1 << KIND_BITS) - 1


class IdRegistry:
    __slots__ = ("_name_to_id", "_id_to_name", "_id_to_group")
    def __init__(self):
        self._name_to_id: dict[str, int] = {}
        self._id_to_name: dict[int, str] = {}
        self._id_to_group: dict[int, str] = {}
        self._register_all_objects()

    @staticmethod
    def _normalize_name(name:str):
        return name.strip().casefold()

    def _register_all_objects(self):

        for group_name, group  in GROUP_DICT.items():
            group_id = GROUP_IDS[group_name]
            self._id_to_group[group_id] = group_name
            for kind_name, kind_id in group.items():
                id = group_id << KIND_BITS | kind_id & KIND_MASK
                self._name_to_id[kind_name] = id
                self._id_to_name[id] = kind_name

    def code_object(self, kind_name:str):
        return self._name_to_id.get(kind_name.casefold(),-1)

    def decode_object(self, id:int):
        return self._id_to_name.get(id, "UNKNOWN").upper()

    def get_organism_group_from_id(self, id: int):
        group_id = id >> KIND_BITS
        return self._id_to_group.get(group_id, "UNKNOWN").casefold()








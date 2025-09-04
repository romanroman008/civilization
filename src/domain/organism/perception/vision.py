from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.organism.organism_id import OrganismID
from domain.organism.perception.perception import Perception
from domain.organism.perception.target_info import TargetInfo
from domain.organism.transform.transform import TransformReadOnly

from domain.world_map.vision_port_protocol import VisionPortProtocol

from shared.id_registry import IdRegistry


class Vision:
    def __init__(self,
                 transform:TransformReadOnly,
                 vision_port: VisionPortProtocol,
                 id_registry: IdRegistry,
                 range = 5):
        self._vision_port = vision_port
        self._id_registry = id_registry
        self._transform = transform
        self._range = range
        self._perception: Perception = self._vision_port.get_vision(transform.position, 5)



    def update(self, target: TargetInfo | None = None) -> TargetInfo | None:
        self._perception = self._vision_port.get_vision(self._transform.position, self._range)
        if target:
            i = self.get_index_by_id(target.id)
            if i == -1:
                target.update()
                return target
            perception = self._perception
            target.update(Position(perception.xs[i], perception.ys[i]))
            return target
        return None

    def get_index_by_id(self, organism_id:OrganismID):
        perception = self._perception
        organism_kind_id = self._id_registry.code_object(organism_id.kind)
        organism_id = organism_id.id
        for i in range(len(perception.xs)):
            if perception.organisms[i] == organism_kind_id:
                if perception.xs[i] == organism_id:
                    return i
        return -1

    def get_index_by_coordinates(self, coordinates:Position):
        perception = self._perception
        for i in range(len(perception.xs)):
            if perception.xs[i] == coordinates.x and perception.ys[i] == coordinates.y:
                return i
        return -1

    def get_indexes_by_positions(self, positions: list[Position]):
        perception = self._perception
        indexes = []
        append  = indexes.append
        for position in positions:
            for i in range(len(perception.xs)):
                if perception.xs[i] == position.x and perception.ys[i] == position.y:
                    append(i)
        return indexes

    def get_available_positions_in_sight(self, available_terrains:set[Terrain]):
        perception = self._perception
        code_terrain = self._id_registry.code_object
        available_positions = []
        append = available_positions.append
        for terrain in available_terrains:
            terrain_id = code_terrain(terrain)
            for i in range(len(perception.xs)):
                if perception.terrains[i] == terrain_id:
                    append((perception.xs[i], perception.ys[i]))
        return available_positions


    def get_possible_move_positions(self, available_terrains:set[Terrain]) -> list[Position]:
        neighbours = self._transform.position.neighbors()
        possible_moves = []
        terrain_ids = [self._id_registry.code_object(terrain) for terrain in available_terrains]
        append = possible_moves.append
        indexes = self.get_indexes_by_positions(neighbours)
        perception = self._perception
        for i in indexes:
            if perception.terrains[i] in terrain_ids and perception.allowed[i] == 1:
                append(Position(self._perception.xs[i], self._perception.ys[i]))

        return possible_moves



    def detect_closest_animal(self):
        animals_indexes = self.get_animals_indexes()
        perception = self._perception
        min_distance = 2 * self._range
        x, y = self._transform.position.x, self._transform.position.y
        current = -1
        for i in animals_indexes:
            d = abs(perception.xs[i] - x) + abs(perception.ys[i] - y)
            if d < min_distance:
                min_distance = d
                current = i

        #zwroc perceived_obj

    def get_animals_indexes(self):
        animal_id = self._id_registry.code_group("animal")
        perception = self._perception
        result: list[int] = []
        append = result.append
        for i in range(len(perception.xs)):
            if perception.groups[i] == animal_id:
                append(i)
        return result


    def get_available_move_positions(self, allowed_terrains: list[Terrain]) -> list[Position]:
        allowed_terrain_ids = [
            self._id_registry.code_object(terrain)
            for terrain in allowed_terrains
        ]
        perception = self._perception
        available_move_positons = []
        append = available_move_positons.append

        for id in allowed_terrain_ids:
            for i in range(len(perception.xs)):

                if perception.terrains[i] == id:
                    append(Position(perception.xs[i], perception.ys[i]))

        return available_move_positons










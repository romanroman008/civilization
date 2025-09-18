from typing import Optional

from codetiming import Timer

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
                 allowed_terrains: set[Terrain],
                 range = 5):
        self._vision_port = vision_port
        self._id_registry = id_registry
        self._transform = transform
        self._range = range
        self._available_terrain_ids = [id_registry.code_object(terrain) for terrain in allowed_terrains]
        self._perception: Perception = self._vision_port.get_vision(transform.position, 5)

        self._pos_to_idx : dict[tuple[int,int], int] = {}
        self._reindex_perception()



    def _reindex_perception(self):
        m = self._pos_to_idx
        m.clear()
        xs, ys = self._perception.xs, self._perception.ys
        n = len(xs)
        for i in range(n):
            m[(xs[i], ys[i])] = i



    def update(self, target: TargetInfo | None = None) -> TargetInfo | None:
        self._perception = self._vision_port.get_vision(self._transform.position, self._range)
        self._reindex_perception()
        if target:
            i = self.get_index_by_id(target.id)
            if i == -1:
                target.update()
                return target
            perception = self._perception
            target.update(Position(perception.xs[i], perception.ys[i]), (perception.offsets_x[i], perception.offsets_y[i]))
            return target
        return None


    def get_animals_in_given_distance(self, required_distance: int = 2):
        perception = self._perception
        position = self._transform.position
        get_organism_group = self._id_registry.get_organism_group_from_id
        decode = self._id_registry.decode_object
        for i in range(len(perception.xs)):
            if perception.organisms_id[i] == 0:
                continue
            group_name = get_organism_group(perception.organisms[i])
            if group_name == "animal":
                distance = (abs(position.x - (perception.xs[i] + perception.offsets_x[i] / 100))
                            + abs(position.y - (perception.ys[i] + perception.offsets_y[i] / 100)))
                if distance <= required_distance:
                    yield OrganismID(decode(perception.organisms[i]), perception.organisms_id[i])




    def get_index_by_id(self, organism_id:OrganismID):
        perception = self._perception
        organism_kind_id = self._id_registry.code_object(organism_id.kind)
        organism_id = organism_id.id
        for i in range(len(perception.xs)):
            if perception.organisms[i] == organism_kind_id:
                if perception.organisms_id[i] == organism_id:
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

    def get_available_positions_in_sight(self, allowed_terrains:set[Terrain]):
        perception = self._perception
        code_terrain = self._id_registry.code_object
        available_positions = []
        append = available_positions.append
        for terrain in allowed_terrains:
            terrain_id = code_terrain(terrain)
            for i in range(len(perception.xs)):
                if perception.terrains[i] == terrain_id:
                    append((perception.xs[i], perception.ys[i]))
        return available_positions


    def get_possible_move_positions(self, anchor: Position = None) -> list[Position]:
        if anchor:
            neighbours = anchor.neighbors()
        else:
            neighbours = self._transform.position.neighbors()
        possible_moves = []
        terrain_ids = self._available_terrain_ids
        append = possible_moves.append
        perception = self._perception
        pos_to_idx = self._pos_to_idx

        for neighbour in neighbours:
            i = pos_to_idx.get((neighbour.x, neighbour.y))
            if i is None:
                continue
            if perception.terrains[i] in terrain_ids and perception.allowed[i] == 1:
                append(Position(self._perception.xs[i], self._perception.ys[i]))

        return possible_moves

    def get_neighbours_with_allowed_terrains(self, position: Position) -> list[Position]:
        neighbours = position.neighbors()
        possible_moves = []
        terrain_ids = self._available_terrain_ids
        append = possible_moves.append
        perception = self._perception
        pos_to_idx = self._pos_to_idx

        for neighbour in neighbours:
            i = pos_to_idx.get((neighbour.x, neighbour.y))
            if i is None:
                continue
            if perception.terrains[i] in terrain_ids:
                append(Position(self._perception.xs[i], self._perception.ys[i]))

        return possible_moves



    def detect_closest_alive_animal(self) -> Optional[TargetInfo]:
        animals_indexes = self.get_animals_indexes()
        perception = self._perception
        min_distance = 2 * self._range
        x, y = self._transform.position.x, self._transform.position.y
        current = -1
        for i in animals_indexes:
            if perception.organisms_alive[i] == 0:
                continue
            d = abs(perception.xs[i] - x) + abs(perception.ys[i] - y)
            if d < min_distance:
                min_distance = d
                current = i
        if current == -1:
            return None

        position = Position(perception.xs[current], perception.ys[current])
        id = perception.organisms_id[current]
        organism_kind = self._id_registry.decode_object(perception.organisms[current])
        is_alive = bool(perception.organisms_alive[current])
        return TargetInfo(OrganismID(organism_kind, id),position, (perception.offsets_x[current], perception.offsets_y[current]), is_alive)



    def get_animals_indexes(self):
        perception = self._perception
        indexes = []
        append = indexes.append
        get_organism_group = self._id_registry.get_organism_group_from_id
        for i in range(len(perception.xs)):
            if perception.organisms_id[i] == 0:
                continue
            group_name = get_organism_group(perception.organisms[i])
            if group_name == "animal":
               append(i)

        return indexes




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










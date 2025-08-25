from dataclasses import dataclass

from infrastructure.rendering.soa.organism_soa import OrganismSoA
from infrastructure.rendering.soa.tile_soa import TileSoA


@dataclass(frozen=True, slots=True)
class WorldFrameSnapshot:
    tick_id: int
    time: float
    tiles: TileSoA
    organisms: OrganismSoA
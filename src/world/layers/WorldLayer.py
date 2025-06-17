from dataclasses import dataclass
from typing import Literal
import numpy as np


@dataclass
class WorldLayer:
    name: Literal["Height", "Temperature", "Moisture"]
    cmap: str
    label: str
    values: np.ndarray

    @staticmethod
    def from_type(name: Literal["Height", "Temperature", "Moisture"], values: np.ndarray) -> "WorldLayer":
        presets = {
            "Height": {"cmap": "terrain", "label": "Elevation"},
            "Temperature": {"cmap": "coolwarm", "label": "Temperature (°C)"},
            "Moisture": {"cmap": "Blues", "label": "Moisture (%)"},
        }

        if name not in presets:
            raise ValueError(f"Unknown layer name: {name}")

        return WorldLayer(
            name=name,
            cmap=presets[name]["cmap"],
            label=presets[name]["label"],
            values=values
        )

from dataclasses import dataclass
from typing import Literal, Optional, Callable, Tuple
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Colormap, Normalize

from tools.Utils import terrain_colormap_with_water


@dataclass
class WorldLayer:
    name: Literal["Height", "Temperature", "Moisture"]
    cmap: str
    label: str
    values: np.ndarray
    original_range: tuple[float, float] = (0.0, 1.0)
    colormap_fn: Optional[Callable[[], Tuple[Colormap, Optional[Normalize]]]] = None

    def denormalized(self) -> np.ndarray:
        min_val, max_val = self.original_range
        return self.values * (max_val - min_val) + min_val

    def get_colormap_and_norm(self) -> Tuple[Colormap, Optional[Normalize]]:
        if self.colormap_fn:
            return self.colormap_fn()
        return plt.get_cmap(self.cmap), None

    @staticmethod
    def from_type(name: Literal["Height", "Temperature", "Moisture"], values: np.ndarray) -> "WorldLayer":
        presets = {
            "Height": {
                "cmap": "terrain",
                "label": "Elevation (m)",
                "range": (-3000, 9000),
                "colormap_fn": terrain_colormap_with_water
            },
            "Temperature": {
                "cmap": "coolwarm",
                "label": "Temperature (°C)",
                "range": (-30, 55),
                "colormap_fn": None
            },
            "Moisture": {
                "cmap": "Blues",
                "label": "Moisture (%)",
                "range": (0, 100),
                "colormap_fn": None
            },
        }

        if name not in presets:
            raise ValueError(f"Unknown layer name: {name}")

        config = presets[name]
        return WorldLayer(
            name=name,
            cmap=config["cmap"],
            label=config["label"],
            values=values,
            original_range=config["range"],
            colormap_fn=config["colormap_fn"]
        )
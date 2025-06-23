import numpy as np

from view.presentation.layers.world_layer import WorldLayer


def create_terrain_layer(values: np.ndarray):
    return WorldLayer.from_type("Height", values)

def create_temperature_layer(values: np.ndarray):
    return WorldLayer.from_type("Temperature", values)

def create_moisture_layer(values: np.ndarray):
    return WorldLayer.from_type("Moisture", values)
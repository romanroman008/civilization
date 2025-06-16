import numpy as np

from tools.logger import get_logger
from world.Visualisation import show_layer

from world.WorldGenerator import  WorldGenerator
from world.WorldLayer import WorldLayer


def main():
    logger = get_logger("civilization.world", level="DEBUG")
    worldGenerator = WorldGenerator(logger)
    world = worldGenerator.generate_map(200,200)

    terrain = create_terrain_layer(world[:,:,0])
    temperature = create_temperature_layer(world[:,:1])
    moisture = create_moisture_layer(world[:,:,2])

    show_layer(terrain)
    show_layer(temperature)
    show_layer(moisture)






def create_terrain_layer(values: np.ndarray):
    return WorldLayer.from_type("Height", values)

def create_temperature_layer(values: np.ndarray):
    return WorldLayer.from_type("Temperature", values)

def create_moisture_layer(values: np.ndarray):
    return WorldLayer.from_type("Moisture", values)



if __name__ == "__main__":
    main()

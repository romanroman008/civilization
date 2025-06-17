import numpy as np

from tools.logger import get_logger
from tools.paths import get_data_path
from world.Visualisation import show_layer, visualize_biome_map

from world.WorldGenerator import  WorldGenerator
from world.biome.Biome import Biome
from world.biome.BiomeClassifier import BiomeClassifier
from world.layers.WorldLayer import WorldLayer


def main():
    logger = get_logger("civilization.world", level="DEBUG")


    biome_list = Biome.load_from_json(get_data_path("biomes.json"))
    biome_classifier = BiomeClassifier(biome_list)
    worldGenerator = WorldGenerator(logger, biome_classifier)
    world,biome_map = worldGenerator.generate_map(200,200)

    terrain = create_terrain_layer(world[:,:,0])
    temperature = create_temperature_layer(world[:,:,1])
    moisture = create_moisture_layer(world[:,:,2])



    show_layer(terrain)
    show_layer(temperature)
    show_layer(moisture)

    visualize_biome_map(biome_map,biome_list)








def create_terrain_layer(values: np.ndarray):
    return WorldLayer.from_type("Height", values)

def create_temperature_layer(values: np.ndarray):
    return WorldLayer.from_type("Temperature", values)

def create_moisture_layer(values: np.ndarray):
    return WorldLayer.from_type("Moisture", values)



if __name__ == "__main__":
    main()

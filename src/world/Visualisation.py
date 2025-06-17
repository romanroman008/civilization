import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

from world.layers.WorldLayer import WorldLayer


def show_layer(layer:WorldLayer):
    plt.imshow(layer.values, cmap=layer.cmap)
    plt.colorbar(label=layer.label)
    plt.title(layer.name)
    plt.show()


def visualize_biome_map(biome_map, biome_list):
    height, width = biome_map.shape
    image = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            biome = biome_map[y][x]
            image[y, x] = biome.color if biome else (255, 255, 255)  # fallback: biały


    unique_biomes = {b.id: b for b in biome_list}
    legend_elements = [
        Patch(facecolor=np.array(b.color) / 255, edgecolor='black', label=b.name)
        for b in unique_biomes.values()
    ]

    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.title("Biome Map")
    plt.axis("off")


    plt.legend(
        handles=legend_elements,
        loc='upper left',
        bbox_to_anchor=(1.05, 1),
        borderaxespad=0.,
        fontsize='small'
    )

    plt.tight_layout()
    plt.show()

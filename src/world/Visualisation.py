import matplotlib.pyplot as plt
import numpy as np

from world.WorldLayer import WorldLayer


def show_layer(layer:WorldLayer):
    plt.imshow(layer.values, cmap=layer.cmap)
    plt.colorbar(label=layer.label)
    plt.title(layer.name)
    plt.show()

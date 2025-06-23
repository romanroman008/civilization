import matplotlib.pyplot as plt

from view.presentation.layers.world_layer import WorldLayer


def show_layer(layer: WorldLayer):
    cmap, norm = layer.get_colormap_and_norm()
    plt.imshow(layer.denormalized(), cmap=cmap, norm=norm)
    plt.colorbar(label=layer.label)
    plt.title(layer.name)
    plt.axis("off")
    plt.show()



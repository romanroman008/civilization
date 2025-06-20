def normalize(value: float, min_val: float, max_val: float) -> float:
    if max_val - min_val == 0:
        return 0.0
    return (value - min_val) / (max_val - min_val)


def normalize_layered_noise(value: float, amplitude_sum: float) -> float:
    avg = value / amplitude_sum
    return (avg + 1) / 2


def terrain_colormap_with_water():
    from matplotlib.colors import ListedColormap, BoundaryNorm
    boundaries = [0, 16, 32, 48, 64, 80, 100]
    colors = [
        "#3b83bd",  # woda
        "#355e3b",  # ciemna zieleń (niziny)
        "#4CAF50",  # średnia zieleń
        "#8BC34A",  # jasna zieleń
        "#f4e19c",  # żółty
        "#8B8C7A"  # pomarańcz
    ]
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(boundaries, len(colors))
    return cmap, norm

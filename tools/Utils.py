

def normalize(value: float, min_val: float, max_val: float) -> float:
    if max_val - min_val == 0:
        return 0.0
    return (value - min_val) / (max_val - min_val)


def normalize_layered_noise(value: float, amplitude_sum: float) -> float:
    avg = value / amplitude_sum
    return (avg + 1) / 2

def terrain_colormap_with_water():
    from matplotlib.colors import ListedColormap, BoundaryNorm
    boundaries = [-11000, -5000, -2000, 0, 500, 1000, 2000, 4000, 9000]
    colors = [
        "#08306b", "#2171b5", "#6baed6",  # woda
         "#00441b",  # ciemna zieleń (niziny)
        "#238b45",  # średnia zieleń
        "#78c679",  # jasna zieleń
        "#fed976",  # żółty
        "#fd8d3c",  # pomarańcz
        "#e31a1c"   # czerwony (szczyty)
    ]
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(boundaries, len(colors))
    return cmap, norm


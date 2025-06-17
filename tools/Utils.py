

def normalize(value: float, min_val: float, max_val: float) -> float:
    if max_val - min_val == 0:
        return 0.0
    return (value - min_val) / (max_val - min_val)


def normalize_layered_noise(value: float, amplitude_sum: float) -> float:
    avg = value / amplitude_sum
    return (avg + 1) / 2



from domain.components.direction import Direction
from domain.components.position import Position


def quantize_to_set(value, allowed_values):
    return min(allowed_values, key=lambda x: abs(x - value))

def find_divisors(n: int) -> list[int]:
    if n <= 0:
        raise ValueError("Value has to be positive integer")
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sorted(divisors)

def find_needed_offset(organism) -> tuple[float,float]:
    offset_x = organism.target_position.x - organism.relative_position.x
    offset_y = organism.target_position.y - organism.relative_position.y
    return offset_x, offset_y

def find_target_position(actual:Position, direction: Direction, distance: int = 1):
    return actual + direction.vector() * distance



def find_shortest_rotation(current: Direction, desired: Direction) -> int:
    current_angle = current.angle
    desired_angle = desired.angle

    rotation = desired_angle - current_angle

    if rotation > 180:
        rotation -= 360
    elif rotation < -180:
        rotation += 360


    return rotation

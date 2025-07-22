import pytest
from unittest.mock import MagicMock


from domain.world.entieties.direction import Direction
from domain.world.entieties.position import Position
from domain.world.services.movement.movement_interpolation import _find_needed_rotation, _find_needed_offset, \
    MovementInterpolation


@pytest.fixture
def mock_organism():
    organism = MagicMock()
    organism.position = Position(0, 0)
    organism.target_position = Position(1, 0)
    organism.rotation = 0.0
    organism.offset = (0.0, 0.0)
    return organism


def test_find_needed_rotation_left(mock_organism):
    mock_organism.target_position = Position(-1, 0)
    mock_organism.position = Position(0, 0)
    mock_organism.rotation = 0.0

    assert _find_needed_rotation(mock_organism) == 90.0


def test_find_needed_offset_returns_correct_vector():
    class FakeOrganism:
        position = Position(1, 1)
        target_position = Position(3, 4)

    offset_x, offset_y = _find_needed_offset(FakeOrganism())
    assert offset_x == 2
    assert offset_y == 3


def test_rotation_applied_when_not_facing_target(mock_organism):
    movement = MovementInterpolation([mock_organism])
    movement.rotation_speed = 1

    mock_organism.target_position = Position(-1, 0)
    mock_organism.position = Position(0, 0)
    mock_organism.rotation = 0.0
    mock_organism.offset = (0.0, 0.0)

    movement(tick_numbers=1)

    assert mock_organism.rotate.called


def test_movement_applied_when_facing_target(mock_organism):
    movement = MovementInterpolation([mock_organism])
    movement.rotation_speed = 1
    movement.movement_speed = 1

    mock_organism.target_position = Position(1, 0)
    mock_organism.position = Position(0, 0)
    mock_organism.rotation = 270.0  # facing right
    mock_organism.offset = (0.0, 0.0)

    movement(tick_numbers=1)

    assert mock_organism.move_offset_x.called


def test_no_action_when_position_equals_target(mock_organism):
    movement = MovementInterpolation([mock_organism])

    mock_organism.position = Position(1, 1)
    mock_organism.target_position = Position(1, 1)

    movement()

    mock_organism.rotate.assert_not_called()
    mock_organism.move_offset_x.assert_not_called()
    mock_organism.reset_offset.assert_not_called()
    mock_organism.reset_rotation.assert_not_called()


def test_resets_when_target_reached(mock_organism):
    movement = MovementInterpolation([mock_organism])
    movement.rotation_speed = 1
    movement.movement_speed = 1

    # Setup: rotation is correct, offset już przesunięty
    mock_organism.rotation = 270.0
    mock_organism.offset = (1.0, 0.0)
    mock_organism.position = Position(0, 0)
    mock_organism.target_position = Position(1, 0)

    movement(tick_numbers=1)

    # Sprawdzenie resetu
    assert mock_organism.reset_offset.called
    assert mock_organism.reset_rotation.called
    assert mock_organism.position == mock_organism.target_position

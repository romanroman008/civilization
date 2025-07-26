from dataclasses import dataclass

from shared.utils import clamp


@dataclass
class Vitals:
    _hunger: float = 1.0
    _fatigue: float = 1.0
    _health: float = 1.0

    HUNGER_DECAY_PER_CALL = 0.001
    HUNGER_INCREASE_PER_EAT = 0.01

    FATIGUE_RECOVERY_PER_REST: float = 0.01
    FATIGUE_INCREASE_PER_EFFORT: float = 0.01

    def get_hungry(self, amount: float = HUNGER_DECAY_PER_CALL):
        return self._hunger * amount

    def eat(self, amount: float = HUNGER_INCREASE_PER_EAT):
        self._hunger = max(0.0, self._hunger + amount)

    def make_effort(self, amount: float = FATIGUE_INCREASE_PER_EFFORT):
        self._fatigue = clamp(self._fatigue + amount, 0.0, 1.0)

    def rest(self, amount: float = FATIGUE_RECOVERY_PER_REST):
        self._fatigue = clamp(self._fatigue - amount, 0.0, 1.0)

    @property
    def hunger(self):
        return self._hunger

    @property
    def health(self):
        return self._health

    @property
    def fatigue(self):
        return self._fatigue

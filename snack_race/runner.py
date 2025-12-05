from .dice import Dice
from .constants import GOAL
import numpy as np


class Runner:
    def __init__(self,
                 name: str,
                 dice: Dice | list[int] | None = None):
        self.name = name
        self._random = np.random.random()
        self.goaled_time = None

        if isinstance(dice, Dice):
            self.dice = dice
        elif dice is None:
            self.dice = Dice()
        else:
            self.dice = Dice(dice)
        self.history = [0]

    def reset(self):
        self.history = [0]
        self.goaled_time = None
        self._random = np.random.random()

    def step(self):
        if self.is_finished:
            self.history.append(GOAL)
            return None
        else:
            x = self.history[-1]
            step_size = self.dice.roll()
            x_new = x + step_size
            x_new = max(0, x_new)
            x_new = min(GOAL, x_new)
            if x_new >= GOAL:
                self.goaled_time = len(self.history)
            self.history.append(x_new)

    def __repr__(self):
        return f"Runner({self.name})\t {self.dice}"

    @property
    def is_finished(self):
        return max(self.history) >= GOAL

    def __lt__(self, other):
        self_key = self.goaled_time, self._random
        other_key = other.goaled_time, self._random
        return (self_key <= other_key)

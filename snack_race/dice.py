import numpy as np
from itertools import pairwise

STANDARD_DICE_EYES = (1, 2, 3, 4, 5, 6)
NUM_EYES = len(STANDARD_DICE_EYES)
SUM_EYES = sum(STANDARD_DICE_EYES)

def make_random_eyes():
    sampled = np.random.choice(range(NUM_EYES + SUM_EYES - 1),
                               size=NUM_EYES - 1,
                               replace=False)
    sampled = [-1, *sorted(sampled), NUM_EYES + SUM_EYES - 1]
    eyes = [p2 - p1 - 1 for p1, p2 in pairwise(sampled)]
    return eyes


class Dice:
    def __init__(self, eyes: list[int] = None):
        if eyes is None:
            eyes = make_random_eyes()
        self.eyes = eyes
        self.validate()

    def __repr__(self):
        return f'Dice{tuple(map(int, self.eyes))}'

    def validate(self):
        assert len(self.eyes) == NUM_EYES
        assert sum(self.eyes) == SUM_EYES

    def roll(self) -> int:
        return np.random.choice(self.eyes)

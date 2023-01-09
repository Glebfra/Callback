import numpy as np


class Pacemaker:
    def __init__(self, x, y, init_phase, time):
        self.x = x
        self.y = y
        self.time = time
        self.phase = init_phase

    def next_step(self):
        self.phase = self.phase + 1 if self.phase <= self.time - 1 else 0

    def __str__(self):
        return {'x': self.x, 'y': self.y, 'time': self.time, 'init_phase': self.phase}

import numpy as np


class State(object):
    def __init__(self, height: int = 200, width: int = 200, excitation_time: float = None,
                 refractory_time: float = None, critical_value: float = None, activator_remain: float = None):
        self.width, self.height = width, height
        self.states = np.zeros((width, height))
        self.__old_states = self.states
        self.activator_concentration = np.zeros((width, height))
        self.activator_production = np.zeros((width, height))
        self.excitation_time = excitation_time
        self.refractory_time = refractory_time
        self.critical_value = critical_value
        self.activator_remain = activator_remain

    def reshape_states(self, height, width):
        self.height = height
        self.width = width
        self.states.reshape((width, height))

    def next_step(self):
        for row, cols in enumerate(self.states):
            for col, value in enumerate(cols):
                if 0 < self.states[row, col] < self.refractory_time + self.excitation_time:
                    self.states[row, col] += 1
                elif self.states[row, col] == self.excitation_time + self.refractory_time:
                    self.states[row, col] = 0
                elif self.states[row, col] == 0 and self.activator_concentration[row, col] < self.critical_value:
                    self.states[row, col] = 0
                elif self.states[row, col] == 0 and self.activator_concentration[row, col] >= self.critical_value:
                    self.states[row, col] = 1
        yield self.states


if __name__ == '__main__':
    pass

import numpy as np


class State(object):
    def __init__(self, height, width, excitation_time, refractory_time, critical_value, activator_remain):
        self.width, self.height = width, height
        self._states = np.zeros((width, height))
        self.__old_states = self._states
        self.activator_concentration = np.zeros((width, height))
        self.activator_production = np.zeros((width, height))
        self.excitation_time = excitation_time
        self.refractory_time = refractory_time
        self.critical_value = critical_value
        self.activator_remain = activator_remain

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, height=None, width=None):
        self.height = height if height is not None else self.height
        self.width = width if width is not None else self.width
        self._states = self._states.reshape((self.width, self.height))

    def next_step(self):
        for row, cols in enumerate(self._states):
            for col, value in enumerate(cols):
                if 0 < self._states[row, col] < self.refractory_time + self.excitation_time:
                    self._states[row, col] += 1
                elif self._states[row, col] == self.excitation_time + self.refractory_time:
                    self._states[row, col] = 0
                elif self._states[row, col] == 0 and self.activator_concentration[row, col] < self.critical_value:
                    self._states[row, col] = 0
                elif self._states[row, col] == 0 and self.activator_concentration[row, col] >= self.critical_value:
                    self._states[row, col] = 1
        yield self._states

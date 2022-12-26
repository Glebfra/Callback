import numpy as np
import numba
import matplotlib.pyplot as plt


class State(object):
    def __init__(self, height: int = 200, width: int = 200, excitation_time: float = 0.4,
                 refractory_time: float = 0.2, critical_value: float = 2, activator_remain: float = 0.5):
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
        self.activator_production.reshape((width, height))
        self.activator_concentration.reshape((width, height))

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

                if 0 < self.states[row, col] < self.excitation_time:
                    self.activator_production[row, col] = 1
                elif self.excitation_time < self.states[row, col] < self.excitation_time + self.refractory_time or self.states[row, col] == 0:
                    self.activator_production[row, col] = 0

                self.activator_concentration[row, col] += self.activator_production[row-1:row+2, col-1:col+2].sum()
        return self.states


if __name__ == '__main__':
    state = State(height=10, width=10)
    state.states[0, 0] = 1
    plt.figure(1)
    plt.ion()

    for states in range(10):
        plt.imshow(state.states)
        plt.draw()
        plt.pause(0.0001)
        plt.clf()
        state.states[states, 1] = 2

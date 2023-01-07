import json
import typing

import numpy as np

import matplotlib.pyplot as plt


class State(object):
    def __init__(self, height: int = 30, width: int = 27, excitation_time: float = 3, refractory_time: float = 5,
                 critical_value: float = 2.50, activator_remain: float = 0.55, states: typing.Iterable = None,
                 pacemakers: typing.Iterable = None) -> None:
        """
        This class contains the arrays
        :param height: The number of rows in arrays
        :param width: The number of columns in arrays
        :param excitation_time: Excitation time
        :param refractory_time: Refactory time
        :param critical_value: Critical value
        :param activator_remain: Activator remain
        :param states: States array
        """
        self.width, self.height = width, height
        self._states = np.zeros((width, height)) if states is None else np.array(states)
        self.pacemakers = np.zeros((width, height)) if pacemakers is None else np.array(pacemakers)
        self.activator_concentration = np.zeros((width, height))
        self.activator_production = np.zeros((width, height))
        self.excitation_time = excitation_time
        self.refractory_time = refractory_time
        self.critical_value = critical_value
        self.activator_remain = activator_remain

    @classmethod
    def create_state_from_file(cls, filepath):
        with open(filepath, 'r') as file:
            properties = json.load(file)
        return cls(**properties)

    @property
    def states(self):
        states_array = self._states.copy()
        for row in range(self.width):
            for col in range(self.height):
                if 0 < states_array[row, col] <= self.excitation_time:
                    states_array[row, col] = 1
                elif self.excitation_time < states_array[row, col] <= self.excitation_time + self.refractory_time:
                    states_array[row, col] = 2
        return states_array

    @states.setter
    def states(self, states):
        self._states = states

    def save_state_to_file(self, filepath):
        properties = {
            'height': self.height,
            'width': self.width,
            'refractory_time': self.refractory_time,
            'excitation_time': self.excitation_time,
            'activator_remain': self.activator_remain,
            'critical_value': self.critical_value,
            'states': self._states.tolist()
        }
        with open(filepath, 'w') as file:
            json.dump(properties, file)

    def create_pacemaker(self):
        pass

    def reshape_states(self, height, width):
        # TODO make this method workable
        self.height = height
        self.width = width
        self._states.reshape((width, height))
        self.activator_production.reshape((width, height))
        self.activator_concentration.reshape((width, height))

    def next_step(self):
        """
        This method calculate the next_step's states
        :return: states
        """
        for row in range(self.width):
            for col in range(self.height):

                if 0 < self._states[row, col] <= self.excitation_time:
                    self.activator_production[row, col] = 1
                elif self.excitation_time < self._states[row, col] <= self.excitation_time + self.refractory_time or \
                        self._states[row, col] == 0:
                    self.activator_production[row, col] = 0

                self.activator_concentration[row, col] *= self.activator_remain
                self.activator_concentration[row, col] += self.activator_production[
                                                         row - 1 if row - 1 >= 0 else 0:row + 2,
                                                         col - 1 if col - 1 >= 0 else 0:col + 2
                                                         ].sum()

                if 0 < self._states[row, col] < self.excitation_time + self.refractory_time:
                    self._states[row, col] += 1
                elif self._states[row, col] == self.excitation_time + self.refractory_time:
                    self._states[row, col] = 0
                elif self._states[row, col] == 0 and self.activator_concentration[row, col] < self.critical_value:
                    self._states[row, col] = 0
                elif self._states[row, col] == 0 and self.activator_concentration[row, col] >= self.critical_value:
                    self._states[row, col] = 1

        return self._states


if __name__ == '__main__':
    state = State.create_state_from_file('config/state3.json')
    plt.figure(1)
    plt.imshow(state.states)
    plt.ion()
    while True:
        plt.imshow(state.states)
        plt.draw()
        plt.pause(0.0001)
        plt.clf()
        state.next_step()

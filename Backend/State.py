import json
import typing

import numpy as np
import numba

import matplotlib.pyplot as plt


class State(object):
    def __init__(self, height: int = 30, width: int = 27, excitation_time: int = 3, refractory_time: int = 5,
                 critical_value: float = 3, activator_remain: float = 0.3, states: typing.Iterable = None,
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

    def resize_states(self, width, height):
        self.width, self.height = width, height

        old_states: np.ndarray = self._states.copy()
        old_activator_production: np.ndarray = self.activator_production.copy()
        old_activator_concentration: np.ndarray = self.activator_concentration.copy()

        new_states: np.ndarray = np.zeros((width, height))
        new_activator_production: np.ndarray = np.zeros((width, height))
        new_activator_concentration: np.ndarray = np.zeros((width, height))

        for row in range(old_states.shape[0]):
            if row >= new_states.shape[0]:
                break
            for col in range(old_states.shape[1]):
                if col >= new_states.shape[1]:
                    break
                new_states[row, col] = old_states[row, col]
                new_activator_production[row, col] = old_activator_production[row, col]
                new_activator_concentration[row, col] = old_activator_concentration[row, col]

        self._states = new_states
        self.activator_production = new_activator_production
        self.activator_concentration = new_activator_concentration

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

    @staticmethod
    @numba.njit
    def __next_step(states: np.ndarray, activator_production: np.ndarray, activator_concentration: np.ndarray,
                    width: int, height: int, excitation_time: float, refractory_time: float, activator_remain: float,
                    critical_value: float):
        for row in range(width):
            for col in range(height):

                if 0 < states[row, col] <= excitation_time:
                    activator_production[row, col] = 1
                elif excitation_time < states[row, col] <= excitation_time + refractory_time or \
                        states[row, col] == 0:
                    activator_production[row, col] = 0

                activator_concentration[row, col] *= activator_remain
                activator_concentration[row, col] += activator_production[
                                                     row - 1 if row - 1 >= 0 else 0:row + 2,
                                                     col - 1 if col - 1 >= 0 else 0:col + 2
                                                     ].sum()

                if 0 < states[row, col] < excitation_time + refractory_time:
                    states[row, col] += 1
                elif states[row, col] == excitation_time + refractory_time:
                    states[row, col] = 0
                elif states[row, col] == 0 and activator_concentration[row, col] < critical_value:
                    states[row, col] = 0
                elif states[row, col] == 0 and activator_concentration[row, col] >= critical_value:
                    states[row, col] = 1

        return states, activator_concentration, activator_production

    def next_step(self):
        """
        This method calculate the next_step's states
        :return: states
        """
        self._states, self.activator_concentration, self.activator_production = self.__next_step(self._states,
                                                                                                 self.activator_production,
                                                                                                 self.activator_concentration,
                                                                                                 self.width,
                                                                                                 self.height,
                                                                                                 self.excitation_time,
                                                                                                 self.refractory_time,
                                                                                                 self.activator_remain,
                                                                                                 self.critical_value)

        return self._states


if __name__ == '__main__':
    state = State.create_state_from_file('config/state3.json')
    state.resize_states(30, 30)
    plt.figure(1)
    plt.imshow(state.states)
    plt.ion()
    while True:
        plt.imshow(state.states)
        plt.draw()
        plt.pause(0.0001)
        plt.clf()
        state.next_step()

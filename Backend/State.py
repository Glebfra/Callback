import json
import typing

import numpy as np
import numba

import matplotlib.pyplot as plt

from Pacemaker import Pacemaker


class State(object):
    def __init__(self, height: int = 30, width: int = 27, excitation_time: int = 3, refractory_time: int = 5,
                 critical_value: float = 3, activator_remain: float = 0.3, states: typing.Iterable = None,
                 pacemakers: list = []) -> None:
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
        self.activator_concentration = np.zeros((width, height))
        self.activator_production = np.zeros((width, height))
        self.excitation_time = excitation_time
        self.refractory_time = refractory_time
        self.critical_value = critical_value
        self.activator_remain = activator_remain
        self.pacemakers = pacemakers

    @classmethod
    def create_state_from_file(cls, filepath):
        with open(filepath, 'r') as file:
            properties = json.load(file)
        if 'pacemakers' in properties.keys():
            pacemakers = properties['pacemakers']
            properties['pacemakers'] = []
            for pacemaker in pacemakers:
                properties['pacemakers'].append(Pacemaker(**pacemaker))

        return cls(**properties)

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

    @property
    def states(self):
        states_array = self._states.copy()
        states_array[np.where(np.logical_and(states_array <= self.excitation_time, states_array > 0))] = 1
        states_array[np.where(np.logical_and(states_array <= self.excitation_time + self.refractory_time,
                                             states_array > self.excitation_time))] = 2

        return states_array

    @states.setter
    def states(self, states):
        self._states = states

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

    def create_pacemaker(self, x, y, t, init_phase) -> None:
        self.pacemakers.append(Pacemaker(x, y, init_phase, t))

    def next_step(self):
        """
        This method calculate the next_step's states
        :return: states
        """
        self.activator_production[...] = 0
        self.activator_production[np.where(np.logical_and(self._states <= self.excitation_time, self._states > 0))] = 1

        self.activator_concentration *= self.activator_remain
        self.activator_concentration += np.roll(self.activator_production, 1, axis=0) + \
                                        np.roll(self.activator_production, -1, axis=0) + \
                                        np.roll(self.activator_production, 1, axis=1) + \
                                        np.roll(self.activator_production, -1, axis=1)

        self._states[np.where(np.logical_and(self._states > 0, self._states < (self.excitation_time + self.refractory_time)))] += 1
        self._states[np.where(self._states == (self.excitation_time + self.refractory_time))] = 0
        self._states[np.where(np.logical_and(self._states == 0, self.activator_concentration < self.critical_value))] = 0
        self._states[np.where(np.logical_and(self._states == 0, self.activator_concentration >= self.critical_value))] = 1

        for pacemaker in self.pacemakers:
            self._states[pacemaker.y, pacemaker.x] = pacemaker.phase
            pacemaker.next_step()

        return self._states


if __name__ == '__main__':
    state = State.create_state_from_file('config/state3.json')
    plt.figure(1)
    pic = plt.imshow(state.states)
    while True:
        pic.set_data(state.states)
        plt.draw()
        plt.pause(0.001)
        state.next_step()

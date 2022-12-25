import numpy as np


class CurrentState(object):
    def __init__(self, height, width) -> None:
        """
        Class of states
        :param height: The height of conditions matrix
        :param width: The width of conditions matrix
        """
        self.conditions = np.zeros((width, height))

    def next_step(self) -> np.ndarray:
        for row, cols in enumerate(self.conditions):
            for col, value in enumerate(cols):
                self.conditions[row, col] = 1 if value == 1 and (
                        self.conditions[row - 1, col] + self.conditions[1-row, col] == 0
                        or self.conditions[row, col-1] + self.conditions[row, 1-col] == 0
                        or self.conditions[row - 1, col] + self.conditions[1-row, col] == 1
                        or self.conditions[row, col-1] + self.conditions[row, 1-col] == 1
                ) or (value == 0 and self.conditions[row - 1, col] + self.conditions[1-row, col] == 2) else 0
                print(f'row: {row}, col: {col}, value: {value}')
        return self.conditions


if __name__ == '__main__':
    current_state = CurrentState(3, 3)
    current_state.conditions[0, 0] = 1
    # print(current_state.conditions)
    current_state.next_step()

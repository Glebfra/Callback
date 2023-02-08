import matplotlib.pyplot as plt
import numpy as np
import time


class Calculations:
    def __init__(self,
                 number_of_partitions=20,
                 h=3,
                 g=0.4,
                 refraction_time=7,
                 arousal_time=5,
                 background_logic=1,
                 ** kwargs):
        super().__init__(**kwargs)

        # Инициализация параметров системы
        self.number_of_partitions = number_of_partitions  # Количество разбиений вдоль одной оси
        self.h = h  # Пороговое значение концентрации
        self.g = g  # Коэффициент остаточного значений концентрации
        self.refraction_time = refraction_time  # Время рефракции
        self.arousal_time = arousal_time  # Время возбуждения
        self.background_logic = background_logic  # Логическая переменная для выбора фона, 1 - фон Мура, 0 - фон Неймана

        # Инициализация рабочих матриц
        self.matrix_of_states = np.zeros((self.number_of_partitions, self.number_of_partitions))  # Матрица состояний
        self.phase_matrix = np.zeros((self.number_of_partitions, self.number_of_partitions))  # Матрица фаз
        self.production_matrix = np.zeros((self.number_of_partitions, self.number_of_partitions))  # Матр производства
        self.concentration_matrix = np.zeros((self.number_of_partitions, self.number_of_partitions))  # Матр конц
        self.matrix_of_periods = np.zeros((self.number_of_partitions, self.number_of_partitions))  # Матр периодов
        self.time_matrix = np.zeros((self.number_of_partitions, self.number_of_partitions))  # Матр времени

    @staticmethod
    def resizing(matrix, new_n):  # Функция изменения размеров матрицы
        if new_n > np.size(matrix, axis=0):
            z = np.zeros((np.size(matrix, axis=0), new_n - np.size(matrix, axis=0)), dtype=matrix.dtype)
            matrix = np.concatenate((matrix, z), axis=1)
            z = np.zeros((new_n - np.size(matrix, axis=0), new_n), dtype=matrix.dtype)
            matrix = np.concatenate((matrix, z), axis=0)
        elif new_n < np.size(matrix, axis=0):
            matrix = np.delete(matrix, np.s_[new_n:np.size(matrix, axis=0)], axis=0)
            matrix = np.delete(matrix, np.s_[new_n:np.size(matrix, axis=1)], axis=1)
        return matrix

    def changing_the_size_of_matrices(self, new_n):  # Метод изменения размеров всех матриц
        self.matrix_of_states = self.resizing(self.matrix_of_states, new_n)
        self.phase_matrix = self.resizing(self.phase_matrix, new_n)
        self.production_matrix = self.resizing(self.production_matrix, new_n)
        self.concentration_matrix = self.resizing(self.concentration_matrix, new_n)
        self.matrix_of_periods = self.resizing(self.matrix_of_periods, new_n)
        self.time_matrix = self.resizing(self.time_matrix, new_n)
        self.number_of_partitions = new_n

    def calculation_step(self):  # Расчет матриц следующего шага
        # Расчет значений концентрации
        self.production_matrix[...] = 0
        self.production_matrix[np.where(self.matrix_of_states == 1)] = 1  # Выявление производящих клеток

        self.concentration_matrix = self.g * self.concentration_matrix
        self.concentration_matrix += np.roll(self.production_matrix, 1, axis=0) + np.roll(self.production_matrix, -1,
                                                                                          axis=0) + np.roll(
            self.production_matrix, 1, axis=1) + np.roll(self.production_matrix, -1, axis=1) + self.production_matrix

        if self.background_logic:  # Учет области фона Мура
            self.concentration_matrix += np.roll(np.roll(self.production_matrix, 1, axis=0), 1, axis=1) + np.roll(
                np.roll(self.production_matrix, -1, axis=0), 1, axis=1) + np.roll(
                np.roll(self.production_matrix, 1, axis=0), -1, axis=1) + np.roll(
                np.roll(self.production_matrix, -1, axis=0), -1, axis=1)

        # Увеличение фазы и рождение/умерщвление клеток, переходы в новое состояние
        self.phase_matrix[np.where(self.phase_matrix != 0)] += 1  # Увеличение фазы у "старых" клеток
        index = np.where((self.phase_matrix == 0) & (self.concentration_matrix >= self.h))
        self.matrix_of_states[index] = 1  # Рождение новых клеток | Состояния
        self.phase_matrix[index] = 1  # Рождение новых клеток | Фаза
        index = np.where(self.phase_matrix > self.arousal_time + self.refraction_time)
        self.matrix_of_states[index] = 0  # Умерщвление клеток | Состояния
        self.phase_matrix[index] = 0  # Умерщвление клеток | Фаза
        index = np.where(self.phase_matrix >= self.arousal_time + 1)
        self.matrix_of_states[index] = 2  # Переход из состояния возбуждения в состояние рефрактерности
        index = np.where(self.matrix_of_periods != 0)
        self.time_matrix[np.where(self.matrix_of_periods != 0)] += 1  # Увеличение временной компоненты у пейсмейкеров
        index = np.where((self.matrix_of_periods != 0) & (self.time_matrix % self.matrix_of_periods == 0))
        self.matrix_of_states[index] = 0  # Срабатывание периодов у пейсмейкеров 0 | Состояние
        self.phase_matrix[index] = 0  # Срабатывание периодов у пейсмейкеров 0 | Состояние
        index = np.where((self.matrix_of_periods != 0) & (self.time_matrix % self.matrix_of_periods == 1))
        self.matrix_of_states[index] = 1  # Срабатывание периодов у пейсмейкеров 1 | Состояние
        self.phase_matrix[index] = 1  # Срабатывание периодов у пейсмейкеров 1 | Состояние

    def updateCalcs(self):
        self.phase_matrix[np.where(self.matrix_of_states == 1)] = 1
        self.phase_matrix[np.where(self.matrix_of_states == 2)] = self.arousal_time + 1
        self.phase_matrix[np.where(self.matrix_of_states == 0)] = 0
if __name__ =="__main__":
    C = Calculations()
    # Плоская волна
    # C.matrix_of_states[:, 3:5] = 2
    # C.matrix_of_states[:, 5] = 1
    # C.phase_matrix[np.where(C.matrix_of_states == 1)] = 1
    # C.phase_matrix[np.where(C.matrix_of_states == 2)] = C.arousal_time + 1

    # Пейсмейкеры
    # C.changing_the_size_of_matrices(150)
    # C.matrix_of_periods[30:35, 30:35] = 30
    # C.matrix_of_periods[135:140, 135:140] = 10
    # C.background_logic = 1
    #
    # C.phase_matrix[np.where(C.matrix_of_states == 1)] = 1
    # C.phase_matrix[np.where(C.matrix_of_states == 2)] = C.arousal_time + 1

    # Другие пейсмейкеры
    C.background_logic = 1
    C.changing_the_size_of_matrices(150)
    T1 = 40
    C.matrix_of_periods[30:121, 30:33] = T1
    C.matrix_of_periods[30:33, 30:121] = T1
    C.matrix_of_periods[30:121, 120:123] = T1
    C.matrix_of_periods[120:123, 30:121] = T1

    C.matrix_of_periods[70:81, 70:81] = 5

    C.refraction_time = 3
    C.arousal_time = 1
    C.h = 1.5

    # Спираль
    # C.changing_the_size_of_matrices(500)
    # C.background_logic = 1
    # C.matrix_of_states[1:250, 200:260] = 1
    # C.matrix_of_states[1:250, 260:300] = 2
    # C.matrix_of_states[250:510, 200:260] = 2
    # C.matrix_of_states[250:510, 260:300] = 1
    # C.phase_matrix[np.where(C.matrix_of_states == 1)] = 1
    # C.phase_matrix[np.where(C.matrix_of_states == 2)] = C.arousal_time + 1


    # Код для ДЕМО

    plt.figure(1)
    plt.imshow(C.matrix_of_states)

    plt.ion()
    start = time.time()
    N = 500
    for i in range(N):
        plt.imshow(C.matrix_of_states)
        plt.draw()
        plt.pause(0.001)
        plt.clf()
        C.calculation_step()
    print('(sec): ', (time.time() - start) / N)
    plt.ioff()
    plt.imshow(C.matrix_of_states)
    print(C.matrix_of_states)
    plt.show()

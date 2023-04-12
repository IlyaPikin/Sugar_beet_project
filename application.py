import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment
from matrix_generation import get_rand_matrix
from matrix_generation import add_inorganic
from algorithms import greedy_algorithm, lean_algorithm

def run_experiments(n: int, num_exp=10, inorganic=True, output=False):
    # Массивы значений усреднённых целевых функций на каждом этапе переработки
    s_arr_max = np.zeros((n,))       # Оптимальный макс
    s_arr_min = np.zeros((n,))       # Оптимальный мин
    s_arr_greedy = np.zeros((n,))    # Жадный
    s_arr_lean = np.zeros((n,))      # Бережливый

    # Массивы значений усреднённых относительных ошибок
    err_arr_greedy = np.zeros((n,))   # Погрешность жадного
    err_arr_lean = np.zeros((n,))     # Погрешность бережливого

    for series_num in range(num_exp):
        # ___Создание матрицы P___
        p_matrix = get_rand_matrix(n)

        if inorganic:
            p_matrix = add_inorganic(p_matrix)      # учёт связывания сахарозы с неорганикой

        # ___Выполнение алгоритмов___
        # 1. Оптимальный макс
        col_ind_max, row_ind_max = linear_sum_assignment(np.array(p_matrix.T), True)    # Транспонирование для удобства
        s_arr_max[0] = p_matrix[row_ind_max[0]][col_ind_max[0]]/num_exp
        for i in range(1, n):
            value_on_i_stage = p_matrix[row_ind_max[i]][col_ind_max[i]]
            s_arr_max[i] = s_arr_max[i-1] + value_on_i_stage/num_exp    # Деление для усреднения

        # 2. Оптимальный мин
        col_ind_min, row_ind_min = linear_sum_assignment(np.array(p_matrix.T), False)   # Транспонирование для удобства
        s_arr_min[0] = p_matrix[row_ind_min[0]][col_ind_min[0]]/num_exp
        for i in range(1, n):
            value_on_i_stage = p_matrix[row_ind_min[i]][col_ind_min[i]]
            s_arr_min[i] = s_arr_min[i-1] + value_on_i_stage/num_exp    # Деление для усреднения

        # 3. Жадный алгоритм
        row_ind_greedy, col_ind_greedy = greedy_algorithm(p_matrix)
        s_arr_greedy[0] = p_matrix[row_ind_greedy[0]][col_ind_greedy[0]]/num_exp
        for i in range(1, n):
            value_on_i_stage = p_matrix[row_ind_greedy[i]][col_ind_greedy[i]]
            s_arr_greedy[i] = s_arr_greedy[i-1] + value_on_i_stage/num_exp    # Деление для усреднения
        # 4. Бережливый алгоритм
        row_ind_lean, col_ind_lean = lean_algorithm(p_matrix)
        s_arr_lean[0] = p_matrix[row_ind_lean[0]][col_ind_lean[0]] / num_exp
        for i in range(1, n):
            value_on_i_stage = p_matrix[row_ind_lean[i]][col_ind_lean[i]]
            s_arr_lean[i] = s_arr_lean[i - 1] + value_on_i_stage / num_exp  # Деление для усреднения

    fig, ax = plt.subplots()
    ax.plot(s_arr_max, color='red', linestyle='--', marker='o')
    ax.plot(s_arr_min, color='blue', linestyle='--', marker='o')
    ax.plot(s_arr_greedy, color='orange', linestyle='--', marker='o')
    ax.plot(s_arr_lean, color='green', linestyle='--', marker='o')
    plt.show()


def run_application():
    #n = input("Введите размер матрицы:\n")
    #n = int(n)
    n = 10
    run_experiments(n)
    #p = get_rand_matrix(5)
    #p = np.array([[4, 1, 3], [2, 0, 5], [3, 2, 2]])
    #p = add_inorganic(p)
    # p = np.array([
    #     [7, 6, 5.1, 4],
    #     [6, 5.1, 4, 2],
    #     [5, 4, 2, 1],
    #     [4, 2, 1, 0.5]
    # ])
    # print(p)
    # r, c = greedy_algorithm(p)
    # r1, c1 = lean_algorithm(p)
    # c2, r2 = linear_sum_assignment(p.T)
    # print(r, c)
    # print(r1, c1)
    # print(r2, c2)
    # print()
    # print(p.T)

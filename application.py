import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment
from matrix_generation import get_rand_matrix, add_inorganic
from algorithms import greedy_algorithm, thrifty_algorithm

#def calculate():

# Добавить а и б, переменные для алгоритмов, неорганика?
def run_experiments(n: int, num_exp=10, inorganic=True, output=False):
    # Результаты экспериментов
    result = {}

    # Массивы значений усреднённых целевых функций на каждом этапе переработки
    s_arr_max = np.zeros((n,))       # Оптимальный макс
    s_arr_min = np.zeros((n,))       # Оптимальный мин
    s_arr_greedy = np.zeros((n,))    # Жадный
    s_arr_thrifty = np.zeros((n,))   # Бережливый

    # Массивы значений усреднённых относительных ошибок
    err_arr_greedy = np.zeros((n,))   # Погрешность жадного
    err_arr_thrifty = np.zeros((n,))  # Погрешность бережливого

    for series_num in range(num_exp):
        # ___Создание матрицы P___
        p_matrix = get_rand_matrix(n, a_min, a_max, b_min, b_max)

        if inorganic:
            p_matrix = add_inorganic(p_matrix)      # учёт связывания сахарозы с неорганикой

        # ___Выполнение алгоритмов___
        # 1. Оптимальный макс
        col_ind_max, row_ind_max = linear_sum_assignment(np.array(p_matrix.T), True)    # Транспонирование для удобства
        s_arr_max[0] = p_matrix[row_ind_max[0]][col_ind_max[0]]/num_exp
        for i in range(1, n):
            value_on_i_stage = p_matrix[row_ind_max[i]][col_ind_max[i]]
            s_arr_max[i] = s_arr_max[i-1] + value_on_i_stage/num_exp    # Деление для усреднения
        result['Оптимальный макс'] = s_arr_max

        # 2. Оптимальный мин
        if is_venger:
            col_ind_min, row_ind_min = linear_sum_assignment(np.array(p_matrix.T), False)  # Трансп-е для удобства
            s_arr_min[0] = p_matrix[row_ind_min[0]][col_ind_min[0]]/num_exp
            for i in range(1, n):
                value_on_i_stage = p_matrix[row_ind_min[i]][col_ind_min[i]]
                s_arr_min[i] = s_arr_min[i-1] + value_on_i_stage/num_exp    # Деление для усреднения
            result['Оптимальный мин'] = s_arr_min

        # 3. Жадный алгоритм
        if is_greedy:
            row_ind_greedy, col_ind_greedy = greedy_algorithm(p_matrix)
            s_arr_greedy[0] = p_matrix[row_ind_greedy[0]][col_ind_greedy[0]]/num_exp
            err_arr_greedy[0] = abs(s_arr_max[0] - s_arr_greedy[0])/num_exp
            for i in range(1, n):
                value_on_i_stage = p_matrix[row_ind_greedy[i]][col_ind_greedy[i]]
                s_arr_greedy[i] = s_arr_greedy[i-1] + value_on_i_stage/num_exp    # Деление для усреднения
                err_arr_greedy[i] = abs(s_arr_max[i] - s_arr_greedy[i])/num_exp
            result['Жадный алгоритм'] = s_arr_greedy
            result['Погрешность жадного алг'] = err_arr_greedy

        # 4. Бережливый алгоритм
        if is_thrifty:
            row_ind_thrifty, col_ind_thrifty = thrifty_algorithm(p_matrix)
            s_arr_thrifty[0] = p_matrix[row_ind_thrifty[0]][col_ind_thrifty[0]] / num_exp
            err_arr_thrifty[0] = abs(s_arr_thrifty[0] - s_arr_thrifty[0])/num_exp
            for i in range(1, n):
                value_on_i_stage = p_matrix[row_ind_thrifty[i]][col_ind_thrifty[i]]
                s_arr_thrifty[i] = s_arr_thrifty[i - 1] + value_on_i_stage / num_exp  # Деление для усреднения
                err_arr_thrifty[i] = abs(s_arr_thrifty[i] - s_arr_thrifty[i]) / num_exp
            result['Бережливый алгоритм'] = s_arr_greedy
            result['Погрешность бережливого алг'] = err_arr_thrifty

    # Добавить подписи и перенести это в plot()
    # fig, ax = plt.subplots()
    # ax.plot(s_arr_max, color='red', linestyle='--', marker='o')
    # ax.plot(s_arr_min, color='blue', linestyle='--', marker='o')
    # ax.plot(s_arr_greedy, color='orange', linestyle='--', marker='o')
    # ax.plot(s_arr_thrifty, color='green', linestyle='--', marker='o')
    # plt.show()
    return result


def run_application():
    #n = input("Введите размер матрицы:\n")
    #n = int(n)
    n = 100
    run_experiments(n)
    #p = get_rand_matrix(5)
    #p = np.array([[4, 1, 3], [2, 0, 5], [3, 2, 2]])
    #p = add_inorganic(p)
    # p1 = np.array([
    #     [7, 6, 5.1, 4],
    #     [6, 5.1, 4, 2],
    #     [5, 4, 2, 1],
    #     [4, 2, 1, 0.5]
    # ])
    # p3 = np.array([
    #     [4, 2, 0.666666, 0.166666],
    #     [15, 7.5, 2.5, 0.625],
    #     [6, 3, 1, 0.25],
    #     [12, 6, 2, 0.5]
    # ])
    # p = np.array([
    #     [16, 32/3, 64/9, 128/27],
    #     [16, 4, 1, 1/4],
    #     [16, 8, 4, 2],
    #     [16, 16/3, 16/9, 16/27]
    # ])
    # print(p)
    # # r, c = greedy_algorithm(p)
    # # r1, c1 = thrifty_algorithm(p)
    # c2, r2 = linear_sum_assignment(p.T, True)
    # # print(r, c)
    # # print(r1, c1)
    # print(r2, c2)
    # print()
    # print(p.T)

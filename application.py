import numpy as np
from scipy.optimize import linear_sum_assignment
from matrix_generation import get_rand_matrix, add_inorganic
from algorithms import greedy_algorithm, thrifty_algorithm


def run_calculate(p_matrix: np.ndarray, is_venger_max: bool, is_venger_min: bool, is_greedy: bool, is_thrifty: bool):
    n = p_matrix.shape[0]
    target_funcs = {}     # Массивы значений целевых функций
    results = {}          # Индексы элементов матрицы, полученные из алгоримов, и суммы этих элементов

    # Массивы значений целевых функций на каждом этапе переработки
    arr_max = np.zeros((n,))  # Оптимальный макс
    arr_min = np.zeros((n,))  # Оптимальный мин
    arr_greedy = np.zeros((n,))  # Жадный
    arr_thrifty = np.zeros((n,))  # Бережливый

    # ___Выполнение алгоритмов___
    # 1. Оптимальный макс
    if is_venger_max:
        col_ind_max, row_ind_max = linear_sum_assignment(np.array(p_matrix.T), True)  # Транспонирование для удобства
        arr_max[0] = p_matrix[row_ind_max[0]][col_ind_max[0]]
        for i in range(1, n):
            value_on_i_stage = p_matrix[row_ind_max[i]][col_ind_max[i]]
            arr_max[i] = arr_max[i - 1] + value_on_i_stage
        target_funcs['Оптимальный макс'] = arr_max
        results['Индекс столбца (оптимальный макс)'] = col_ind_max
        results['Индекс строки (оптимальный макс)'] = row_ind_max
        results['Сумма (оптимальный макс)'] = p_matrix[col_ind_max, row_ind_max].sum()

    # 2. Оптимальный мин
    if is_venger_min:
        col_ind_min, row_ind_min = linear_sum_assignment(np.array(p_matrix.T), False)  # Трансп-е для удобства
        arr_min[0] = p_matrix[row_ind_min[0]][col_ind_min[0]]
        for i in range(1, n):
            value_on_i_stage = p_matrix[row_ind_min[i]][col_ind_min[i]]
            arr_min[i] = arr_min[i - 1] + value_on_i_stage
        target_funcs['Оптимальный мин'] = arr_min
        results['Индекс столбца (оптимальный мин)'] = col_ind_min
        results['Индекс строки (оптимальный мин)'] = row_ind_min
        results['Сумма (оптимальный мин)'] = p_matrix[col_ind_min, row_ind_min].sum()

    # 3. Жадный алгоритм
    if is_greedy:
        row_ind_greedy, col_ind_greedy = greedy_algorithm(p_matrix)
        arr_greedy[0] = p_matrix[row_ind_greedy[0]][col_ind_greedy[0]]
        for i in range(1, n):
            value_on_i_stage = p_matrix[row_ind_greedy[i]][col_ind_greedy[i]]
            arr_greedy[i] = arr_greedy[i - 1] + value_on_i_stage
        target_funcs['Жадный алгоритм'] = arr_greedy
        results['Индекс столбца (жадный алг)'] = col_ind_greedy
        results['Индекс строки (жадный алг)'] = row_ind_greedy
        results['Сумма (жадный алг)'] = p_matrix[row_ind_greedy, col_ind_greedy].sum()

    # 4. Бережливый алгоритм
    if is_thrifty:
        row_ind_thrifty, col_ind_thrifty = thrifty_algorithm(p_matrix)
        arr_thrifty[0] = p_matrix[row_ind_thrifty[0]][col_ind_thrifty[0]]
        for i in range(1, n):
            value_on_i_stage = p_matrix[row_ind_thrifty[i]][col_ind_thrifty[i]]
            arr_thrifty[i] = arr_thrifty[i - 1] + value_on_i_stage
        target_funcs['Бережливый алгоритм'] = arr_thrifty
        results['Индекс столбца (бережливый алг)'] = col_ind_thrifty
        results['Индекс строки (бережливый алг)'] = row_ind_thrifty
        results['Сумма (бережливый алг)'] = p_matrix[row_ind_thrifty, col_ind_thrifty].sum()

    return target_funcs, results


def run_experiments(n: int, num_exp: int, inorganic: bool,
                    is_venger_max: bool, is_venger_min: bool, is_greedy: bool, is_thrifty: bool,
                    a_min: float, a_max: float, b_min: float, b_max: float
                    ):
    # Результаты экспериментов
    target_funcs = {}
    results = {}

    # Массивы значений усреднённых целевых функций на каждом этапе переработки
    s_arr_max = np.zeros((n,))       # Оптимальный макс
    s_arr_min = np.zeros((n,))       # Оптимальный мин
    s_arr_greedy = np.zeros((n,))    # Жадный
    s_arr_thrifty = np.zeros((n,))   # Бережливый

    for _ in range(num_exp):
        # Локальный массивы целевых функций
        arr_max = np.zeros((n,))        # Оптимальный макс
        arr_min = np.zeros((n,))        # Оптимальный мин
        arr_greedy = np.zeros((n,))     # Жадный
        arr_thrifty = np.zeros((n,))    # Бережливый

        # ___Создание матрицы P___
        p_matrix = get_rand_matrix(n, a_min, a_max, b_min, b_max)

        if inorganic:
            p_matrix = add_inorganic(p_matrix)      # учёт связывания сахарозы с неорганикой

        # ___Выполнение алгоритмов___
        # 1. Оптимальный макс
        col_ind_max, row_ind_max = linear_sum_assignment(np.array(p_matrix.T), True)    # Транспонирование для удобства
        arr_max[0] = p_matrix[row_ind_max[0]][col_ind_max[0]]
        for i in range(1, n):
            value_on_i_stage = p_matrix[row_ind_max[i]][col_ind_max[i]]
            arr_max[i] = arr_max[i-1] + value_on_i_stage
        s_arr_max += arr_max

        # 2. Оптимальный мин
        if is_venger_min:
            col_ind_min, row_ind_min = linear_sum_assignment(np.array(p_matrix.T), False)  # Трансп-е для удобства
            arr_min[0] = p_matrix[row_ind_min[0]][col_ind_min[0]]
            for i in range(1, n):
                value_on_i_stage = p_matrix[row_ind_min[i]][col_ind_min[i]]
                arr_min[i] = arr_min[i-1] + value_on_i_stage
            s_arr_min += arr_min

        # 3. Жадный алгоритм
        if is_greedy:
            row_ind_greedy, col_ind_greedy = greedy_algorithm(p_matrix)
            arr_greedy[0] = p_matrix[row_ind_greedy[0]][col_ind_greedy[0]]
            for i in range(1, n):
                value_on_i_stage = p_matrix[row_ind_greedy[i]][col_ind_greedy[i]]
                arr_greedy[i] = arr_greedy[i-1] + value_on_i_stage
            s_arr_greedy += arr_greedy

        # 4. Бережливый алгоритм
        if is_thrifty:
            row_ind_thrifty, col_ind_thrifty = thrifty_algorithm(p_matrix)
            arr_thrifty[0] = p_matrix[row_ind_thrifty[0]][col_ind_thrifty[0]]
            for i in range(1, n):
                value_on_i_stage = p_matrix[row_ind_thrifty[i]][col_ind_thrifty[i]]
                arr_thrifty[i] = arr_thrifty[i - 1] + value_on_i_stage
            s_arr_thrifty += arr_thrifty

    s_arr_max = s_arr_max / num_exp
    if is_venger_max:
        target_funcs['Оптимальный макс'] = s_arr_max
        results['Оптимальный макс'] = s_arr_max[n-1]
    if is_venger_min:
        s_arr_min = s_arr_min/num_exp
        target_funcs['Оптимальный мин'] = s_arr_min
        results['Оптимальный мин'] = s_arr_min[n-1]
    if is_greedy:
        s_arr_greedy = s_arr_greedy/num_exp
        target_funcs['Жадный алгоритм'] = s_arr_greedy
        results['Жадный алгоритм'] = s_arr_greedy[n-1]
        results['Погрешность жадного алг'] = abs(s_arr_max[n-1] - s_arr_greedy[n-1])/s_arr_max[n-1]
    if is_thrifty:
        s_arr_thrifty = s_arr_thrifty/num_exp
        target_funcs['Бережливый алгоритм'] = s_arr_thrifty
        results['Бережливый алгоритм'] = s_arr_thrifty[n-1]
        results['Погрешность бережливого алг'] = abs(s_arr_max[n-1] - s_arr_thrifty[n-1])/s_arr_max[n-1]

    return target_funcs, results


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

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
        results['Сумма (оптимальный макс)'] = round(p_matrix[row_ind_max, col_ind_max].sum(), 6)

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
        results['Сумма (оптимальный мин)'] = round(p_matrix[row_ind_min, col_ind_min].sum(), 6)

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
        results['Сумма (жадный алг)'] = round(p_matrix[row_ind_greedy, col_ind_greedy].sum(), 6)

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
        results['Сумма (бережливый алг)'] = round(p_matrix[row_ind_thrifty, col_ind_thrifty].sum(), 6)

    return target_funcs, results


def run_experiments(n: int, num_exp: int, inorganic: bool,
                    is_venger_max: bool, is_venger_min: bool, is_greedy: bool, is_thrifty: bool,
                    a_min: float, a_max: float, b_min: float, b_max: float,
                    k_low: float, na_low: float, n_low: float,
                    k_high: float, na_high: float, n_high: float
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

        # Учёт связывания сахарозы с неорганикой
        if inorganic:
            p_matrix = add_inorganic(p_matrix, k_low, na_low, n_low, k_high, na_high, n_high)

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
        results['Оптимальный макс'] = round(s_arr_max[n-1], 6)
    if is_venger_min:
        s_arr_min = s_arr_min/num_exp
        target_funcs['Оптимальный мин'] = s_arr_min
        results['Оптимальный мин'] = round(s_arr_min[n-1], 6)
    if is_greedy:
        s_arr_greedy = s_arr_greedy/num_exp
        target_funcs['Жадный алгоритм'] = s_arr_greedy
        results['Жадный алгоритм'] = round(s_arr_greedy[n-1], 6)
    if is_thrifty:
        s_arr_thrifty = s_arr_thrifty/num_exp
        target_funcs['Бережливый алгоритм'] = s_arr_thrifty
        results['Бережливый алгоритм'] = round(s_arr_thrifty[n-1], 6)
    if is_greedy:
        results['Погрешность жадного алг'] = round(abs(s_arr_max[n-1] - s_arr_greedy[n-1])/s_arr_max[n-1], 6)
    if is_thrifty:
        results['Погрешность бережливого алг'] = round(abs(s_arr_max[n-1] - s_arr_thrifty[n-1])/s_arr_max[n-1], 6)
    return target_funcs, results

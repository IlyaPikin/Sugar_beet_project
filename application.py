import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment


def get_rand_matrix(n: int):
    #rand_matrix = [[1 for j in range(n)] for i in range(n)]
    rand_matrix = [[4, 1, 3], [2, 0, 5], [3, 2, 2]]     # Just for example
    return rand_matrix


def run_experiments(n: int, num_exp=10, add_inorganic=True, output=False):
    # arrays of averaged target functions
    s_arr_max = [0 for i in range(n)]
    s_arr_min = [0 for i in range(n)]
    s_arr_greedy = [0 for i in range(n)]    # Жадный
    s_arr_lean = [0 for i in range(n)]      # Бережливый

    # arrays of average relative errors
    err_arr_greedy = [0 for i in range(n)]  # Погрешность жадного
    err_arr_lean = [0 for i in range(n)]    # Погрешность бережливого

    for series_num in range(num_exp):
        # ___Setting the P matrix values___
        p_matrix = get_rand_matrix(n)

        if (add_inorganic):
            ...             # add z_matrix implementation!

        # ___Computing the algorithms___
        # 1. Optimal max algorithm
        row_ind_max, col_ind_max = linear_sum_assignment(np.array(p_matrix), True)
        s_arr_max[0] = p_matrix[row_ind_max[0]][col_ind_max[0]]
        for i in range(1, n):
            value_on_i_stage = p_matrix[row_ind_max[i]][col_ind_max[i]]
            s_arr_max[i] = s_arr_max[i-1] + value_on_i_stage/num_exp    # division for averaging

        # 2. Optimal min algorithm
        row_ind_min, col_ind_min = linear_sum_assignment(np.array(p_matrix), False)
        s_arr_min[0] = p_matrix[row_ind_min[0]][col_ind_min[0]]
        for i in range(1, n):
            value_on_i_stage = p_matrix[row_ind_min[i]][col_ind_min[i]]
            s_arr_min[i] = s_arr_min[i-1] + value_on_i_stage/num_exp    # division for averaging

        # 3. Greedy algorithm
        ...
        # 4. Lean algorithm
        ...

    fig, ax = plt.subplots()
    ax.plot(s_arr_max, color='red', linestyle='--')
    ax.plot(s_arr_min, color='blue', linestyle='--')
    plt.show()
    input()
    a = 10


def run_application():
    #n = input("Введите размер матрицы:\n")
    #n = int(n)
    n = 3
    run_experiments(n, 1)

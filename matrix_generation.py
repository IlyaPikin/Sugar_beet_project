import numpy as np


# Содержание неорганики K, Na, N (столбцы) в 6 сортах свёклы (строки)
inorganic_in_beet_sorts = np.array([
    [7.05, 0.35, 1.88],
    [4.99, 0.38, 1.91],
    [4.88, 0.31, 2.01],
    [5.35, 0.21, 1.58],
    [7.05, 0.75, 2.8],
    [5.23, 0.82, 2.72]
])


def get_rand_matrix(n: int, a_low: float = 0.14, a_high: float = 0.22, b_low: float = 0., b_high: float = 1.):
    a_column = np.random.uniform(a_low, a_high, (n, 1))
    b_matrix = np.random.uniform(b_low, b_high, (n, n-1))

    zero_addition = np.zeros((n, n-1))
    p_matrix = np.concatenate((a_column, zero_addition), axis=1)

    for i in range(n):
        for j in range(1, n):
            p_matrix[i][j] = p_matrix[i][j-1]*b_matrix[i][j-1]

    return p_matrix


def braunschweig_formula(k: float, na: float, n: float):
    return 0.12 * (k + na) + 0.24 * n + 0.48


def add_inorganic(p_matrix: np.ndarray):
    n = p_matrix.shape[0]
    # k_content = np.random.uniform(4.88, 7.05, (n, 1))
    # na_content = np.random.uniform(0.21, 0.82, (n, 1))
    # n_content = np.random.uniform(1.58, 2.8, (n, 1))

    # Массив с номерами сортов каждой партии свёклы
    sort_numbers = np.random.random_integers(low=0, high=5, size=n)

    for i in range(n):
        k_ = inorganic_in_beet_sorts[sort_numbers[i]][0]
        na_ = inorganic_in_beet_sorts[sort_numbers[i]][1]
        n_ = inorganic_in_beet_sorts[sort_numbers[i]][2]
        inorganic = braunschweig_formula(k_, na_, n_)/100
        for j in range(n):
            p_matrix[i][j] -= inorganic
            if p_matrix[i][j] < 0:
                p_matrix[i][j] = 0

    return p_matrix

import numpy as np


# # Содержание неорганики K, Na, N (столбцы) в 6 сортах свёклы (строки)
# inorganic_in_beet_sorts = np.array([
#     [7.05, 0.35, 1.88],
#     [4.99, 0.38, 1.91],
#     [4.88, 0.31, 2.01],
#     [5.35, 0.21, 1.58],
#     [7.05, 0.75, 2.8],
#     [5.23, 0.82, 2.72]
# ])


def get_rand_matrix(n: int, a_low: float = 0.1893, a_high: float = 0.2252, b_low: float = 0.8, b_high: float = 1.):
    a_column = np.random.uniform(a_low, a_high, (n, 1))
    b_matrix = np.random.uniform(b_low, b_high, (n, n-1))

    zero_addition = np.zeros((n, n-1))
    p_matrix = np.concatenate((a_column, zero_addition), axis=1)

    for i in range(n):
        for j in range(1, n):
            p_matrix[i][j] = p_matrix[i][j-1]*b_matrix[i][j-1]

    for i in range(n):
        for j in range(n):
            p_matrix[i][j] = round(p_matrix[i][j], 6)

    return p_matrix


def braunschweig_formula(k: float, na: float, n: float):
    return 0.12 * (k + na) + 0.24 * n + 0.48


def add_inorganic(p_matrix: np.ndarray, k_low: float, na_low: float, n_low: float,
                  k_high: float, na_high: float, n_high: float):
    n = p_matrix.shape[0]

    k_content = np.random.uniform(k_low, k_high, (n, 1))
    na_content = np.random.uniform(na_low, na_high, (n, 1))
    n_content = np.random.uniform(n_low, n_high, (n, 1))

    inorganic_matrix = np.concatenate((k_content, na_content, n_content),  axis=1)

    for i in range(n):
        k_ = inorganic_matrix[i][0]
        na_ = inorganic_matrix[i][1]
        n_ = inorganic_matrix[i][2]
        inorganic = round(braunschweig_formula(k_, na_, n_)/100, 6)
        for j in range(n):
            p_matrix[i][j] -= inorganic
            if p_matrix[i][j] < 0:
                p_matrix[i][j] = 0

    return p_matrix

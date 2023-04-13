import numpy as np


def greedy_algorithm(p_matrix: np.ndarray):
    n = p_matrix.shape[0]
    row_ind = np.zeros((n,), dtype=int)
    col_ind = np.zeros((n,), dtype=int)

    remained_row_indexes = [int(x) for x in range(n)]

    for j in range(n):
        max_ = p_matrix[remained_row_indexes[0]][j]
        row_ind[j] = remained_row_indexes[0]
        col_ind[j] = j
        for i in remained_row_indexes:
            if p_matrix[i][j] > max_:
                max_ = p_matrix[i][j]
                row_ind[j] = i
        remained_row_indexes.remove(row_ind[j])

    return row_ind, col_ind


def thrifty_algorithm(p_matrix: np.ndarray):
    n = p_matrix.shape[0]
    row_ind = np.zeros((n,), dtype=int)
    col_ind = np.zeros((n,), dtype=int)

    remained_row_indexes = [int(x) for x in range(n)]

    for j in range(n):
        min_ = p_matrix[remained_row_indexes[0]][j]
        row_ind[j] = remained_row_indexes[0]
        col_ind[j] = j
        for i in remained_row_indexes:
            if p_matrix[i][j] < min_:
                min_ = p_matrix[i][j]
                row_ind[j] = i
        remained_row_indexes.remove(row_ind[j])

    return row_ind, col_ind


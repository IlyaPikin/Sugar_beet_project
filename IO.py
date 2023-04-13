import pandas as pd
import numpy as np

def save_res_in_table(results: dict[str, float]):
    #filepath = filedialog.askopenfilename()
    filepath = './Результаты_эксперимента.xlsx'
    df = pd.DataFrame(results)
    df.to_excel(filepath)

def load_matrix_from_file():
    #filepath = filedialog.askopenfilename()
    filepath = './матрица.txt'
    # data = pd.read_excel(filepath, 0)
    # print(data)
    # return data
    with open(filepath, 'r') as f:
        matrix = [[int(num) for num in line.split(',')] for line in f]
    return np.array(matrix)

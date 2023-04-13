import pandas as pd
import numpy as np

def save_res_in_table(results: dict[str, float]):
    filepath = filedialog.askopenfilename()
    df = pd.DataFrame(results)
    df.to_excel(filepath)

def save_matrix_in_file(matrix: np.ndarray):
    # ПОЛУЧИТЬ filepath из функции!
    filepath = './матрица2.xlsx'
    df = pd.DataFrame(matrix)
    df.to_excel(filepath, index=False, header=False)
def load_matrix_from_file():
    filepath = filedialog.askopenfilename()
    df = pd.read_excel(filepath, header=None)
    return np.array(df)

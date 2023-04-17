import random
import re
from tkinter import *
from tkinter import ttk     # подключаем пакет ttk
from tkinter import filedialog
from tkinter import font

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from matrix_generation import *
from application import *
from tkinter.messagebox import showerror, showwarning, showinfo
from fourFn import try_to_get_float

###################### Настройки #############################

width_screen = 1100
height_screen = 680

###################### Создание окна #######################

root = Tk()
root.title("Sugar Beet")
w = root.winfo_screenwidth() # ширина экрана
h = root.winfo_screenheight() # высота экрана
root.geometry(f'{width_screen}x{height_screen}+{(w-1100)//2}+{(h-720)//2}')
root.resizable(width=False, height=False)

################ Создание фреймов ############################

top_frame = ttk.Frame(master=root,
                      width=width_screen,
                      height=90,
                      borderwidth=1,
                      relief=SOLID
                      )

matrix_frame = ttk.Frame(master=root,
                         width=500,
                         height=550,
                         borderwidth=1,
                         relief=SOLID
                         )

result_frame = ttk.Frame(master=root,
                         width=505,
                         height=550,
                         borderwidth=1,
                         relief=SOLID
                         )

top_frame.place(x=0, y=0)

matrix_frame.place(x=20, y=100)
result_frame.place(x=575, y=100)

##################### Переменные состояния ####################

# button_image=PhotoImage(file="button.png")
# button_style = ttk.Style()
# button_style.configure('W.TButton', borderwidth=0, padding=3, relief='flat', background="#ccc", width=1, heigh=1)

right_border_value = [1, 1, 1, 1]

top_font = font.Font(weight="bold", size=12)
medium_font = font.Font(weight="bold", size=10)
cell_font = font.Font(size=13)

n_choice = 5
fields_matrix = []  # В ней хранятся инпут поля гуя
p_matrix = np.array([])  # полноценная матрица
matrix_show_button_onscreen = False
showed_matrix_fields = False
is_generated_by_random = False
is_loaded_from_file = False
neorganic_on = BooleanVar()
target_funcs = {}   # Массивы значений целевых функций на каждом этапе переработки
results = {}        # Основные результаты

a_min = DoubleVar(value=0.1893)
a_max = DoubleVar(value=0.2252)
b_min = DoubleVar(value=0.8)
b_max = DoubleVar(value=1.0)

is_venger_max = BooleanVar(value=False)
is_venger_min = BooleanVar(value=False)
is_greedy = BooleanVar(value=False)
is_thrifty = BooleanVar(value=False)

count_series = IntVar(value=50)

#is_experiment = False
is_calculating = False

err_msg_a_min = StringVar()
err_msg_a_max = StringVar()
err_msg_b_min = StringVar()
err_msg_b_max = StringVar()

plot_to_save = Figure(figsize=(5, 4.5),
                 dpi=100)

###################### Шаблоны функций ########################


def is_valid_a_min(new_val):
    if new_val == "":
        err_msg_a_min.set("Заполните поле!")
        return False
        right_border_value[0] = 0
    try:
        float(new_val)
    except ValueError:
        err_msg_a_min.set("Введите число!")
        right_border_value[0] = 0
        return False
    try:
        float(a_max.get())
    except Exception as e:
        err_msg_a_min.set("Верхняя граница не является числом!")
        right_border_value[0] = 0
        return False
    value = float(new_val)
    if value > a_max.get():
        err_msg_a_min.set("Значение больше верхней границы!")
        right_border_value[0] = 0
        return False
    elif value < 0.0:
        err_msg_a_min.set("Значение меньше 0!")
        right_border_value[0] = 0
        return False
    elif value > 1:
        err_msg_a_min.set("Значение больше 1!")
        right_border_value[0] = 0
        return False
    else:
        err_msg_a_min.set("")
        right_border_value[0] = 1
        return True


def is_valid_a_max(new_val):
    if new_val == "":
        err_msg_a_max.set("Заполните поле!")
        right_border_value[1] = 0
        return False
    try:
        float(new_val)
    except ValueError:
        err_msg_a_max.set("Введите число!")
        right_border_value[1] = 0
        return False
    try:
        float(a_min.get())
    except Exception as e:
        err_msg_a_max.set("Нижняя граница не является числом!")
        right_border_value[1] = 0
        return False
    value = float(new_val)
    if value < a_min.get():
        err_msg_a_max.set("Значение меньше нижней границы!")
        right_border_value[1] = 0
        return False
    elif value < 0.0:
        err_msg_a_max.set("Значение меньше 0!")
        right_border_value[1] = 0
        return False
    elif value > 1:
        err_msg_a_max.set("Значение больше 1!")
        right_border_value[1] = 0
        return False
    else:
        err_msg_a_max.set("")
        right_border_value[1] = 1
        return True


def is_valid_b_min(new_val):
    if new_val == "":
        err_msg_b_min.set("Заполните поле!")
        right_border_value[2] = 0
        return False
    try:
        float(new_val)
    except ValueError:
        err_msg_b_min.set("Введите число!")
        right_border_value[2] = 0
        return False
    try:
        float(b_max.get())
    except Exception as e:
        err_msg_b_min.set("Верхняя граница не является числом!")
        right_border_value[2] = 0
        return False
    value = float(new_val)
    if value > b_max.get():
        err_msg_b_min.set("Значение больше верхней границы!")
        right_border_value[2] = 0
        return False
    elif value < 0.0:
        err_msg_b_min.set("Значение меньше 0!")
        right_border_value[2] = 0
        return False
    elif value > 1:
        err_msg_b_min.set("Значение больше 1!")
        right_border_value[2] = 0
        return False
    else:
        err_msg_b_min.set("")
        right_border_value[2] = 1
        return True


def is_valid_b_max(new_val):
    if new_val == "":
        err_msg_b_max.set("Заполните поле!")
        right_border_value[3] = 0
        return False
    try:
        float(new_val)
    except ValueError:
        err_msg_b_max.set("Введите число!")
        right_border_value[3] = 0
        return False
    try:
        float(b_min.get())
    except Exception as e:
        err_msg_b_max.set("Нижняя граница не является числом!")
        right_border_value[3] = 0
        return False
    value = float(new_val)
    if value < b_min.get():
        err_msg_b_max.set("Значение меньше нижней границы!")
        right_border_value[3] = 0
        return False
    elif value < 0.0:
        err_msg_b_max.set("Значение меньше 0!")
        right_border_value[3] = 0
        return False
    elif value > 1:
        err_msg_b_max.set("Значение больше 1!")
        right_border_value[3] = 0
        return False
    else:
        err_msg_b_max.set("")
        right_border_value[3] = 1
        return True


def is_valid_input_field(new_value):
    pattern = r'^[\d\/\.,]*$'
    # pattern = r'^[\d\/\.,]+$' - если сделать +, то поле нельзя будет оставить пустым. Со зведочкой поле может остаться пустым
    return bool(re.match(pattern, new_value))


check_a_min = (root.register(is_valid_a_min), "%P")
check_a_max = (root.register(is_valid_a_max), "%P")
check_b_min = (root.register(is_valid_b_min), "%P")
check_b_max = (root.register(is_valid_b_max), "%P")
check_field_matr = (root.register(is_valid_input_field), "%P")

def dismiss(window):
    window.grab_release()
    window.destroy()


def load_matrix_from_file():
    global n_choice, p_matrix, fields_matrix, is_loaded_from_file
    filepath = filedialog.askopenfilename(defaultextension=".xlsl", filetypes=[("Excel Files", "*.xlsx")])
    # filepath = './something.xlsx'
    # Попытка считать данные из файла
    if filepath == "":
        return
    try:
        df = pd.read_excel(filepath, header=None, dtype=str)
    except Exception as e:
        open_error_with_bad_file()
        return

    data = np.array(df, dtype=str)
    matrix = np.array([], dtype=float)
    fields_matrix_list = []     # Будущая fields_matrix
    # Проверка данных на корректность и заполнение matrix
    try:
        if df.ndim != 2 or df.shape[0] != df.shape[1]:
            raise Exception('Недопустимые размеры матрицы: матрица должна быть квадратной с размерностью n > 1!')

        matrix = np.resize(matrix, (data.shape[0], data.shape[0]))
        for row_ind in range(data.shape[0]):
            for column_ind in range(data.shape[1]):
                str_value = data[row_ind][column_ind]
                float_value = try_to_get_float(str_value)
                matrix[row_ind][column_ind] = float_value
                fields_matrix_list.append(str_value)     # Записываем строковый value в fields_matrix_list
    except Exception as str_exception:
        open_error(str_exception.args[0])
        return

    is_loaded_from_file = True
    n_choice = data.shape[0]
    p_matrix = matrix
    fields_matrix.clear()
    fields_matrix = [StringVar(value=el) for el in fields_matrix_list]

    rerun_left_frame()
    display_left_screen_down()



def open_error_with_bad_file():
    showerror(title="Ошибка!", message="Данного файла не существует или тип файла не соответствует требуемому типу!")

def open_error(msg: str):
    showerror(title="Ошибка!", message=msg)

def save_matrix_coef():
    if not fields_matrix:
        open_error_with_empty_matr()
        return
    # filepath = './матрица2.xlsx'    # это удалить
    filepath = filedialog.asksaveasfilename(filetypes=[("Excel Files", "*.xlsx")])
    if filepath == "":
        return
    if filepath.find(".xlsx") == -1:
        filepath += ".xlsx"

    df = pd.DataFrame(p_matrix)
    try:
        df.to_excel(filepath, index=False, header=False)
    except Exception as e:
        open_error_with_bad_file()
        return


def save_res_in_graph():
    filepath = filedialog.asksaveasfilename(defaultextension=".jpg",
                                            filetypes=[("JPG Files", "*.jpg"),("PDF Files", "*.pdf"), ("PNG Files", "*.png")])
    plot_to_save.savefig(filepath)


def open_error_with_empty_matr():
    showerror(title="Ошибка!", message="Матрица коэффициентов пуста!")


def open_error_with_gen():
    showerror(title="Ошибка!", message="Ошибка в выборе границ генерации!")


def open_error_with_calc():
    showerror(title="Ошибка!", message="Ошибка ввода данных в матрице!")


def open_error_with_series():
    showerror(title="Ошибка!", message="Ошибка выбора числа серий экспериментов!")


def gen_random_matr():
    global fields_matrix, p_matrix, is_generated_by_random

    if 0 in right_border_value:
        open_error_with_gen()
        return

    is_generated_by_random = True
    fields_matrix.clear()
    p_matrix = get_rand_matrix(n_choice, a_min.get(), a_max.get(), b_min.get(), b_max.get())

    if neorganic_on.get():
        p_matrix = add_inorganic(p_matrix)

    array_1d = p_matrix.flatten()   # Уменьшение размерности до 1
    fields_matrix = [StringVar(value="{0:.5f}".format(el)) for el in array_1d]    # Приведение типов

    rerun_left_frame()
    display_left_screen_down()


def valid_series():
    try:
        int(count_series.get())
    except Exception as e:
        return False
    return True


def start_experiments():
    if not valid_series():
        open_error_with_series()
        return
    global target_funcs, results, is_calculating
    target_funcs, results = run_experiments(n_choice, count_series.get(), neorganic_on.get(),
                              is_venger_max.get(), is_venger_min.get(), is_greedy.get(), is_thrifty.get(),
                              a_min.get(), a_max.get(), b_min.get(), b_max.get()
                              )
    is_calculating = False
    rerun_right_frame()
    display_right_frame(has_data=True, is_experiment=True)


def rerun_left_frame():
    global matrix_frame
    matrix_frame.destroy()
    matrix_frame = ttk.Frame(master=root,
                             width=500,
                             height=550,
                             borderwidth=1,
                             relief=SOLID,
                             )
    matrix_frame.place(x=20, y=100)


def rerun_right_frame():
    global result_frame
    result_frame.destroy()
    result_frame = ttk.Frame(master=root,
                             width=505,
                             height=550,
                             borderwidth=1,
                             relief=SOLID
                             )
    result_frame.place(x=575, y=100)


def calculate():
    global target_funcs, results, p_matrix, fields_matrix, is_calculating
    if not fields_matrix:
        open_error_with_empty_matr()
        return
    matrix = np.zeros((n_choice, n_choice))
    try:
        for i in range(n_choice):
            for j in range(n_choice):
                str_value = fields_matrix[i * n_choice + j].get()
                float_value = try_to_get_float(str_value)
                matrix[i][j] = float_value
    except Exception as str_exception:
        open_error(str_exception.args[0])
        return

    p_matrix = matrix
    target_funcs, results = run_calculate(p_matrix, is_venger_max.get(), is_venger_min.get(),
                                            is_greedy.get(), is_thrifty.get())
    is_calculating = True
    rerun_right_frame()
    display_right_frame(has_data=True, is_experiment=False)

def save_results():
    if not results:
        open_error('Результаты не были получены! Выберете необходимые алгоритмы!')
        return
    filepath = filedialog.asksaveasfilename(filetypes=[("Excel Files", "*.xlsx")])
    if filepath == "":
        return
    if filepath.find(".xlsx") == -1:
        filepath += ".xlsx"
    try:
        if is_calculating:
            df = pd.DataFrame(results)
        else:   # in case it was experiments
            df = pd.DataFrame(results, index=[0])
        df.to_excel(filepath, index=False)
    except Exception as e:
        open_error('Ошибка записи результатов в файл.')
        return


def get_row_matrix(row):
    result = ""
    for i in range(n_choice):
        result += "{0} ".format(fields_matrix[row * n_choice + i].get())
    return result


def show_matrix():
    if not fields_matrix:
        open_error_with_empty_matr()
        return
    window = Toplevel()
    window.title("Матрица")
    window.geometry("400x400")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window))
    for row in range(n_choice):
        label = ttk.Label(master=window, text=get_row_matrix(row))
        label.pack(anchor="nw")


###################################### TOP FRAME ########################################

def display_top_screen():
    ################################ ЛЕВАЯ ЧАСТЬ ##########################################
    global is_venger_max
    global is_venger_min
    global is_greedy
    global is_thrifty

    alg_label = ttk.Label(master=top_frame, text="Алгоритмы решения", font=top_font)
    venger_button_max = ttk.Checkbutton(master=top_frame,
                                        text="Венгерский макс",
                                        variable=is_venger_max)
    venger_button_min = ttk.Checkbutton(master=top_frame,
                                        text="Венгерский мин",
                                        variable=is_venger_min)
    greedy_button = ttk.Checkbutton(master=top_frame,
                                    text="Жадный алгоритм",
                                    variable=is_greedy)
    thrifty_button = ttk.Checkbutton(master=top_frame,
                                     text="Бережливый алгоритм",
                                     variable=is_thrifty)

    alg_label.place(x=130, y=0)
    venger_button_max.place(x=70, y=20)
    greedy_button.place(x=230, y=20)
    venger_button_min.place(x=70, y=50)
    thrifty_button.place(x=230, y=50)

    ############################### ПРАВАЯ ЧАСТЬ #############################################

    modes_alg_label = ttk.Label(master=top_frame, text="Режимы запуска алгоритмов", font=top_font)
    experiments_button = ttk.Button(master=top_frame,
                                    text="Решение задачи о назначениях",
                                    command=calculate,
                                    width=40
                                    )
    calculate_button = ttk.Button(master=top_frame,
                                  text="Вычислительный эксперимент",
                                  command=start_experiments,
                                  width=40
                                  )
    choice_series_label = ttk.Label(master=top_frame, text="Количество серий", font=medium_font)
    choice_series_input = ttk.Entry(master=top_frame, textvariable=count_series, width=13)
    modes_alg_label.place(x=720, y=0)
    experiments_button.place(x=575, y=25)
    calculate_button.place(x=830, y=25)
    choice_series_label.place(x=860, y=60)
    choice_series_input.place(x=985, y=60)

display_top_screen()



################################################# MATRIX FRAME ##################################


label_n_choice = ttk.Label(master=top_frame,
                           text="Размерность матрицы: {0}".format(n_choice))

def change_choice(newVal):
    float_value = float(newVal)  # получаем из строки значение float
    int_value = round(float_value)  # округляем до целочисленного значения
    label_n_choice["text"] = "Размерность матрицы: {0}".format(int_value)
    global n_choice
    n_choice = int_value
    fields_matrix.clear()
    for row in range(n_choice):
        for column in range(n_choice):
            value = StringVar(value="0")
            fields_matrix.append(value)
    rerun_left_frame()
    display_left_screen_down()

def display_left_screen_down():
    ####################################### ВЕРХНЯЯ ЧАСТЬ #######################################
    global label_n_choice

    koef_label = ttk.Label(master=matrix_frame,
                           text="Задание матрицы коэффициентов",
                           font=top_font
                           )
    label_n_choice = ttk.Label(master=matrix_frame,
                               text="Размерность матрицы: {0}".format(n_choice),
                               font=medium_font
                               )

    horizontalScale = ttk.Scale(master=matrix_frame,
                                orient=HORIZONTAL,
                                length=400,
                                from_=2.0,
                                to_=100.0,
                                value=n_choice,
                                command=change_choice
                                )

    koef_label.place(x=125, y=0)
    label_n_choice.place(x=50, y=35)
    horizontalScale.place(x=50, y=55)


    start_x = 50
    start_y = 80
    dif_y = 25
    dif_x = 150
    a_min_entry = ttk.Entry(master=matrix_frame, textvariable=a_min, validatecommand=check_a_min, validate="focusout")
    a_min_label = ttk.Label(master=matrix_frame, text="Нижняя граница a")
    err_label_a_min = ttk.Label(master=matrix_frame, foreground='red', textvariable=err_msg_a_min)

    a_max_entry = ttk.Entry(master=matrix_frame, textvariable=a_max,  validatecommand=check_a_max, validate="focusout")
    a_max_label = ttk.Label(master=matrix_frame, text="Верхняя граница a")
    err_label_a_max = ttk.Label(master=matrix_frame, foreground='red', textvariable=err_msg_a_max)

    b_min_entry = ttk.Entry(master=matrix_frame, textvariable=b_min, validatecommand=check_b_min, validate="focusout")
    b_min_label = ttk.Label(master=matrix_frame, text="Нижняя граница b")
    err_label_b_min = ttk.Label(master=matrix_frame, foreground='red', textvariable=err_msg_b_min)

    b_max_entry = ttk.Entry(master=matrix_frame, textvariable=b_max, validatecommand=check_b_max, validate="focusout")
    b_max_label = ttk.Label(master=matrix_frame, text="Верхняя граница b")
    err_label_b_max = ttk.Label(master=matrix_frame, foreground='red', textvariable=err_msg_b_max)

    a_min_label.place(x=start_x, y=start_y)
    a_min_entry.place(x=start_x, y=start_y + dif_y)
    err_label_a_min.place(x=20, y=start_y + 2 * dif_y)


    a_max_label.place(x=start_x + dif_x + 70, y=start_y)
    a_max_entry.place(x=start_x + dif_x + 70, y=start_y + dif_y)
    err_label_a_max.place(x=start_x + dif_x + 70, y=start_y + 2 * dif_y)

    b_min_label.place(x=start_x, y=start_y + 3 * dif_y)
    b_min_entry.place(x=start_x, y=start_y + 4 * dif_y)
    err_label_b_min.place(x=20, y=start_y + 5 * dif_y)

    b_max_label.place(x=start_x + dif_x + 70, y=start_y + 3 * dif_y)
    b_max_entry.place(x=start_x + dif_x + 70, y=start_y + 4 * dif_y)
    err_label_b_max.place(x=start_x + dif_x + 70,  y=start_y + 5 * dif_y)

    neorg_button = ttk.Checkbutton(text="Влияние неорганики", variable=neorganic_on)
    neorg_button.place(x=start_x+20, y=start_y + 9.8 * dif_y)

    random_button = ttk.Button(master=matrix_frame,
                               text="Сгенерировать матрицу",
                               command=gen_random_matr,
                               width=25
                               )

    random_button.place(x=start_x, y=start_y + 7 * dif_y)

    ############################################## МАТРИЦА ###############################################

    global is_generated_by_random

    show_matr_button = ttk.Button(master=matrix_frame,
                                  text="Показать матрицу",
                                  command=show_matrix)

    if n_choice > 5:
        show_matr_button.place(x=190, y=515)
    else:
        start_x = 20
        dif_x = 90
        start_y = 330
        dif_y = 25
        if fields_matrix:
            for row in range(n_choice):
                for column in range(n_choice):
                    field = ttk.Entry(master=matrix_frame,
                                      width=10,
                                      textvariable=fields_matrix[row * n_choice + column],
                                      justify=CENTER,
                                      validatecommand=check_field_matr,
                                      validate="key",
                                      font=cell_font
                                      )
                    field.place(x=start_x + dif_x * column, y=start_y + dif_y * row)
        else:
            for row in range(n_choice):
                for column in range(n_choice):
                    value = StringVar(value='0')
                    field = ttk.Entry(master=matrix_frame,
                                      width=10,
                                      textvariable=value,
                                      justify=CENTER,
                                      validatecommand=check_field_matr,
                                      validate="key",
                                      font=cell_font
                                      )
                    fields_matrix.append(value)
                    field.place(x=start_x + dif_x * column, y=start_y + dif_y * row)

display_left_screen_down()


##################### Создание меню ##########################
main_menu = Menu()
file_menu = Menu(tearoff=0)
save_menu = Menu(tearoff=0)
setting_menu = Menu(tearoff=0)

save_menu.add_command(label="Сохранить матрицу коэффициентов", command=save_matrix_coef)
save_menu.add_command(label="Сохранить график динамики целевых функций", command=save_res_in_graph)

file_menu.add_command(label="Загрузить матрицу из файла", command=load_matrix_from_file)

file_menu.add_cascade(label="Сохранить...", menu=save_menu)
main_menu.add_cascade(label="Файл", menu=file_menu)
root.config(menu=main_menu)


################################### RIGHT FRAME ########################################

def plot(has_data, is_experiment):
    fig = Figure(figsize=(5, 4),
                 dpi=100)

    colors = {'Оптимальный макс': 'red',
              'Оптимальный мин': 'blue',
              'Жадный алгоритм': 'orange',
              'Бережливый алгоритм': 'green'
              }
    global plot_to_save
    plot_to_save = fig
    plot1 = fig.add_subplot(111)
    if has_data:
        # plotting the graph
        for key, value in target_funcs.items():
            if key != 'Погрешность бережливого алг' and key != 'Погрешность жадного алг':
                plot_color = colors[key]
                plot1.plot(value, label=key, color=plot_color, linestyle='--', marker='o', linewidth=0.7)
        plot1.set_xlabel("Этапы переработки")
        plot1.set_ylabel("Значения целевой функции")
        if not target_funcs == {}:
            plot1.legend(loc='lower right')
        if is_experiment:
            plot1.set_title('Динамика усреднённых целевых функций', fontsize=11, fontweight='bold')
        else:
            plot1.set_title('Динамика целевых функций', fontsize=11, fontweight='bold')
    else:
        plot1.plot()

    canvas = FigureCanvasTkAgg(fig,
                               master=result_frame)
    canvas.draw()
    canvas.get_tk_widget().place(x=0, y=0)


def display_right_frame(has_data, is_experiment):
    plot(has_data, is_experiment)

    currentAlg = 0
    places = [(10, 420), (10, 440), (10, 460), (10, 480)]
    if is_experiment:
        res_work = ttk.Label(master=result_frame,
                         text="Значения усреднённых целевых функций:",
                         font=top_font
                         )
    else:
        res_work = ttk.Label(master=result_frame,
                             text="Результат работы алгоритмов:",
                             font=top_font
                             )
    res_work.place(x=0, y=400)

    if not is_experiment:
        if is_venger_max.get():
            venger_max_label = ttk.Label(master=result_frame,
                                         text="Венгерский максимум: {0}".format(results['Сумма (оптимальный макс)'])
                                         )
            venger_max_label.place(x=places[currentAlg][0], y=places[currentAlg][1])
            currentAlg += 1
        if is_venger_min.get():
            venger_min_label = ttk.Label(master=result_frame,
                                         text="Венгерский минимум: {0}".format(results['Сумма (оптимальный мин)'])
                                         )
            venger_min_label.place(x=places[currentAlg][0], y=places[currentAlg][1])
            currentAlg += 1
        if is_greedy.get():
            greedy_label = ttk.Label(master=result_frame,
                                     text="Жадный: {0}".format(results['Сумма (жадный алг)'])
                                     )
            greedy_label.place(x=places[currentAlg][0], y=places[currentAlg][1])
            # greedy_label_error = ttk.Label(master=result_frame,
            #                                text="Погрешность: {0}".format()
            #                                )
            # greedy_label_error.place(x=places[currentAlg][0] + 200, y=places[currentAlg][1])
            currentAlg += 1
        if is_thrifty.get():
            thrifty_label = ttk.Label(master=result_frame,
                                      text="Бережливый: {0}".format(results['Сумма (бережливый алг)'])
                                      )
            thrifty_label.place(x=places[currentAlg][0], y=places[currentAlg][1])
            # thrifty_label_error = ttk.Label(master=result_frame,
            #                                text="Погрешность: ")

            # thrifty_label_error.place(x=places[currentAlg][0] + 200, y=places[currentAlg][1])
    else:
        if is_venger_max.get():
            venger_max_label = ttk.Label(master=result_frame,
                                         text="Венгерский максимум: {0}".format(results['Оптимальный макс'])
                                         )
            venger_max_label.place(x=places[currentAlg][0], y=places[currentAlg][1])
            currentAlg += 1
        if is_venger_min.get():
            venger_min_label = ttk.Label(master=result_frame,
                                         text="Венгерский минимум: {0}".format(results['Оптимальный мин'])
                                         )
            venger_min_label.place(x=places[currentAlg][0], y=places[currentAlg][1])
            currentAlg += 1
        if is_greedy.get():
            greedy_label = ttk.Label(master=result_frame,
                                     text="Жадный: {0}".format(results['Жадный алгоритм'])
                                     )
            greedy_label.place(x=places[currentAlg][0], y=places[currentAlg][1])
            greedy_label_error = ttk.Label(master=result_frame,
                                           text="Относительная погрешность: {0}".format(results['Погрешность жадного алг'])
                                           )
            greedy_label_error.place(x=places[currentAlg][0] + 200, y=places[currentAlg][1])
            currentAlg += 1
        if is_thrifty.get():
            thrifty_label = ttk.Label(master=result_frame,
                                      text="Бережливый: {0}".format(results['Бережливый алгоритм'])
                                      )
            thrifty_label_error = ttk.Label(master=result_frame,
                                           text="Относительная погрешность: {0}".format(results['Погрешность бережливого алг']))
            thrifty_label.place(x=places[currentAlg][0], y=places[currentAlg][1])
            thrifty_label_error.place(x=places[currentAlg][0] + 200, y=places[currentAlg][1])

    button_get_res = ttk.Button(master=result_frame,
                                text="Сохранить результаты",
                                command=save_results)
    button_get_res.place(x=190, y=515)

display_right_frame(False, False)




root.mainloop()

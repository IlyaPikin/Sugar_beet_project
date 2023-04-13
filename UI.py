import random
from tkinter import *
from tkinter import ttk     # подключаем пакет ttk
from tkinter import filedialog
from tkinter import font
import numpy as np
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

###################### Настройки #############################

width_screen = 1100
height_screen = 720

###################### Создание окна #######################

root = Tk()
root.title("Sugar Beet")
root.geometry("{0}x{1}+350+200".format(width_screen, height_screen))
root.resizable(False, False)  # для того, чтобы запретить растягивание

################ Создание фреймов ############################

top_frame = ttk.Frame(master=root,
                      width=width_screen,
                      height=90,
                      borderwidth=1,
                      relief=SOLID
                      )

matrix_frame = ttk.Frame(master=root,
                         width=500,
                         height=600,
                         borderwidth=1,
                         relief=SOLID
                         )

result_frame = ttk.Frame(master=root,
                         width=503,
                         height=600,
                         borderwidth=1,
                         relief=SOLID
                         )

top_frame.place(x=0, y=0)

matrix_frame.place(x=20, y=100)
result_frame.place(x=575, y=100)

##################### Переменные состояния ####################

top_font = font.Font(weight="bold", size=12)
medium_font = font.Font(weight="bold", size=10)
cell_font = font.Font(size=13)

n_choice = 10
fields_matrix = []  # В ней хранятся инпут поля гуя
matrix = []  # полноценная матрица
matrix_show_button_onscreen = False
showed_matrix_fields = False
is_generated_by_random = False
neorganic_on = BooleanVar()

a_min = DoubleVar(value=0.5)
a_max = DoubleVar(value=0.5)
b_min = DoubleVar(value=0.5)
b_max = DoubleVar(value=0.5)

is_venger_max = BooleanVar(value=False)
is_venger_min = BooleanVar(value=False)
is_greedy = BooleanVar(value=False)
is_thrifty = BooleanVar(value=False)

count_series = IntVar(value=10)

is_experiment = False
is_calculating = False


###################### Шаблоны функций ########################

def dismiss(window):
    window.grab_release()
    window.destroy()


def load_matrix_from_file():
    filepath = filedialog.askopenfilename()


def save_res_in_table():
    filepath = filedialog.asksaveasfilename()


def save_res_in_graph():
    filepath = filedialog.asksaveasfilename()

def get_normal_matrix():
    pass

def gen_random_matr():
    global is_generated_by_random
    is_generated_by_random = True
    fields_matrix.clear()
    for row in range(n_choice):
        for column in range(n_choice):
            value = DoubleVar(value=random.randint(10, 30))
            fields_matrix.append(value)
    rerun_left_frame()
    display_left_screen_down()


def start_experiments():
    global is_experiment
    is_experiment = True

def rerun_left_frame():
    global matrix_frame
    matrix_frame.destroy()
    matrix_frame = ttk.Frame(master=root,
                             width=500,
                             height=600,
                             borderwidth=1,
                             relief=SOLID,
                             )
    matrix_frame.place(x=20, y=100)

def rerun_right_frame():
    global result_frame
    result_frame.destroy()
    result_frame = ttk.Frame(master=root,
                             width=505,
                             height=600,
                             borderwidth=1,
                             relief=SOLID
                             )
    result_frame.place(x=575, y=100)

def change_borders():
    pass


def calculate():
    global is_calculating
    is_calculating = True

def save_results():
    pass

def get_row_matrix(row):
    result = ""
    for i in range(n_choice):
        result += "{0} ".format(fields_matrix[row * n_choice + i].get())
    return result


def show_matrix():
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
                                    command=start_experiments,
                                    width=40
                                    )
    calculate_button = ttk.Button(master=top_frame,
                                  text="Вычислительный эксперимент",
                                  command=calculate,
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
            fields_matrix.append(DoubleVar())
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
    a_min_entry = ttk.Entry(master=matrix_frame, textvariable=a_min)
    a_min_label = ttk.Label(master=matrix_frame, text="Нижняя граница a")
    a_max_entry = ttk.Entry(master=matrix_frame, textvariable=a_max)
    a_max_label = ttk.Label(master=matrix_frame, text="Верхняя граница a")
    b_min_entry = ttk.Entry(master=matrix_frame, textvariable=b_min)
    b_min_label = ttk.Label(master=matrix_frame, text="Нижняя граница b")
    b_max_entry = ttk.Entry(master=matrix_frame, textvariable=b_max)
    b_max_label = ttk.Label(master=matrix_frame, text="Верхняя граница b")
    a_min_label.place(x=start_x, y=start_y)
    a_min_entry.place(x=start_x, y=start_y + dif_y)

    a_max_label.place(x=start_x + dif_x, y=start_y)
    a_max_entry.place(x=start_x + dif_x, y=start_y + dif_y)
    b_min_label.place(x=start_x, y=start_y + 2 * dif_y)
    b_min_entry.place(x=start_x, y=start_y + 3 * dif_y)
    b_max_label.place(x=start_x + dif_x, y=start_y + 2 * dif_y)
    b_max_entry.place(x=start_x + dif_x, y=start_y + 3 * dif_y)
    neorg_button = ttk.Checkbutton(text="Влияние неорганики", variable=neorganic_on)
    neorg_button.place(x=start_x+20, y=start_y + 9 * dif_y)

    random_button = ttk.Button(master=matrix_frame,
                               text="Сгенерировать матрицу",
                               command=gen_random_matr,
                               width=25
                               )

    random_button.place(x=start_x, y=start_y + 6.5 * dif_y)

    ############################################## МАТРИЦА ###############################################

    global is_generated_by_random

    show_matr_button = ttk.Button(master=matrix_frame,
                                  text="Показать матрицу",
                                  command=show_matrix)

    if n_choice > 5:
        show_matr_button.place(x=190, y=565)
    else:
        start_x = 20
        dif_x = 90
        start_y = 350
        dif_y = 25
        if is_generated_by_random:
            for row in range(n_choice):
                for column in range(n_choice):
                    field = ttk.Entry(master=matrix_frame,
                                      width=10,
                                      textvariable=fields_matrix[row * n_choice + column],
                                      justify=CENTER,
                                      font=cell_font
                                      )
                    field.place(x=start_x + dif_x * column, y=start_y + dif_y * row)
        else:
            for row in range(n_choice):
                for column in range(n_choice):
                    value = DoubleVar()
                    field = ttk.Entry(master=matrix_frame,
                                      width=10,
                                      textvariable=value,
                                      justify=CENTER,
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

save_menu.add_command(label="Сохранить таблицу погрешностей", command=save_res_in_table)
save_menu.add_command(label="Сохранить ", command=save_res_in_graph)

file_menu.add_command(label="Загрузить матрицу из файла", command=load_matrix_from_file)

file_menu.add_cascade(label="Сохранить...", menu=save_menu)
main_menu.add_cascade(label="Файл", menu=file_menu)
root.config(menu=main_menu)








################################### RIGHT FRAME ########################################

def plot():
    fig = Figure(figsize=(5, 4.5),
                 dpi=100)

    # list of squares
    y = [i ** 2 for i in range(101)]

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(y)
    canvas = FigureCanvasTkAgg(fig,
                               master=result_frame)
    canvas.draw()


    canvas.get_tk_widget().place(x=0, y=0)


def display_right_frame():
    plot()

    currentAlg = 0
    places = [(10, 470), (10, 490), (10, 510), (10, 530)]

    if True:
        res_work = ttk.Label(master=result_frame,
                             text="Результат работы алгоритмов:",
                             font=top_font
                             )
        res_work.place(x=0, y=450)

        if is_venger_max.get():
            venger_max_label = ttk.Label(master=result_frame,
                                         text="Венгерский максимум: "
                                         )
            venger_max_label.place(x=places[currentAlg][0], y=places[currentAlg][1])
            currentAlg += 1
        if is_venger_min.get():
            venger_min_label = ttk.Label(master=result_frame,
                                         text="Венгерский минимум: "
                                         )
            venger_min_label.place(x=places[currentAlg][0], y=places[currentAlg][1])
            currentAlg += 1
        if is_greedy.get():
            greedy_label = ttk.Label(master=result_frame,
                                     text="Жадный: "
                                     )
            greedy_label.place(x=places[currentAlg][0], y=places[currentAlg][1])
            greedy_label_error = ttk.Label(master=result_frame,
                                           text="Погрешность: "
                                           )
            greedy_label_error.place(x=places[currentAlg][0] + 200, y=places[currentAlg][1])
            currentAlg += 1
        if is_thrifty.get():
            thrifty_label = ttk.Label(master=result_frame,
                                      text="Бережливый: "
                                      )
            thrifty_label_error = ttk.Label(master=result_frame,
                                           text="Погрешность: ")
            thrifty_label.place(x=places[currentAlg][0], y=places[currentAlg][1])
            thrifty_label_error.place(x=places[currentAlg][0] + 200, y=places[currentAlg][1])

    button_get_res = ttk.Button(master=result_frame,
                                text="Сохранить результаты",
                                command=save_results)
    button_get_res.place(x=190, y=565)

display_right_frame()




root.mainloop()

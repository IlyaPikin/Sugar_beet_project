import random
from tkinter import *
from tkinter import ttk     # подключаем пакет ttk
from tkinter import filedialog
import numpy as np
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
root.resizable(False, False) # для того, чтобы запретить растягивание

################ Создание фреймов ############################

top_frame = ttk.Frame(master=root,
                      width=width_screen,
                      height=height_screen*0.2,
                      borderwidth=1,
                      relief=SOLID,
                      padding=20
                      )

matrix_frame = ttk.Frame(master=root,
                         width=500,
                         height=500
                         )

result_frame = ttk.Frame(master=root,
                      width=500,
                      height=500
                      )

top_frame.pack(anchor='n', fill=BOTH)
matrix_frame.pack(side=LEFT)
result_frame.pack(side=RIGHT)

##################### Переменные состояния ####################

n_choice = 10
fields_matrix = [] # В ней хранятся инпут поля гуя
matrix = [] # полноценная матрица
matrix_show_button_onscreen = False
showed_matrix_fields = False
is_generated_by_random= False

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

def gen_random_matr():
    global is_generated_by_random
    is_generated_by_random=True
    fields_matrix.clear()
    for row in range(n_choice):
        for column in range(n_choice):
            value = DoubleVar(value=random.randint(10, 30))
            fields_matrix.append(value)
    display_matrix(n_choice, matrix_frame)


def start_experiments():
    pass

def change_borders():
    pass

def calculate():
    pass

def get_row_matrix(row):
    result = ""
    for i in range(n_choice):
        result += "{0} ".format(fields_matrix[row*n_choice + i].get())
    return result

def show_matrix():
    window = Toplevel()
    window.title("Матрица")
    window.geometry("400x400")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window))
    for row in range(n_choice):
        label = ttk.Label(master=window, text=get_row_matrix(row))
        label.pack(anchor="nw")



show_matr_button = ttk.Button(master=matrix_frame,
                           text="Показать матрицу",
                           command=show_matrix)

show_matr_button.place(x=250, y=200)

def destroy_matrix():
    global fields_matrix
    for value in fields_matrix:
        value.destroy()
    fields_matrix.clear()


def display_matrix(n_choice, frame):

    global matrix_frame
    global matrix_show_button_onscreen
    global showed_matrix_fields
    global show_matr_button
    global is_generated_by_random

    if n_choice > 5:
        if not matrix_show_button_onscreen:
            matrix_frame.destroy()
            matrix_frame = ttk.Frame(master=root,
                                     width=500,
                                     height=500
                                     )
            matrix_frame.pack(side=LEFT)
            show_matr_button = ttk.Button(master=matrix_frame,
                           text="Показать матрицу",
                           command=show_matrix)

            show_matr_button.place(x=250, y=200)
            matrix_show_button_onscreen = True
            showed_matrix_fields = False
    else:
        if is_generated_by_random:
            is_generated_by_random = False
            matrix_frame.destroy()
            matrix_frame = ttk.Frame(master=root,
                                     width=500,
                                     height=500
                                     )
            matrix_frame.place(x=60, y=250)
            matrix_show_button_onscreen = False
            showed_matrix_fields = True
            for row in range(n_choice):
                for column in range(n_choice):
                    field = ttk.Entry(master=matrix_frame,
                                      width=15,
                                      textvariable=fields_matrix[row * n_choice + column],
                                      justify=CENTER)
                    field.grid(row=row, column=column)
        elif matrix_show_button_onscreen:
            show_matr_button.destroy()
            matrix_frame.destroy()
            matrix_frame = ttk.Frame(master=root,
                                     width=500,
                                     height=500
                                     )
            matrix_frame.place(x=60, y=250)
            matrix_show_button_onscreen = False
            showed_matrix_fields = True
            for row in range(n_choice):
                for column in range(n_choice):
                    value = DoubleVar()
                    field = ttk.Entry(master=matrix_frame,
                                      width=15,
                                      textvariable=value,
                                      justify=CENTER)
                    fields_matrix.append(value)
                    field.grid(row=row, column=column)
        else:
            matrix_show_button_onscreen = False
            matrix_frame.destroy()
            show_matr_button.destroy()
            matrix_frame.destroy()
            matrix_frame = ttk.Frame(master=root,
                                     width=500,
                                     height=500
                                     )
            matrix_frame.place(x=60, y=250)
            for row in range(n_choice):
                for column in range(n_choice):
                    value = DoubleVar()
                    field = ttk.Entry(master=matrix_frame,
                                      width=15,
                                      textvariable=value,
                                      justify=CENTER)
                    fields_matrix.append(value)
                    field.grid(row=row, column=column)




##################### Создание меню ##########################
main_menu = Menu()
file_menu = Menu(tearoff=0)
save_menu = Menu(tearoff=0)
setting_menu = Menu(tearoff=0)

save_menu.add_command(label="Сохранить таблицу погрешностей", command=save_res_in_table)
save_menu.add_command(label="Сохранить ", command=save_res_in_graph)

file_menu.add_command(label="Загрузить матрицу из файла", command=load_matrix_from_file)




a_min = DoubleVar(value=0.5)
a_max = DoubleVar(value=0.5)
b_min = DoubleVar(value=0.5)
b_max = DoubleVar(value=0.5)

def border_screen():
    window = Toplevel()
    window.title("Выбор алгоритмов")
    window.geometry("400x400")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window))
    close_button = ttk.Button(master=window, text="Готово", command=lambda: dismiss(window))
    a_min_entry = ttk.Entry(master=window, textvariable=a_min)
    a_min_label = ttk.Label(master=window, text="Нижняя граница a")
    a_max_entry = ttk.Entry(master=window, textvariable=a_max)
    a_max_label = ttk.Label(master=window, text="Верхняя граница a")
    b_min_entry = ttk.Entry(master=window, textvariable=b_min)
    b_min_label = ttk.Label(master=window, text="Нижняя граница b")
    b_max_entry = ttk.Entry(master=window, textvariable=b_max)
    b_max_label = ttk.Label(master=window, text="Верхняя граница b")
    a_min_label.pack(anchor=NW)
    a_min_entry.pack(anchor=NW)
    a_max_label.pack(anchor=NW)
    a_max_entry.pack(anchor=NW)
    b_min_label.pack(anchor=NW)
    b_min_entry.pack(anchor=NW)
    b_max_label.pack(anchor=NW)
    b_max_entry.pack(anchor=NW)

    close_button.pack(anchor="center", expand=1)
    window.grab_set()

setting_menu.add_command(label="Изменить границы генерации", command=border_screen)

file_menu.add_cascade(label="Сохранить...", menu=save_menu)
main_menu.add_cascade(label="Файл", menu=file_menu)
main_menu.add_cascade(label="Настройки генерации", menu=setting_menu)
root.config(menu=main_menu)




######################## Заполнение 1 фрейма ###############################

label_n_choice = ttk.Label(master=top_frame,
                           text="Размерность матрицы: {0}".format(n_choice))

def change_choice(newVal):
    float_value = float(newVal)     # получаем из строки значение float
    int_value = round(float_value)  # округляем до целочисленного значения
    label_n_choice["text"] = "Размерность матрицы: {0}".format(int_value)
    global n_choice
    n_choice = int_value
    fields_matrix.clear()
    for row in range(n_choice):
        for column in range(n_choice):
            fields_matrix.append(DoubleVar())
    display_matrix(n_choice, matrix_frame)


horizontalScale = ttk.Scale(master=top_frame,
                            orient=HORIZONTAL,
                            length=400,
                            from_=2.0,
                            to_=100.0,
                            value=10,
                            command=change_choice)
label_n_choice.pack(anchor='nw')
horizontalScale.pack(anchor='w')

random_button = ttk.Button(master=top_frame,
                         text="Сгенерировать матрицу",
                         command=gen_random_matr,
                         width=25
                         )

x_coord_first_button = 470

random_button.place(x=x_coord_first_button, y=15)

experiments_button = ttk.Button(master=top_frame,
                         text="Провети эксперимент",
                         command=start_experiments,
                         width=25
                         )

experiments_button.place(x=x_coord_first_button + 170, y=15)


is_venger = IntVar()
is_greedy = IntVar()
is_thrifty = IntVar()

def choice_screen():
    window = Toplevel()
    window.title("Выбор алгоритмов")
    window.geometry("400x400")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window))
    close_button = ttk.Button(window, text="Готово", command=lambda: dismiss(window))
    venger_button = ttk.Checkbutton(window,
                                    text="Венгерский алгоритм",
                                    variable=is_venger)
    greedy_button = ttk.Checkbutton(window,
                                    text="Венгерский алгоритм",
                                    variable=is_greedy)
    thrifty_button = ttk.Checkbutton(window,
                                    text="Жадный алгоритм",
                                    variable=is_thrifty)
    venger_button.pack(anchor="nw")
    greedy_button.pack(anchor="nw")
    thrifty_button.pack(anchor="nw")
    close_button.pack(anchor="center", expand=1)
    window.grab_set()

choice_algs_button = ttk.Button(master=top_frame,
                         text="Выбрать алгоритмы",
                         command=choice_screen,
                         width=20
                         )

choice_algs_button.place(x=x_coord_first_button + 170+170, y=15)

calculate_button = ttk.Button(master=top_frame,
                         text="Посчитать",
                         command=calculate,
                         width=15
                         )

calculate_button.place(x=x_coord_first_button + 170+170 + 140, y=15)


################################### left frame #############################
def plot(window):
    fig = Figure(figsize=(5, 5),
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

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   result_frame)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

plot(result_frame)
result_label = ttk.Label(master=result_frame, text="Результат: ")
result_label.pack()

root.mainloop()

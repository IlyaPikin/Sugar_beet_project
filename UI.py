from tkinter import *
from tkinter import ttk     # подключаем пакет ttk
from tkinter import filedialog
###################### Настройки #############################
width_screen = 1100
height_screen = 720


##################### Переменные состояния ####################
n_choice = 10

###################### Шаблоны функций ########################
def load_matrix_from_file():
    filepath = filedialog.askopenfilename()

def save_res_in_table():
    filepath = filedialog.asksaveasfilename()

def save_res_in_graph():
    filepath = filedialog.asksaveasfilename()

def gen_random_matr(n_choice):
    pass

def start_experiments():
    pass

def change_borders():
    pass

def calculate():
    pass

###################### Создание окна #######################
root = Tk()
root.title("Sugar Beet")
root.geometry("{0}x{1}+350+200".format(width_screen, height_screen))
root.resizable(False, False) # для того, чтобы запретить растягивание




##################### Создание меню ##########################
main_menu = Menu()
file_menu = Menu(tearoff=0)
save_menu = Menu(tearoff=0)
setting_menu = Menu(tearoff=0)

save_menu.add_command(label="Table", command=save_res_in_table)
save_menu.add_command(label="Graphic", command=save_res_in_graph)

file_menu.add_command(label="Load matrix", command=load_matrix_from_file)

def dismiss(window):
    window.grab_release()
    window.destroy()


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

setting_menu.add_command(label="Change borders", command=border_screen)

file_menu.add_cascade(label="Save", menu=save_menu)
main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Setting", menu=setting_menu)
root.config(menu=main_menu)


################ Создание фреймов ############################

top_frame = ttk.Frame(master=root,
                      width=width_screen,
                      height=height_screen*0.2,
                      borderwidth=1,
                      relief=SOLID,
                      padding=20
                      )

matrix_frame = ttk.Frame(master=root,
                      width=width_screen / 2,
                      height=height_screen*0.8,
                      borderwidth=1,
                      relief=SOLID,
                      )

result_frame = ttk.Frame(master=root,
                      width=width_screen / 2,
                      height=height_screen*0.8,
                      borderwidth=1,
                      relief=SOLID,
                      )

top_frame.pack(anchor='n', fill=X)
matrix_frame.pack(anchor='w')
result_frame.pack(anchor='e')

######################## Заполнение 1 фрейма ###############################

label_n_choice = ttk.Label(master=top_frame,
                           text="Размерность матрицы: {0}".format(n_choice))

def change_choice(newVal):
    float_value = float(newVal)     # получаем из строки значение float
    int_value = round(float_value)  # округляем до целочисленного значения
    label_n_choice["text"] = "Размерность матрицы: {0}".format(int_value)
    global n_choice
    n_choice = int_value

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
                         text="Random",
                         command=gen_random_matr(n_choice),
                         width=15
                         )

random_button.place(x=550, y=15)

experiments_button = ttk.Button(master=top_frame,
                         text="Experiment",
                         command=start_experiments,
                         width=15
                         )

experiments_button.place(x=550 + 125, y=15)


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
                         text="Choice Algs",
                         command=choice_screen,
                         width=15
                         )

choice_algs_button.place(x=675 + 125, y=15)

calculate_button = ttk.Button(master=top_frame,
                         text="Calculate",
                         command=calculate,
                         width=15
                         )

calculate_button.place(x=925, y=15)

############################ Frame 2 ###############################


root.mainloop()

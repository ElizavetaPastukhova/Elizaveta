import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Data import *


def load_file():
    global tree_new, tree_actual
    if combobox.current() == -1:
        tkinter.messagebox.showerror(title="Ошибка", message="Не выбрана гайка")
    else:
        index = combobox.current()
        filepath = filedialog.askopenfilename()
        if filepath != "":
            with open(filepath, "r") as file:
                try:
                    line = file.readline()
                    values1 = [float(i) for i in line.split()]
                    if len(values1) != len(gaikas[index]["actual"]):
                        tkinter.messagebox.showerror(title="Ошибка", message="Некорректные данные в файле")
                        return 0
                    for i in range(len(values1)):
                        tree_actual.insert("", END, values=(gaikas[index]["actual"][i], values1[i]))
                    tree_actual.insert("", END, values=("-------------------", "-------------------"))
                    time_actual = sum(values1) * 60

                    line = file.readline()
                    values2 = [float(i) for i in line.split()]
                    if len(values2) != len(gaikas[index]["new"]):
                        tkinter.messagebox.showerror(title="Ошибка", message="Некорректные данные в файле")
                        return 0
                    for i in range(len(values2)):
                        tree_new.insert("", END, values=(gaikas[index]["new"][i], values2[i]))
                    tree_new.insert("", END, values=("-------------------", "-------------------"))
                    time_new = sum(values1) * 60


                    line = file.readline()
                    values3 = [float(i) for i in line.split()]
                    if len(values3) != len(type_actual):
                        tkinter.messagebox.showerror(title="Ошибка", message="Некорректные данные в файле")
                        return 0
                    for i in range(len(values3)):
                        tree_actual.insert("", END, values=(type_actual[i], values3[i]))

                    colvo_rab = values3[0]
                    zp_rab = values3[1]
                    income = values3[2]
                    V_ready = values3[3]
                    brack_act = values3[4]


                    line = file.readline()
                    values4 = [float(i) for i in line.split()]
                    if len(values4) != len(type_new):
                        tkinter.messagebox.showerror(title="Ошибка", message="Некорректные данные в файле")
                        return 0
                    for i in range(len(values4)):
                        tree_new.insert("", END, values=(type_new[i], values4[i]))

                    zatrat_vnedr = values4[0]
                    plan_income = values4[1]
                    V_proizv = values4[2]
                    brack_new = values4[3]

                    count_results_new(zatrat_vnedr, plan_income, time_new, brack_new, V_proizv)
                    count_results_actual(zp_rab, colvo_rab, zatrat_vnedr/plan_income, income, time_actual,
                                         brack_act, V_ready)
                except:
                    tkinter.messagebox.showerror(title="Ошибка", message="Некорректные данные в файле")

#Заполняем таблицу результатов
def count_results_actual(zp_month, count_r, srok_okup, income, itog_time, V_brak, V_all):
    tree_actual_result.insert('', END, values=(result_actual[0], f"{zp_month*count_r*srok_okup} руб"))
    tree_actual_result.insert('', END, values=(result_actual[1], f"{income/(zp_month*count_r*srok_okup)} руб/руб"))
    tree_actual_result.insert('', END, values=(result_actual[2], f"{itog_time * V_all} н/ч"))
    tree_actual_result.insert('', END, values=(result_actual[3], f"{V_brak*100/V_all} %"))
#Заполняем таблицу результатов
def count_results_new(vnedrenie, income, itog_time, V_brak, V_all):
    tree_new_result.insert('', END, values=(result_actual[0], f"{vnedrenie/income}"))
    tree_new_result.insert('', END, values=(result_actual[1], f"{income /vnedrenie} руб/руб"))
    tree_new_result.insert('', END, values=(result_actual[2], f"{itog_time * V_all} н/ч"))
    tree_new_result.insert('', END, values=(result_actual[3], f"{round(V_brak*100/V_all, 2)} %"))

#Создание окна
root = Tk()
root.title("Программа")
root.geometry("1200x800")

#Разметка страницы
for c in range(2): root.columnconfigure(index=c, weight=1)
for r in range(2): root.rowconfigure(index=r, weight=1)
root.rowconfigure(index=2, weight=2)
root.rowconfigure(index=3, weight=1)
root.rowconfigure(index=4, weight=2)

#Выпадающий список
combobox = ttk.Combobox(values=types)
combobox.grid(row=0, column=0, columnspan=2)
#Кнопка загрузить данные
button_result = Button(text="Загрузить данные",  command=load_file)
button_result.grid(row=1, column=0, columnspan=4)

#Заголовок
label_actual = Label(text='Актуальная технология')
label_actual.grid(row=2, column=0)
#Заголовок
label_newest = Label(text='Новая технология')
label_newest.grid(row=2, column=1)

#Создаем таблицу
columns = ("name", "value")
tree_actual = ttk.Treeview(columns=columns, show="headings", selectmode="browse")
tree_actual.grid(row=2, column=0)

tree_actual.heading("name", text="Название операции")
tree_actual.heading("value", text="Значение Т маш., н/ч")

tree_new = ttk.Treeview(columns=columns, show="headings", selectmode="browse")
tree_new.grid(row=2, column=1)

tree_new.heading("name", text="Название операции")
tree_new.heading("value", text="Значение Т маш., н/ч")

#Заголовок
label_result_act = Label(text="Результат:")
label_result_act.grid(row=3, column=0, columnspan=2)

columns2= ("name", "result")
# actual table
tree_actual_result = ttk.Treeview(columns=columns2, show="headings", selectmode="browse")
tree_actual_result.grid(row=4, column=0)

tree_actual_result.heading("name", text="Категория")
tree_actual_result.heading("result", text="Результат")
# new table
tree_new_result = ttk.Treeview(columns=columns2, show="headings", selectmode="browse")
tree_new_result.grid(row=4, column=1)

tree_new_result.heading("name", text="Категория")
tree_new_result.heading("result", text="Результат")


root.mainloop()

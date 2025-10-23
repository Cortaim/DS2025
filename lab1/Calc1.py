import tkinter as tk
from tkinter import messagebox
from decimal import Decimal, getcontext, InvalidOperation

getcontext().prec = 30

MIN_VALUE = Decimal("-1000000000000.000000")
MAX_VALUE = Decimal("1000000000000.000000")

root = tk.Tk()
root.title("Финансовый калькулятор v1")
root.geometry("420x350")
root.resizable(False, False)

student_info = tk.Label(
    root,
    text="ФИО: Сердюков Вадим Васильевич\nКурс: 4\nГруппа: 4\nГод: 2025",
    font=("Arial", 11),
    justify="left",
)
student_info.pack(pady=10)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Первое число:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5)
entry_num1 = tk.Entry(frame_inputs, width=25, font=("Arial", 11))
entry_num1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Второе число:", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=5)
entry_num2 = tk.Entry(frame_inputs, width=25, font=("Arial", 11))
entry_num2.grid(row=1, column=1, padx=5, pady=5)

operation_var = tk.StringVar(value="Сложение")
frame_ops = tk.Frame(root)
frame_ops.pack(pady=5)

tk.Label(frame_ops, text="Операция:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
operation_menu = tk.OptionMenu(frame_ops, operation_var, "Сложение", "Вычитание")
operation_menu.config(font=("Arial", 11))
operation_menu.pack(side=tk.LEFT, padx=5)

result_label = tk.Label(root, text="Результат:", font=("Arial", 12, "bold"))
result_label.pack(pady=10)

result_value = tk.Label(root, text="", font=("Arial", 12))
result_value.pack()

def calculate():
    num1_str = entry_num1.get().replace(",", ".")
    num2_str = entry_num2.get().replace(",", ".")

    try:
        num1 = Decimal(num1_str)
        num2 = Decimal(num2_str)
    except InvalidOperation:
        messagebox.showerror("Ошибка", "Некорректный ввод числа.")
        return

    if not (MIN_VALUE <= num1 <= MAX_VALUE) or not (MIN_VALUE <= num2 <= MAX_VALUE):
        messagebox.showerror("Ошибка", "Введено число вне допустимого диапазона.")
        return

    if operation_var.get() == "Сложение":
        result = num1 + num2
    else:
        result = num1 - num2

    if result < MIN_VALUE or result > MAX_VALUE:
        result_value.config(text="Переполнение диапазона", fg="red")
        return

    result_value.config(text=format(result, 'f'), fg="black")

calc_button = tk.Button(root, text="Вычислить", command=calculate, font=("Arial", 12))
calc_button.pack(pady=10)

hint = tk.Label(
    root,
    text="Поддерживаются Ctrl+C / Ctrl+V в любой раскладке\n"
         "Можно использовать запятую или точку\n"
         "Диапазон: ±1 000 000 000 000.000000",
    font=("Arial", 9),
    fg="gray",
)
hint.pack(side=tk.BOTTOM, pady=10)

def enable_crosslayout_copy_paste(entry_widget):
    def on_ctrl_key(event):
        # Ctrl + C (англ и рус)
        if event.state & 0x4 and event.keycode == 67:
            entry_widget.event_generate("<<Copy>>")
            return "break"
        # Ctrl + V (англ и рус)
        if event.state & 0x4 and event.keycode == 86:
            entry_widget.event_generate("<<Paste>>")
            return "break"

    entry_widget.bind("<KeyPress>", on_ctrl_key, add=True)

enable_crosslayout_copy_paste(entry_num1)
enable_crosslayout_copy_paste(entry_num2)

root.mainloop()
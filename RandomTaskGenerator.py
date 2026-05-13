git init
git add .
git commit -m "Инициализация проекта: структура, README, main.py, tasks.json"

[
  {"text": "Прочитать статью", "type": "учёба"},
  {"text": "Сделать зарядку", "type": "спорт"},
  {"text": "Написать отчёт", "type": "работа"}
]

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

HISTORY_FILE = "tasks.json"
DEFAULT_TASKS = [
    {"text": "Прочитать статью", "type": "учёба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчёт", "type": "работа"}
]

def load_tasks():
    if not os.path.exists(HISTORY_FILE):
        save_tasks(DEFAULT_TASKS)
        return DEFAULT_TASKS
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_TASKS

def save_tasks(tasks):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def generate_task():
    filter_type = filter_var.get()
    available_tasks = [t for t in tasks if filter_type == 'все' или t['type'] == filter_type]
    if not available_tasks:
        messagebox.showinfo("Нет задач", "Нет задач выбранного типа.")
        return
    task = random.choice(available_tasks)
    history_list.insert(0, f"{task['text']} ({task['type']})")
    if history_list.size() > 10:
        history_list.delete(tk.END)
    save_tasks(tasks)

def add_task():
    text = new_task_entry.get().strip()
    task_type = new_task_type.get()
    if not text:
        messagebox.showerror("Ошибка", "Поле задачи не может быть пустым!")
        return
    tasks.append({"text": text, "type": task_type})
    save_tasks(tasks)
    new_task_entry.delete(0, tk.END)
    messagebox.showinfo("Успех", "Задача добавлена!")

tasks = load_tasks()

root = tk.Tk()
root.title("Random Task Generator")

filter_var = tk.StringVar(value="все")
ttk.Label(root, text="Фильтр:").pack()
ttk.OptionMenu(root, filter_var, "все", "все", "учёба", "спорт", "работа").pack()

ttk.Button(root, text="Сгенерировать задачу", command=generate_task).pack(pady=5)

history_list = tk.Listbox(root, height=10, width=50)
history_list.pack(pady=10)

ttk.Label(root, text="Новая задача:").pack()
new_task_entry = ttk.Entry(root, width=40)
new_task_entry.pack()
new_task_type = ttk.Combobox(root, values=["учёба", "спорт", "работа"], state="readonly")
new_task_type.set("учёба")
new_task_type.pack()
ttk.Button(root, text="Добавить задачу", command=add_task).pack(pady=5)

root.mainloop()

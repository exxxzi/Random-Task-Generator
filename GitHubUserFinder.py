import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import requests
import json
import os

FAVORITES_FILE = "favorites.json"
GITHUB_API_URL = "https://api.github.com/search/users"

def load_favorites():
    if not os.path.exists(FAVORITES_FILE):
        return []
    with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_favorites(favs):
    with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
        json.dump(favs, f, ensure_ascii=False, indent=2)

def search_user():
    query = entry_search.get().strip()
    if not query:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым!")
        return
    try:
        response = requests.get(GITHUB_API_URL, params={'q': query})
        response.raise_for_status()
        data = response.json()
        results = data.get('items', [])
        listbox_results.delete(0, tk.END)
        for user in results:
            listbox_results.insert(tk.END, f"{user['login']} (score: {user['score']})")
    except Exception as e:
        messagebox.showerror("Ошибка API", str(e))

def add_to_favorites():
    selected = listbox_results.curselection()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите пользователя из результатов поиска!")
        return
    login = listbox_results.get(selected[0]).split()[0]
    if login in [u['login'] for u in favorites]:
        messagebox.showinfo("Информация", "Пользователь уже в избранном!")
        return
    try:
        user_data = requests.get(f"https://api.github.com/users/{login}").json()
        favorites.append(user_data)
        save_favorites(favorites)
        listbox_favs.insert(tk.END, f"{user_data['login']}")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def show_favorites():
    listbox_favs.delete(0, tk.END)
    for user in favorites:
        listbox_favs.insert(tk.END, f"{user['login']}")

def show_details():
    selected = listbox_results.curselection()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите пользователя из результатов поиска!")
        return
    login = listbox_results.get(selected[0]).split()[0]
    for user in favorites + [requests.get(f"https://api.github.com/users/{login}").json()]:
        if user.get('login') == login:
            details = Toplevel(root)
            details.title(f"Детали: {user['login']}")
            for key, value in user.items():
                ttk.Label(details, text=f"{key}: {value}").pack(anchor='w')
            break

# Загрузка избранного
favorites = load_favorites()

# Основное окно
root = tk.Tk()
root.title("GitHub User Finder")

# Поле поиска и кнопка
ttk.Label(root, text="Поиск пользователя:").pack()
entry_search = ttk.Entry(root, width=40)
entry_search.pack()
ttk.Button(root, text="Поиск", command=search_user).pack(pady=5)
entry_search.bind('<Return>', lambda e: search_user())

# Результаты поиска
ttk.Label(root, text="Результаты:").pack()
listbox_results = tk.Listbox(root, height=10, width=50)
listbox_results.pack(pady=5)
ttk.Button(root, text="⭐ В избранное", command=add_to_favorites).pack()
ttk.Button(root, text="📋 Детали", command=show_details).pack()

# Избранное
ttk.Label(root, text="Избранное:").pack()
listbox_favs = tk.Listbox(root, height=10, width=50)
listbox_favs.pack(pady=5)
ttk.Button(root, text="Показать избранное", command=show_favorites).pack()

root.mainloop()

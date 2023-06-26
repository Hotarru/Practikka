import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Создание подключения к базе данных MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Asdhgfkljqznipvcyr3526970ot@',
    database="mydb"
)

# Создание объекта "курсор" для выполнения SQL-запросов
cursor = conn.cursor()

# Создание таблицы users (если не существует)
def create_users_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """
    cursor.execute(create_table_query)
    conn.commit()

create_users_table()

# Функция для регистрации пользователя
def register_user():
    username = register_username_entry.get()
    password = register_password_entry.get()

    if not username or not password:
        messagebox.showerror("Ошибка", "Требуются имя пользователя и пароль.")
        return

    select_query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(select_query)
    user = cursor.fetchone()

    if user:
        messagebox.showerror("Ошибка", "Имя пользователя уже существует. Пожалуйста, выберите другое имя пользователя.")
    else:
        insert_query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
        cursor.execute(insert_query)
        conn.commit()
        messagebox.showinfo("Успешно", "Регистрация прошла успешно. Теперь вы можете войти в систему.")

        # Очистка полей ввода
        register_username_entry.delete(0, tk.END)
        register_password_entry.delete(0, tk.END)

# Функция для авторизации пользователя
def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not username or not password:
        messagebox.showerror("Ошибка", "Требуются имя пользователя и пароль.")
        return

    select_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(select_query)
    user = cursor.fetchone()

    if user:
        # Очистка полей ввода
        login_username_entry.delete(0, tk.END)
        login_password_entry.delete(0, tk.END)

        # Скрытие окна регистрации и отображение фрейма с фильтрами и кнопкой обновления
        register_frame.pack_forget()
        filter_frame.pack()
        update_button.pack()

        # Загрузка логов из базы данных и отображение их в таблице
        update_logs()
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")

# Функция для получения записей из таблицы access_logs с примененными фильтрами
def get_filtered_logs():
    ip_filter = ip_entry.get()
    timestamp_filter = timestamp_entry.get()
    
    select_query = f"SELECT ip_address, timestamp, status, size, referer, user_agent FROM access_logs WHERE ip_address LIKE '%{ip_filter}%' AND timestamp LIKE '%{timestamp_filter}%'"
    cursor.execute(select_query)
    logs = cursor.fetchall()
    return logs

# Функция для обновления данных в таблице с применением фильтров
def update_logs():
    # Очистка таблицы
    table.delete(*table.get_children())
    # Загрузка отфильтрованных логов из базы данных и отображение их в таблице
    logs = get_filtered_logs()
    for log in logs:
        table.insert("", tk.END, values=log)

# Создание графического интерфейса с использованием tkinter
root = tk.Tk()
root.title("Log Viewer")
root.geometry("800x600")  # Изменение размера окна

# Создание фрейма для регистрации
register_frame = ttk.Frame(root)
register_frame.pack(pady=10)

# Entry для регистрации по имени пользователя
register_username_label = ttk.Label(register_frame, text="Username:")
register_username_label.grid(row=0, column=0, padx=5)
register_username_entry = ttk.Entry(register_frame, width=20)
register_username_entry.grid(row=0, column=1, padx=5)

# Entry для регистрации по паролю
register_password_label = ttk.Label(register_frame, text="Password:")
register_password_label.grid(row=1, column=0, padx=5)
register_password_entry = ttk.Entry(register_frame, width=20, show="*")
register_password_entry.grid(row=1, column=1, padx=5)

# Кнопка "Зарегистрироваться"
register_button = ttk.Button(register_frame, text="Зарегистрироваться", command=register_user)
register_button.grid(row=2, column=1, padx=5, pady=5)

# Создание фрейма для авторизации
login_frame = ttk.Frame(root)
login_frame.pack(pady=10)

# Entry для авторизации по имени пользователя
login_username_label = ttk.Label(login_frame, text="Username:")
login_username_label.grid(row=0, column=0, padx=5)
login_username_entry = ttk.Entry(login_frame, width=20)
login_username_entry.grid(row=0, column=1, padx=5)

# Entry для авторизации по паролю
login_password_label = ttk.Label(login_frame, text="Password:")
login_password_label.grid(row=1, column=0, padx=5)
login_password_entry = ttk.Entry(login_frame, width=20, show="*")
login_password_entry.grid(row=1, column=1, padx=5)

# Кнопка "Войти"
login_button = ttk.Button(login_frame, text="Войти", command=login_user)
login_button.grid(row=2, column=1, padx=5, pady=5)

# Создание фрейма для фильтров и кнопки обновления
filter_frame = ttk.Frame(root)

# Entry для фильтрации по IP Address
ip_label = ttk.Label(filter_frame, text="IP Address:")
ip_label.grid(row=0, column=0, padx=5)
ip_entry = ttk.Entry(filter_frame, width=20)
ip_entry.grid(row=0, column=1, padx=5)

# Entry для фильтрации по Timestamp
timestamp_label = ttk.Label(filter_frame, text="Timestamp:")
timestamp_label.grid(row=0, column=2, padx=5)
timestamp_entry = ttk.Entry(filter_frame, width=20)
timestamp_entry.grid(row=0, column=3, padx=5)

# Кнопка "Применить фильтр"
apply_filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=update_logs)
apply_filter_button.grid(row=0, column=4, padx=5)

# Создание фрейма для таблицы и ползунка прокрутки
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)  # Использование fill и expand для заполнения доступного пространства

# Создание таблицы для отображения логов
table = ttk.Treeview(frame, columns=("ip_address", "timestamp", "status", "size", "referer", "user_agent"))
table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Использование fill и expand для заполнения доступного пространства

# Создание ползунка прокрутки
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=table.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Привязка ползунка прокрутки к таблице
table.configure(yscrollcommand=scrollbar.set)

# Установка заголовков столбцов
table.heading("ip_address", text="IP Address")
table.heading("timestamp", text="Timestamp")
table.heading("status", text="Status")
table.heading("size", text="Size")
table.heading("referer", text="Referer")
table.heading("user_agent", text="User Agent")

# Кнопка "Обновить"
update_button = tk.Button(root, text="Обновить", command=update_logs)

# Запуск основного цикла обработки событий tkinter
root.mainloop()

# Закрытие курсора и соединения с базой данных
cursor.close()
conn.close()


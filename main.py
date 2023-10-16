# Приложение "Список сотрудников для компании"
import tkinter as tk 
from tkinter import ttk
import sqlite3

# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
        
    # Хранение и создание виджетов
    def init_main(self):

        # Панель управления на которой располагаются виджеты
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка с картинкой "добавить"
        self.img_add = tk.PhotoImage(file='./img/add.png')
        but_add = tk.Button(toolbar, text='Добавить', bg='#d7d7d7', 
                            bd=0, image=self.img_add, command=self.open_child)

        # Кнопка с картинкой "изменить"
        self.update_image = tk.PhotoImage(file='./img/update.png')
        but_edit_dialog = tk.Button(toolbar, text='Изменить', bg='#d7d7d7', 
                                    bd=0, image=self.update_image, command=self.open_update_dialog)

        # Кнопка с картинкой "удалить"
        self.delete_image = tk.PhotoImage(file='./img/delete.png')
        but_delete = tk.Button(toolbar, text='Изменить', bg='#d7d7d7', 
                                    bd=0, image=self.delete_image, command=self.delete_records)
        
        # Кнопка с картинкой "поиск"
        self.search_image = tk.PhotoImage(file='./img/search.png')
        but_search = tk.Button(toolbar, text='Найти', bg='#d7d7d7', 
                                    bd=0, image=self.search_image, command=self.open_search)

        # Кнопка с картинкой "обновить"
        self.refresh_image = tk.PhotoImage(file='./img/refresh.png')
        but_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d7d7', 
                                    bd=0, image=self.refresh_image, command=self.view_records)

        but_add.pack(side=tk.LEFT)
        but_edit_dialog.pack(side=tk.LEFT)
        but_delete.pack(side=tk.LEFT)
        but_search.pack(side=tk.LEFT)
        but_refresh.pack(side=tk.LEFT)


        # Столбцы с данными
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email', 'salary'),
                                 height=45, show='headings')
        
        # Размеры столбцов
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=150, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        # Названия столбцов
        self.tree.heading('ID', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')
        self.tree.pack(side=tk.LEFT)

        # Ползунок
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод добавления данных
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # Обновление (изменение) данных
    def update_records(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''UPDATE users SET name=?, phone=?, email=?, salary=? WHERE ID=?''',
                            (name, phone, email, salary, id))               
        self.db.con.commit()
        self.view_records()

    # вывод данных в виджет таблицы
    def view_records(self):
        self.db.cur.execute('''SELECT * FROM users''')

        # Удалить все из виджета
        [self.tree.delete(i) for i in self.tree.get_children()]

        # Добавляем в таблицу все данные из БД
        [self.tree.insert('', 'end', values=row)
        for row in self.db.cur.fetchall()]

    # Удаление записей
    def delete_records(self):
        # Цикл по выделенным записям
        for selection_item in self.tree.selection():
            # удаляем из дб
            self.db.cur.execute('''DELETE FROM users WHERE ID=?''',
                                (self.tree.set(selection_item, '#1'), ))
        self.db.con.commit()
        self.view_records()

    # Поиск контакта
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute('''SELECT * FROM users WHERE name LIKE ?''', (name, ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
        for row in self.db.cur.fetchall()]



    # Метод вызывающий дочернее окно
    def open_child(self):
        Child()

    # Метод вызывающий окно изменения данных
    def open_update_dialog(self):
        Update()
    
    # Метод вызывающий окно поиска
    def open_search(self):
        Search()

# Класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app


    # Инициализация виджетов дочернего класса
    def init_child(self):
        self.title('Добавление сотрудника')
        self.geometry('400x220')
        self.resizable(False,False)
        self.grab_set()
        self.focus_set()

        # Текстовые поля 
        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=50, y=30)

        label_phone = tk.Label(self, text='Телефон: ')
        label_phone.place(x=50, y=60)

        label_email = tk.Label(self, text='E-mail: ')
        label_email.place(x=50, y=90)

        label_salary = tk.Label(self, text='Зарплата: ')
        label_salary.place(x=50, y=120)

        # Строки для ввода
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=30)

        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=60)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=90)
        
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=120)

        # Кнопка закрытия дочернего окна
        self.but_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.but_cancel.place(x=200, y=150)

        # Кнопка добавления нового пользователя
        self.but_add2 = tk.Button(self, text='Добавить')
        self.but_add2.place(x=265, y=150)
        self.but_add2.bind('<Button-1>', lambda event:
                     self.view.records(self.entry_name.get(),
                                       self.entry_phone.get(),
                                       self.entry_email.get(),
                                       self.entry_salary.get()))

# Класс окна обновления, наследуемый от класса дочернего окна
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.db = db  
        self.view = app
        self.deafult_data()

    def init_edit(self):
        self.title ('Редактировать позицию ')
        self.but_add2.destroy()

        self.but_edit = tk.Button(self, text='Редактировать', bg='#d7d7d7')
        self.but_edit.place(x=265, y=150)
        self.but_edit.bind('<Button-1>', lambda event:
                     self.view.update_records(self.entry_name.get(),
                                              self.entry_phone.get(),
                                              self.entry_email.get(),
                                              self.entry_salary.get()))
        self.but_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        
    def deafult_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('''SELECT * FROM users   WHERE ID=?''', (id, ))

        # Получаем доступ к первой записи из выборки
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

# Класс для поиска контакта
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
    def init_child(self):
        self.title('Поиск сотрудника')
        self.geometry('300x100')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=20, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=70, y=20)

        self.but_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.but_cancel.place(x=200, y=70)

        self.but_add2 = tk.Button(self, text='Найти')
        self.but_add2.place(x=150, y=70)
        self.but_add2.bind('<Button-1>', lambda event: self.view.search_records(self.entry_name.get()))

# Класс БД
class DB:
    def __init__(self):
        # Соединение с БД
        self.con = sqlite3.connect('staff.db')
        self.cur = self.con.cursor()
        self.cur.execute('''
                        CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        phone TEXT,
                        email TEXT,
                        salary TEXT)   
                                ''')
        self.con.commit()

    def insert_data(self, name, phone, email, salary):
        self.cur.execute(''' INSERT INTO users(name, phone, email, salary)
                            VALUES(?, ?, ?, ?)''',(name, phone, email, salary))
        self.con.commit()



# При запуске программы
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('645x450')
    root.config(bg='white')
    root.resizable(False, False)
    root.mainloop()



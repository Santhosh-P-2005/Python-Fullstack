import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Database setup
def init_db():
    conn = sqlite3.connect('dress_management.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS dresses
                      (id INTEGER PRIMARY KEY, name TEXT, size TEXT, color TEXT, price REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()


# User Authentication
def register_user(username, password):
    conn = sqlite3.connect('dress_management.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo('Success', 'User registered successfully!')
    except sqlite3.IntegrityError:
        messagebox.showerror('Error', 'Username already exists!')
    conn.close()


def authenticate_user(username, password):
    conn = sqlite3.connect('dress_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user


# CRUD operations
def add_dress(name, size, color, price):
    conn = sqlite3.connect('dress_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO dresses (name, size, color, price) VALUES (?, ?, ?, ?)',
                   (name, size, color, price))
    conn.commit()
    conn.close()
    messagebox.showinfo('Success', 'Dress added successfully!')


def get_all_dresses():
    conn = sqlite3.connect('dress_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dresses')
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_dress(dress_id, name, size, color, price):
    conn = sqlite3.connect('dress_management.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE dresses SET name=?, size=?, color=?, price=? WHERE id=?',
                   (name, size, color, price, dress_id))
    conn.commit()
    conn.close()
    messagebox.showinfo('Success', 'Dress updated successfully!')


def delete_dress(dress_id):
    conn = sqlite3.connect('dress_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM dresses WHERE id=?', (dress_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo('Success', 'Dress deleted successfully!')


# GUI
class DressManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Dress Management System')
        self.root.geometry('800x600')
        self.root.configure(bg='#f0f0f0')

        self.name_var = tk.StringVar()
        self.size_var = tk.StringVar()
        self.color_var = tk.StringVar()
        self.price_var = tk.DoubleVar()
        self.selected_dress_id = None

        self.login_window()

        self.fullscreen = False
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)

    def login_window(self):
        self.clear_window()

        login_frame = tk.Frame(self.root, bg='#4a90e2', padx=20, pady=20)
        login_frame.pack(expand=True)

        tk.Label(login_frame, text="Login", font=('Arial', 16, 'bold'), bg='#4a90e2', fg='white').pack(pady=20)

        tk.Label(login_frame, text="Username", font=('Arial', 12), bg='#4a90e2', fg='white').pack(pady=5)
        self.login_username_var = tk.StringVar()
        tk.Entry(login_frame, textvariable=self.login_username_var, font=('Arial', 12), width=30).pack(pady=5)

        tk.Label(login_frame, text="Password", font=('Arial', 12), bg='#4a90e2', fg='white').pack(pady=5)
        self.login_password_var = tk.StringVar()
        tk.Entry(login_frame, textvariable=self.login_password_var, font=('Arial', 12), show='*', width=30).pack(pady=5)

        tk.Button(login_frame, text="Login", command=self.login, font=('Arial', 12), bg='#34c759', fg='white').pack(
            pady=20)
        tk.Button(login_frame, text="Register", command=self.register_window, font=('Arial', 12), bg='#ff9500',
                  fg='white').pack()

    def register_window(self):
        self.clear_window()

        register_frame = tk.Frame(self.root, bg='#4a90e2', padx=20, pady=20)
        register_frame.pack(expand=True)

        tk.Label(register_frame, text="Register", font=('Arial', 16, 'bold'), bg='#4a90e2', fg='white').pack(pady=20)

        tk.Label(register_frame, text="Username", font=('Arial', 12), bg='#4a90e2', fg='white').pack(pady=5)
        self.register_username_var = tk.StringVar()
        tk.Entry(register_frame, textvariable=self.register_username_var, font=('Arial', 12), width=30).pack(pady=5)

        tk.Label(register_frame, text="Password", font=('Arial', 12), bg='#4a90e2', fg='white').pack(pady=5)
        self.register_password_var = tk.StringVar()
        tk.Entry(register_frame, textvariable=self.register_password_var, font=('Arial', 12), show='*', width=30).pack(
            pady=5)

        tk.Button(register_frame, text="Register", command=self.register, font=('Arial', 12), bg='#34c759',
                  fg='white').pack(pady=20)
        tk.Button(register_frame, text="Back to Login", command=self.login_window, font=('Arial', 12), bg='#ff9500',
                  fg='white').pack()

    def login(self):
        username = self.login_username_var.get()
        password = self.login_password_var.get()
        if authenticate_user(username, password):
            self.setup_main_gui()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.register_username_var.get()
        password = self.register_password_var.get()
        if username and password:
            register_user(username, password)
            self.login_window()
        else:
            messagebox.showwarning("Input Error", "All fields are required!")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_main_gui(self):
        self.clear_window()

        # Menu Bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Fullscreen (F11)", command=self.toggle_fullscreen)
        file_menu.add_command(label="Exit Fullscreen (Esc)", command=self.exit_fullscreen)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.login_window)
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Main Frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=10, pady=10)
        main_frame.pack(fill='both', expand=True)

        # Form Frame
        form_frame = tk.Frame(main_frame, bg='#f0f0f0')
        form_frame.grid(row=0, column=0, pady=10)

        tk.Label(form_frame, text='Name', bg='#f0f0f0', font=('Arial', 12)).grid(row=0, column=0, sticky='w', pady=5)
        tk.Entry(form_frame, textvariable=self.name_var, font=('Arial', 12), width=30).grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text='Size', bg='#f0f0f0', font=('Arial', 12)).grid(row=1, column=0, sticky='w', pady=5)
        tk.Entry(form_frame, textvariable=self.size_var, font=('Arial', 12), width=30).grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text='Color', bg='#f0f0f0', font=('Arial', 12)).grid(row=2, column=0, sticky='w', pady=5)
        tk.Entry(form_frame, textvariable=self.color_var, font=('Arial', 12), width=30).grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text='Price', bg='#f0f0f0', font=('Arial', 12)).grid(row=3, column=0, sticky='w', pady=5)
        tk.Entry(form_frame, textvariable=self.price_var, font=('Arial', 12), width=30).grid(row=3, column=1, pady=5)

        # Button Frame
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.grid(row=1, column=0, pady=10)

        tk.Button(button_frame, text='Add Dress', command=self.add_dress, bg='#4caf50', fg='white',
                  font=('Arial', 12)).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text='Update Dress', command=self.update_dress, bg='#2196f3', fg='white',
                  font=('Arial', 12)).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text='Delete Dress', command=self.delete_dress, bg='#f44336', fg='white',
                  font=('Arial', 12)).grid(row=0, column=2, padx=5)

        # Treeview Frame
        tree_frame = tk.Frame(main_frame, bg='#f0f0f0')
        tree_frame.grid(row=2, column=0, pady=10, sticky='nsew')
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Treeview for dress list
        columns = ('ID', 'Name', 'Size', 'Color', 'Price')
        self.dress_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', style='mystyle.Treeview')
        self.dress_tree.heading('ID', text='ID')
        self.dress_tree.heading('Name', text='Name')
        self.dress_tree.heading('Size', text='Size')
        self.dress_tree.heading('Color', text='Color')
        self.dress_tree.heading('Price', text='Price')
        self.dress_tree.column('ID', width=50)
        self.dress_tree.column('Name', width=150)
        self.dress_tree.column('Size', width=50)
        self.dress_tree.column('Color', width=100)
        self.dress_tree.column('Price', width=70)
        self.dress_tree.grid(row=0, column=0, sticky='nsew')
        self.dress_tree.bind('<<TreeviewSelect>>', self.on_select)

        # Scrollbars for Treeview
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.dress_tree.xview)
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient='vertical', command=self.dress_tree.yview)
        self.dress_tree.configure(xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set)
        tree_scroll_x.grid(row=1, column=0, sticky='ew')
        tree_scroll_y.grid(row=0, column=1, sticky='ns')

        self.load_dresses()

    def add_dress(self):
        name = self.name_var.get()
        size = self.size_var.get()
        color = self.color_var.get()
        price = self.price_var.get()
        if name and size and color and price:
            add_dress(name, size, color, price)
            self.load_dresses()
            self.clear_fields()
        else:
            messagebox.showwarning('Input Error', 'All fields are required!')

    def load_dresses(self):
        for row in self.dress_tree.get_children():
            self.dress_tree.delete(row)
        for dress in get_all_dresses():
            self.dress_tree.insert('', 'end', values=dress)

    def on_select(self, event):
        selected_item = self.dress_tree.selection()[0]
        selected_dress = self.dress_tree.item(selected_item, 'values')
        self.selected_dress_id = int(selected_dress[0])
        self.name_var.set(selected_dress[1])
        self.size_var.set(selected_dress[2])
        self.color_var.set(selected_dress[3])
        self.price_var.set(selected_dress[4])

    def update_dress(self):
        if self.selected_dress_id is None:
            messagebox.showwarning('Selection Error', 'No dress selected!')
            return
        name = self.name_var.get()
        size = self.size_var.get()
        color = self.color_var.get()
        price = self.price_var.get()
        if name and size and color and price:
            update_dress(self.selected_dress_id, name, size, color, price)
            self.load_dresses()
            self.clear_fields()
        else:
            messagebox.showwarning('Input Error', 'All fields are required!')

    def delete_dress(self):
        if self.selected_dress_id is None:
            messagebox.showwarning('Selection Error', 'No dress selected!')
            return
        delete_dress(self.selected_dress_id)
        self.load_dresses()
        self.clear_fields()
        self.selected_dress_id = None

    def clear_fields(self):
        self.name_var.set('')
        self.size_var.set('')
        self.color_var.set('')
        self.price_var.set('')

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes('-fullscreen', False)


if __name__ == '__main__':
    init_db()
    root = tk.Tk()

    # Styling
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#ccc")
    style.configure("TLabel", background="#f0f0f0")
    style.configure("TFrame", background="#f0f0f0")
    style.configure('Treeview.Heading', font=('Arial', 12, 'bold'), background='#f0f0f0')
    style.configure('Treeview', rowheight=25)
    style.map("TButton",
              foreground=[('active', 'white')],
              background=[('active', 'blue')])

    app = DressManagementApp(root)
    root.mainloop()

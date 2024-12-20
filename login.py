import tkinter.messagebox as messagebox
import tkinter as tk
import sqlite3

from utilities import HoverPlaceholderEntry
from utilities_new import resource_path, center_window
from main import MainPage
from register import RegisterPage
from controller import GetUserInfo

class LoginPage:
    def __init__(self, master, switch_to_main):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        center_window(self.root, 300, 240) # 让窗口出现在屏幕中央
        self.root.minsize(width = 250, height = 240)
        self.root.title('登陆')
        self.root.iconbitmap(resource_path("images/configs/diamond.ico"))
        self.register_frame = RegisterPage(self.root, self.show_login_frame)
        self.switch_to_main = switch_to_main

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.user_type = None

        # 登录错误信息标签
        self.username_error_label = tk.Label(self.page, text='', fg='red')
        self.username_error_label.grid(row=2, column=1, sticky=tk.W, pady=(0, 5))
        self.password_error_label = tk.Label(self.page, text='', fg='red')
        self.password_error_label.grid(row=4, column=1, sticky=tk.W, pady=(0, 5))

        # 登录界面标签
        tk.Label(self.page).grid(row=0, column=0)
        tk.Label(self.page, text='用户名').grid(row=1, column=0, sticky=tk.E, pady=(10, 0))
        self.username_entry = HoverPlaceholderEntry(self.page, "请输入用户名", is_password=False, textvariable=self.username)
        self.username_entry.grid(row=1, column=1, sticky=tk.E,  pady=(10, 0))
        tk.Label(self.page, text='密码').grid(row=3, column=0, sticky=tk.E, pady=(5, 0))
        self.password_entry = HoverPlaceholderEntry(self.page, "请输入密码", is_password=True, textvariable=self.password)
        self.password_entry.grid(row=3, column=1, sticky=tk.E,  pady=(5, 0))

        tk.Button(self.page, text='登录', command=self.login_check).grid(row=5, column=1, sticky=tk.E, pady=(0, 0))
        self.root.bind("<Return>", self.login_check)
        tk.Button(self.page, text='注册', command=self.show_register).grid(row=5, column=0, sticky=tk.W, pady=(0, 0))


    def show_register(self):
        self.clear_login_fields()
        self.page.pack_forget()
        self.root.title('注册')
        self.register_frame.pack()

    def show_login_frame(self):
        self.register_frame.pack_forget()
        self.root.title('登录')
        self.page.pack()

    def clear_login_fields(self):
        self.username_error_label.config(text='')
        self.password_error_label.config(text='')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.username_entry.reset_entry(event=None)
        self.password_entry.reset_entry(event=None)

    def login_check(self, event=None):
        username = self.username.get().strip()
        password = self.password.get().strip()

        self.username_error_label.config(text='')
        self.password_error_label.config(text='')

        if not username:
            self.username_error_label.config(text='请输入用户名')
        if not password:
            self.password_error_label.config(text='请输入密码')
        if username and password:
            connection = sqlite3.connect(resource_path('databases/database.db'))
            cursor = connection.cursor()
            cursor.execute("SELECT password, type FROM users WHERE username=?", (username,))
            res = cursor.fetchone()
            if not res:
                messagebox.showinfo(title='提示信息', message='用户名不存在')
                return
            user_password, user_type = res

            if user_password is None or user_password != password:
                messagebox.showinfo(title='提示信息', message='密码错误')
            elif user_type == '申请中':
                messagebox.showinfo(title='提示信息', message='账号正在申请，请等待管理员确认')
            else:
                get_user_type_instance = GetUserInfo.get_instance()
                get_user_type_instance.usertype = user_type
                get_user_type_instance.username = username
                messagebox.showinfo(title='提示信息', message='登录成功！')
                self.clear_login_fields()
                self.switch_to_main(username)

            connection.close()

class Controller:
    def __init__(self, root):
        self.root = root
        self.main_window = None
        self.login_window = None
        self.switch_to_login()

    def switch_to_login(self):
        if self.main_window:
            self.main_window.root.withdraw()
        self.login_window = LoginPage(self.root, self.switch_to_main)
        self.login_window.root.deiconify()

    def switch_to_main(self, username):
        if self.login_window:
            self.login_window.page.pack_forget()
            self.login_window.root.withdraw()
        self.main_window = MainPage(self.root, username, self.switch_to_login)
        self.main_window.root.deiconify()

if __name__ == '__main__':
    root = tk.Tk()
    controller = Controller(root)
    root.mainloop()
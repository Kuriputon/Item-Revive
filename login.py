import tkinter as tk
import tkinter.messagebox as messagebox

from utilities import *
from main import MainPage
from register import RegisterPage
from item_detail import *

class LoginPage:
    def __init__(self, master):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        center_window(self.root, 300, 240) # 让窗口出现在屏幕中央
        self.root.minsize(width = 250, height = 240)
        self.root.title('登陆')
        self.root.iconbitmap(resource_path("images/configs/diamond.ico"))
        self.register_frame = RegisterPage(self.root, self.show_login_frame)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.user_type = None


        # 登录错误信息标签
        self.username_error_label = tk.Label(self.page, text='', fg='red')
        self.username_error_label.grid(row=2, column=1, sticky=tk.W, pady=(0, 5))
        self.password_error_label = tk.Label(self.page, text='', fg='red')
        self.password_error_label.grid(row=4, column=1, sticky=tk.W, pady=(0, 5))

        # # 游客登录标签，仅开发测试方便用
        # self.problem_label = tk.Label(self.page, text='游客登录', fg='gray', cursor='hand2', justify='center',
        #                               anchor='center')
        # self.problem_label.grid(row=7, column=1, sticky=tk.NSEW, padx=(0, 30), pady=(10, 10))
        # self.problem_label.bind("<Button-1>", self.guest_login)
        # self.problem_label.config(font=("Arial", 10, "underline"))


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


    def guest_login(self, event):
        username = None
        self.open_main_page(username)

    def user_login(self):
        username = self.username.get()
        self.open_main_page(username)

    def open_main_page(self, username):
        self.clear_login_fields()
        if not username:
            self.root.withdraw()
            self.main_page = MainPage(self.root, username)
        else:
            username = username
            self.root.withdraw()
            self.main_page = MainPage(self.root, username)


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
            connection = sqlite3.connect(resource_path('databases/users.db'))
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM users WHERE username=?", (username,))
            result = cursor.fetchone()

            if result is None or result[0] != password:
                messagebox.showinfo(title='提示信息', message='用户名或密码错误')
            else:
                messagebox.showinfo(title='提示信息', message='登录成功！')
                self.user_login()

            connection.close()



if __name__ == '__main__':
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()
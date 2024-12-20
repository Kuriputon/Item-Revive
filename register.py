import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3
from tkinter import ttk
from utilities import HoverPlaceholderEntry, resource_path

class RegisterPage(tk.Frame):
    def __init__(self, master, show_login_frame):
        super().__init__(master)
        super().__init__(master)

        self.root = master
        self.show_login_frame = show_login_frame

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.contact_info = tk.StringVar()

        tip_font_style = ttk.Style()
        tip_font_style.theme_use('default')
        tip_font_style.configure('TipFont.TLabel', font=('方正小标宋_GBK', 9), foreground='red', background='#f0f0f0')

        username_frame = tk.Frame(self)
        password_frame = tk.Frame(self)
        contact_info_frame = tk.Frame(self)

        username_tip_frame = tk.Frame(self)
        password_tip_frame = tk.Frame(self)
        contact_info_tip_frame = tk.Frame(self)


        tk.Label(username_frame, text='用户名').pack(side='left',  anchor='nw', padx=(20, 0), pady=(0, 0))
        self.username_entry = HoverPlaceholderEntry(username_frame, "请输入用户名", is_password=False, textvariable=self.username)
        self.username_entry.pack(side='left', anchor='w', padx=(20, 0), pady=(1, 0))
        username_frame.pack(side='top', padx=(10, 10), pady=(20, 0))

        self.username_error_label = ttk.Label(username_tip_frame, text='', style='TipFont.TLabel')
        self.username_error_label.pack(side='left')
        username_tip_frame.pack(side='top', padx=(25, 10), pady=(0, 0))

        tk.Label(password_frame, text='密码').pack(side='left', anchor='nw', padx=(30, 0), pady=(1, 0))
        self.password_entry = HoverPlaceholderEntry(password_frame, "请输入密码", is_password=True, textvariable=self.password)
        self.password_entry.pack(side='left', anchor='w', padx=(22, 0), pady=(1, 0))
        password_frame.pack(side='top', padx=(10, 10), pady=(5, 0))

        self.password_error_label = ttk.Label(password_tip_frame, text='', style='TipFont.TLabel')
        self.password_error_label.pack(side='left')
        password_tip_frame.pack(side='top', padx=(10, 10), pady=(0, 0))

        tk.Label(contact_info_frame, text='联系方式').pack(side='left', anchor='nw', padx=(2, 0), pady=(1, 0))
        self.contact_info_entry = HoverPlaceholderEntry(contact_info_frame, "手机号\微信号\邮箱", is_password=False, textvariable=self.contact_info)
        self.contact_info_entry.pack(side='left', anchor='w', padx=(23, 0), pady=(1, 0))
        contact_info_frame.pack(side='top', padx=(10, 10), pady=(5, 0))

        self.contact_info_error_label = ttk.Label(contact_info_tip_frame, text='', style='TipFont.TLabel')
        self.contact_info_error_label.pack(side='left')
        contact_info_tip_frame.pack(side='top', padx=(25, 10), pady=(0, 0))

        button_frame = tk.Frame(self)
        self.return_button = tk.Button(button_frame, text='返回', command=self.show_login)
        self.return_button.pack(side='left', padx=(0, 20))
        self.register_button = tk.Button(button_frame, text='注册', command=self.register_check)
        self.register_button.pack(side='left', padx=(20, 0))
        button_frame.pack(side='top', padx=(10, 10), pady=(40, 0))



    def show_login(self):
        self.clear_register_fields()
        self.pack_forget()
        self.show_login_frame()

    def clear_register_fields(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.contact_info_entry.delete(0, 'end')
        self.username_error_label.config(text='')
        self.password_error_label.config(text='')
        self.contact_info_error_label.config(text='')
        self.username_entry.reset_entry(event=None)
        self.password_entry.reset_entry(event=None)
        self.contact_info_entry.reset_entry(event=None)

    def register_check(self):
        username = self.username.get().strip()
        password = self.password.get().strip()
        contact_info = self.contact_info.get().strip()

        self.username_error_label.config(text='')
        self.password_error_label.config(text='')
        self.contact_info_error_label.config(text='')

        if not username:
            self.username_error_label.config(text="请输入用户名")
        if not password:
            self.password_error_label.config(text="请输入密码")
        if not contact_info:
            self.contact_info_error_label.config(text="请输入联系方式")
        if username and password and contact_info:
            connection = sqlite3.connect(resource_path('databases/database.db'))
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
            if cursor.fetchone()[0] > 0:
                messagebox.showinfo(title='提示信息', message='用户名已存在')
                connection.close()
                return

            try:
                cursor.execute(
                    "INSERT INTO users (username, password, contact_info, type) VALUES (?, ?, ?, ?)",
                    (username, password, contact_info, "申请中")
                )
                connection.commit()
                connection.close()
                messagebox.showinfo(title='提示信息', message='注册成功，请等待管理员确认')
                self.show_login()

            except sqlite3.Error as e:
                print("Database error:", e)
                connection.close()



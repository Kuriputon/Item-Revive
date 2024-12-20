import tkinter as tk
import sqlite3

from tkinter import ttk, messagebox

from base_class import ManageFrame
from utilities import resource_path
from utilities_new import center_window

class ManageUserFrame(ManageFrame):   # 管理用户界面
    def __init__(self, master):
        super().__init__(master)
        tag_label = ttk.Label(self.title_frame, text='用户信息', style='ThemeFont.TLabel')
        tag_label.pack(side='left')

        # 功能按钮
        refresh_button = ttk.Button(self.title_frame, text="刷新数据", command=self.refresh, style='ButtonFont.TButton', takefocus=False)
        refresh_button.pack(side='left', padx=(20,10),pady=(0,0))
        authenticate_button = ttk.Button(self.title_frame, text="权限给与", command=self.authenticate, style='ButtonFont.TButton', takefocus=False)
        authenticate_button.pack(side='left', padx=(10,5),pady=(0,0))
        remove_button = ttk.Button(self.title_frame, text="权限移除", command=self.remove, style='ButtonFont.TButton', takefocus=False)
        remove_button.pack(side='left', padx=(10,5),pady=(0,0))
        affirm_button = ttk.Button(self.title_frame, text="通过申请", command=self.admit, style='ButtonFont.TButton', takefocus=False)
        affirm_button.pack(side='left', padx=(10,5),pady=(0,0))

        columns = ('name', 'contact_info', 'register_time', 'user_type')
        self.treeview = ttk.Treeview(self, show='headings', columns=columns)
        self.treeview.column('name', width=80, anchor='center')
        self.treeview.column('contact_info', width=120, anchor='center')
        self.treeview.column('register_time', width=120, anchor='center')
        self.treeview.column('user_type', width=80, anchor='center')
        self.treeview.heading('name', text='用户名')
        self.treeview.heading('contact_info', text='联络方式')
        self.treeview.heading('register_time', text='注册时间')
        self.treeview.heading('user_type', text='用户类别')
        self.treeview.pack(side='top', fill='both', expand=True)

        self.refresh()


    def refresh(self):
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query = '''
                    SELECT username, contact_info, registration_time, type
                    FROM users
                '''
        cur.execute(query)
        user_info = cur.fetchall()
        self.treeview.delete(*self.treeview.get_children())
        for _ in user_info:
            self.treeview.insert('', 'end', values=_)

    def authenticate(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("修改用户类别")
        center_window(dialog, 300, 150)

        label = tk.Label(dialog, text="请输入要授予管理员权限的用户名")
        label.pack(side='top', pady=10)

        username = tk.StringVar()
        username_entry = ttk.Entry(dialog, width=20, font=("Arial 16"), textvariable=username, takefocus=False)
        username_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)


        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm(username_entry.get(), dialog, 1))
        confirm_button.pack(side='left', padx=10, pady=10)

        button_frame.pack(side='top', padx=(10,10))

    def remove(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("撤销权限")
        center_window(dialog, 300, 150)

        label = tk.Label(dialog, text="请输入要撤销管理员权限的用户名")
        label.pack(side='top', pady=10)

        username = tk.StringVar()
        username_entry = ttk.Entry(dialog, width=20, font=("Arial 16"), textvariable=username, takefocus=False)
        username_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)

        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm(username_entry.get(), dialog, 0))
        confirm_button.pack(side='left', padx=10, pady=10)

        button_frame.pack(side='top', padx=(10, 10))

    def admit(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("通过注册申请")
        center_window(dialog, 300, 150)

        label = tk.Label(dialog, text="请输入要通过注册申请的用户名")
        label.pack(side='top', pady=10)

        username = tk.StringVar()
        username_entry = ttk.Entry(dialog, width=20, font=("Arial 16"), textvariable=username, takefocus=False)
        username_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)


        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm(username_entry.get(), dialog, 3))
        confirm_button.pack(side='left', padx=10, pady=10)
        button_frame.pack(side='top', padx=(10,10))

    def confirm(self, username, dialog, flag):
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        cur.execute('''SELECT count(*) FROM users WHERE username = ?''', (username,))
        cnt = cur.fetchone()[0]
        if cnt == 0:
            messagebox.showinfo("提示信息", "请输入正确的用户名")
            connection.close()
            return
        cur.execute('''SELECT type FROM users WHERE username = ?''', (username,))
        usertype = cur.fetchone()[0]
        if flag == 1:
            if usertype == '管理员':
                messagebox.showinfo('提示信息', '该用户已经是管理员')
                return
            confirm = messagebox.askyesno('确认授权', f'您确定要将管理员权限授给 {username} 吗？')
            if confirm:
                cur.execute('''UPDATE users SET type = '管理员' WHERE username = ?''', (username,))
                connection.commit()
                messagebox.showinfo("提交成功", "已将管理员权限授权给 "+ username)
                connection.close()
        elif flag == 0:
            if usertype != '管理员':
                messagebox.showinfo('提示信息', '该用户不是管理员')
                return
            confirm = messagebox.askyesno('确认收回权限', f'您确定要将{username}的管理员权限收回吗？')
            if confirm:
                cur.execute('''UPDATE users SET type = '普通用户' WHERE username = ?''', (username,))
                connection.commit()
                messagebox.showinfo("提交成功", "已将 "+username+" 的管理员权限收回")
                connection.close()
        elif flag == 3:
            if usertype != '申请中':
                messagebox.showinfo('提示信息', '该用户已经是正式用户')
                return
            confirm = messagebox.askyesno('确认通过', f'您确定要通过{username}的注册申请吗？')
            if confirm:
                cur.execute('''UPDATE users SET type = '普通用户' WHERE username = ?''', (username,))
                connection.commit()
                messagebox.showinfo("提交成功", "已通过 "+username+" 的注册申请")
                connection.close()
        dialog.destroy()
        self.refresh()







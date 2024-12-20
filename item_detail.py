import sqlite3
import tkinter as tk

from datetime import datetime
from tkinter import ttk, messagebox
from base_class import DetailFrame
from controller import GetUserInfo
from utilities_new import resource_path, center_window


class AvailableItemDetailFrame(DetailFrame):
    def __init__(self, master, item_id, name, category, description, image_path, upload_time, uploaded_by, price):
        super().__init__(master, item_id, name, category, description, image_path, upload_time, uploaded_by, price)

        self.submit_button_frame = tk.Frame(self.attributes_frame)
        self.submit_button = ttk.Button(self.submit_button_frame, text="我想要", style='ButtonFont.TButton', takefocus=False)
        self.submit_button.config(command=lambda: self.i_want_item(self.uploaded_by))
        self.submit_button.pack(side='top', padx=(20, 0), pady=(0, 0))
        self.submit_button_frame.pack(side='top', padx=(10,0), pady=(35,10))
        self.attributes_frame.pack(side='left', padx=(40, 10), pady=(50, 10))

    def i_want_item(self, uploaded_by):
        get_user_type_instance = GetUserInfo.get_instance()
        username = get_user_type_instance.username
        if uploaded_by == username:
            messagebox.showinfo(title='提示信息', message='不能对自己发布的物品发起交易请求')
            return

        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query1 = '''SELECT count(*) FROM quests WHERE activator_name = ? AND receiver_name = ? AND item_name = ? AND item_id = ?'''
        cur.execute(query1, (username, uploaded_by, self.name, self.item_id))
        cnt = cur.fetchone()[0]
        if cnt:
            messagebox.showinfo(title='提示信息', message='已对该物品发起过交易请求')
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("提示")
        center_window(dialog, 500, 200)

        label = ttk.Label(dialog, text="您确定想要此物品吗？如果需要的话，请写下该请求的备注\n\n按下确定后，你和对方将能看到彼此的联系方式", style='NormalFont.TLabel')
        label.pack(side='top', pady=10)

        note = tk.StringVar()
        note_entry = ttk.Entry(dialog, width=40, font="Arial 11", textvariable=note, takefocus=False)
        note_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)

        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm(dialog, uploaded_by, note_entry.get()))
        confirm_button.pack(side='left', padx=10, pady=10)
        button_frame.pack(side='top', padx=(10, 10))

    def confirm(self, dialog, uploaded_by, note):
        dialog.destroy()
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query1 = '''SELECT contact_info FROM users WHERE username = ?'''
        cur.execute(query1, (uploaded_by, ))
        receiver_contact_info = cur.fetchone()[0]

        get_user_type_instance = GetUserInfo.get_instance()
        activator_name = get_user_type_instance.username

        query2 = '''SELECT contact_info FROM users WHERE username = ?'''
        cur.execute(query2, (activator_name, ))
        activator_contact_info = cur.fetchone()[0]

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        query3 = '''INSERT INTO quests (item_name, item_id, activator_name, receiver_name, activator_contact_info, receiver_contact_info, quest_type, create_time, quest_status, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cur.execute(query3, (self.name, self.item_id, activator_name, uploaded_by, activator_contact_info, receiver_contact_info, "想要", timestamp, "申请中", note))
        connection.commit()
        dialog = tk.Toplevel(self.root)
        dialog.title("提示")
        center_window(dialog, 400, 150)

        label = ttk.Label(dialog, text="对方的联络方式是：\n\n" + receiver_contact_info + "\n\n请尽快与对方联系", style='NormalFont.TLabel')
        label.pack(side='top', pady=10)

class WantingItemDetailFrame(DetailFrame):
    def __init__(self, master, item_id, name, category, description, image_path, upload_time, uploaded_by, price):
        super().__init__(master, item_id, name, category, description, image_path, upload_time, uploaded_by, price)

        self.submit_button_frame = tk.Frame(self.attributes_frame)
        self.submit_button = ttk.Button(self.submit_button_frame, text="我有", style='ButtonFont.TButton', takefocus=False)
        self.submit_button.config(command=lambda: self.i_have_item(self.uploaded_by))
        self.submit_button.pack(side='top', padx=(20, 0), pady=(0, 0))
        self.submit_button_frame.pack(side='top', padx=(10,0), pady=(35,10))
        self.attributes_frame.pack(side='left', padx=(40, 10), pady=(50, 10))

    def i_have_item(self, uploaded_by):
        get_user_type_instance = GetUserInfo.get_instance()
        username = get_user_type_instance.username
        if uploaded_by == username:
            messagebox.showinfo(title='提示信息', message='不能对自己发布的物品发起交易请求')
            return
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query1 = '''SELECT count(*) FROM quests WHERE activator_name = ? AND receiver_name = ? AND item_name = ? AND item_id = ?'''
        cur.execute(query1, (username, uploaded_by, self.name, self.item_id))
        cnt = cur.fetchone()[0]
        if cnt:
            messagebox.showinfo(title='提示信息', message='已对该物品发起过交易请求')
            return
        dialog = tk.Toplevel(self.root)
        dialog.title("提示")
        center_window(dialog, 500, 200)

        label = ttk.Label(dialog, text="您确定有此物品吗？如果需要的话，请写下交易备注\n按下确定后，你和对方将能看到彼此的联系方式", style='NormalFont.TLabel')
        label.pack(side='top', pady=5)

        note = tk.StringVar()
        note_entry = ttk.Entry(dialog, width=40, font=("Arial 11"), textvariable=note, takefocus=False)
        note_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)

        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm(dialog, note_entry.get(), uploaded_by))
        confirm_button.pack(side='left', padx=10, pady=10)
        button_frame.pack(side='top', padx=(10, 10))

    def confirm(self, dialog, note, uploaded_by):
        dialog.destroy()
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query1 = '''SELECT contact_info FROM users WHERE username = ?'''
        cur.execute(query1, (uploaded_by, ))
        receiver_contact_info = cur.fetchone()[0]

        get_user_type_instance = GetUserInfo.get_instance()
        activator_name = get_user_type_instance.username

        query2 = '''SELECT contact_info FROM users WHERE username = ?'''
        cur.execute(query2, (activator_name, ))
        activator_contact_info = cur.fetchone()[0]

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        query3 = '''INSERT INTO quests (item_name, item_id, activator_name, receiver_name, activator_contact_info, receiver_contact_info, quest_type, create_time, quest_status, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cur.execute(query3, (self.name, self.item_id, activator_name, uploaded_by, activator_contact_info, receiver_contact_info, "我有", timestamp, "申请中", note))
        connection.commit()

        dialog = tk.Toplevel(self.root)
        dialog.title("提示")
        center_window(dialog, 400, 150)

        label = ttk.Label(dialog, text="对方的联络方式是：\n\n" + receiver_contact_info + "\n\n请尽快与对方联系", style='NormalFont.TLabel')
        label.pack(side='top', pady=10)

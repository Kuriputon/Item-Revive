import tkinter as tk
import sqlite3
from datetime import datetime

from tkinter import ttk, messagebox

from base_class import ManageFrame
from utilities import resource_path
from utilities_new import center_window


class ManageReceivedQuestsFrame(ManageFrame):  # 管理我收到的物品交易请求界面
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username

        tag_label = ttk.Label(self.title_frame, text='我收到的交易请求', style='ThemeFont.TLabel')
        tag_label.pack(side='left')

        # 功能按钮
        refresh_button = ttk.Button(self.title_frame, text="刷新数据", command=self.refresh, style='ButtonFont.TButton', takefocus=False)
        refresh_button.pack(side='left', padx=(20, 10), pady=(0, 0))
        accept_button = ttk.Button(self.title_frame, text="通过请求", command=self.accept, style='ButtonFont.TButton', takefocus=False)
        accept_button.pack(side='left', padx=(10, 5), pady=(0, 0))
        decline_button = ttk.Button(self.title_frame, text="拒绝请求", command=self.decline, style='ButtonFont.TButton',
                                   takefocus=False)
        decline_button.pack(side='left', padx=(10, 5), pady=(0, 0))
        remove_button = ttk.Button(self.title_frame, text="删除记录", command=self.remove, style='ButtonFont.TButton',
                                   takefocus=False)
        remove_button.pack(side='left', padx=(10, 5), pady=(0, 0))

        columns = ('id', 'item', 'name', 'contact_info', 'create_time', 'quest_type', 'note', 'quest_status')
        self.treeview = ttk.Treeview(self, show='headings', columns=columns)
        self.treeview.column('id', width=20, anchor='center')
        self.treeview.column('item', width=100, anchor='center')
        self.treeview.column('name', width=80, anchor='center')
        self.treeview.column('contact_info', width=120, anchor='center')
        self.treeview.column('create_time', width=100, anchor='center')
        self.treeview.column('quest_type', width=40, anchor='center')
        self.treeview.column('note', width=150, anchor='center')
        self.treeview.column('quest_status', width=30, anchor='center')

        self.treeview.heading('id', text='id')
        self.treeview.heading('item', text='物品名称')
        self.treeview.heading('name', text='用户名')
        self.treeview.heading('contact_info', text='联络方式')
        self.treeview.heading('create_time', text='发出时间')
        self.treeview.heading('quest_type', text='请求类型')
        self.treeview.heading('note', text='备注')
        self.treeview.heading('quest_status', text='请求状态')
        self.treeview.pack(side='top', fill='both', expand=True)

        self.refresh()

    def refresh(self):
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query = '''
                    SELECT id, item_name, activator_name, activator_contact_info, create_time, quest_type, note, quest_status
                    FROM quests
                    WHERE receiver_name = ?
                '''
        cur.execute(query, (self.username, ))
        quest_info = cur.fetchall()
        new_info = []
        for info in quest_info:
            info = list(info)
            dt = datetime.strptime(str(info[4]), "%Y%m%d%H%M%S")
            info[4] = dt.strftime("%Y.%m.%d %H:%M")
            new_info.append(info)
        self.treeview.delete(*self.treeview.get_children())
        for _ in new_info:
            self.treeview.insert('', 'end', values=_)

    def accept(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("通过请求")
        center_window(dialog, 300, 150)

        label = ttk.Label(dialog, text="请输入要通过的请求id", style='NormalFont.TLabel')
        label.pack(side='top', pady=10)

        tar_id = tk.StringVar()
        id_entry = ttk.Entry(dialog, width=20, font="Arial 16", textvariable=tar_id, takefocus=False)
        id_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)

        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm(id_entry.get(), dialog, 1))
        confirm_button.pack(side='left', padx=10, pady=10)
        button_frame.pack(side='top', padx=(10, 10))

    def decline(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("拒绝请求")
        center_window(dialog, 300, 150)

        label = ttk.Label(dialog, text="请输入要拒绝的请求id", style='NormalFont.TLabel')
        label.pack(side='top', pady=10)

        quest_id = tk.StringVar()
        id_entry = ttk.Entry(dialog, width=20, font="Arial 16", textvariable=quest_id, takefocus=False)
        id_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)

        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm(id_entry.get(), dialog, 0))
        confirm_button.pack(side='left', padx=10, pady=10)
        button_frame.pack(side='top', padx=(10, 10))

    def remove(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("删除请求记录")
        center_window(dialog, 300, 150)

        label = ttk.Label(dialog, text="请输入要删除的请求记录id\n\n只能删除已通过或已拒绝的请求记录", style='NormalFont.TLabel')
        label.pack(side='top', pady=10)

        quest_id = tk.StringVar()
        id_entry = ttk.Entry(dialog, width=20, font="Arial 16", textvariable=quest_id, takefocus=False)
        id_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)

        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm(id_entry.get(), dialog, 2))
        confirm_button.pack(side='left', padx=10, pady=10)

        button_frame.pack(side='top', padx=(10, 10))

    def confirm(self, quest_id, dialog, flag):
        quest_id = int(quest_id)
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query = '''
                    SELECT id FROM quests WHERE receiver_name = ?
                '''
        cur.execute(query, (self.username,))
        ids = cur.fetchall()
        id_list = []
        for _ in ids:
            id_list.append(_[0])
        if quest_id not in id_list:
            messagebox.showwarning("提示信息", "请输入有效的请求id")
            return
        cur.execute('''SELECT quest_status FROM quests WHERE id = ?''', (quest_id,))
        quest_status = cur.fetchone()[0]
        if flag == 1:
            if quest_status == '已通过':
                messagebox.showinfo("提示信息", "该请求已通过，不能再通过")
                return
            elif quest_status == '已拒绝':
                messagebox.showinfo("提示信息", "该请求已拒绝，不能再通过")
                return
            confirm = messagebox.askyesno("确认请求", "您确定要通过该请求吗？通过后，相应物品会自动下架\n\n请确认您已给出/收到相应物品")
            if confirm:
                cur.execute("SELECT item_id FROM quests WHERE id = ?", (quest_id,))
                item_id = cur.fetchone()[0]
                cur.execute("SELECT status FROM items WHERE id = ?", (item_id,))
                item_status = cur.fetchone()[0]
                if item_status == '闲置中':
                    cur.execute("UPDATE items SET status = '已出' WHERE id = ?", (item_id,))
                elif item_status == '求物中':
                    cur.execute("UPDATE items SET status = '已得' WHERE id = ?", (item_id,))
                cur.execute("UPDATE quests SET quest_status = '已通过' WHERE id = ?", (quest_id,))
                cur.execute("SELECT activator_name FROM quests WHERE id = ?", (quest_id,))
                activator_name = cur.fetchone()[0]
                cur.execute("UPDATE quests SET quest_status = '已拒绝' WHERE receiver_name = ? AND item_id = ? AND activator_name <> ?", (self.username, item_id, activator_name))
                connection.commit()
                connection.close()
                messagebox.showinfo("提交成功", "已通过该交易请求")
        elif flag == 0:
            if quest_status == '已通过':
                messagebox.showinfo("提示信息", "该请求已通过，不能再拒绝")
                return
            elif quest_status == '已拒绝':
                messagebox.showinfo("提示信息", "该请求已拒绝，不能再拒绝")
                return
            confirm = messagebox.askyesno("确认拒绝", "您确定要拒绝该交易请求吗？")
            if confirm:
                cur.execute('''UPDATE quests SET quest_status = ? WHERE id = ?''', ('已拒绝', quest_id))
                connection.commit()
                connection.close()
                messagebox.showinfo("提交成功", "已拒绝该交易请求")
        elif flag == 2:
            if quest_status == '申请中':
                messagebox.showinfo("提示信息", "不能删除正在进行中的交易申请")
                return
            confirm = messagebox.askyesno("确认删除", "您确定要将该交易记录删除吗？")
            if confirm:
                cur.execute('''DELETE FROM quests WHERE id = ?''', (quest_id,))
                messagebox.showinfo("提交成功", "已将该交易记录删除")
                connection.commit()
                connection.close()
        dialog.destroy()
        self.refresh()



import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import ttk, messagebox
from base_class import ManageFrame
from utilities import resource_path
from utilities_new import center_window


class ManageSentQuestsFrame(ManageFrame):   # 管理我已发出的物品交易请求界面
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username

        tag_label = ttk.Label(self.title_frame, text='我已发出的交易请求', style='ThemeFont.TLabel')
        tag_label.pack(side='left')

        # 功能按钮
        refresh_button = ttk.Button(self.title_frame, text="刷新数据", command=self.refresh, style='ButtonFont.TButton', takefocus=False)
        refresh_button.pack(side='left', padx=(20,10),pady=(0,0))
        remove_button = ttk.Button(self.title_frame, text="撤销请求", command=self.retreat, style='ButtonFont.TButton', takefocus=False)
        remove_button.pack(side='left', padx=(10,5),pady=(0,0))
        modify_button = ttk.Button(self.title_frame, text="修改请求备注", command=self.modify, style='ButtonFont.TButton', takefocus=False)
        modify_button.pack(side='left', padx=(10,5),pady=(0,0))
        remove_button = ttk.Button(self.title_frame, text="删除记录", command=self.delete, style='ButtonFont.TButton',
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

        self.font_style = ttk.Style()
        self.font_style.theme_use('default')
        self.font_style.configure('NormalFont.TLabel', font=("方正像素12", 12), background='#f0f0f0')

        self.refresh()
        self.pop_message()


    def refresh(self):
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query = '''
                    SELECT id, item_name, receiver_name, receiver_contact_info, create_time, quest_type, note, quest_status
                    FROM quests
                    WHERE activator_name = ?
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

    def pop_message(self):
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query = '''
                    SELECT id, item_name, receiver_name
                    FROM quests
                    WHERE quest_status = ? AND activator_name = ?
                '''
        cur.execute(query, ('已拒绝', self.username))
        declined_info = cur.fetchall()
        for info in declined_info:
            quest_id, item_name, receiver_name = info
            dialog = tk.Toplevel(self.root)
            dialog.title("提示信息")
            center_window(dialog, 500, 150)

            label = ttk.Label(dialog, text="你对 '"+ receiver_name + "' 发出的对 '" + item_name + "' 的交易申请已被拒绝\n\n要撤回此申请吗？", style='NormalFont.TLabel')
            label.pack(side='top', pady=10, anchor='center')

            button_frame = tk.Frame(dialog)
            cancel_button = tk.Button(button_frame, text="取消")
            cancel_button.bind("<Button-1>", lambda e, dialog_ = dialog : dialog.destroy())
            cancel_button.pack(side='left', padx=10, pady=10)

            confirm_button = tk.Button(button_frame, text="确认")
            confirm_button.bind("<Button-1>", lambda e, id_=id, dialog_=dialog : self.confirm(id_, dialog_, 0))
            confirm_button.pack(side='left', padx=10, pady=10)
            button_frame.pack(side='top', padx=(10, 10))


    def retreat(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("撤销请求")
        center_window(dialog, 300, 150)

        label = ttk.Label(dialog, text="请输入要撤销的请求id")
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

    def delete(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("删除请求")
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
    def modify(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("修改请求备注")
        center_window(dialog, 300, 150)

        label = tk.Label(dialog, text="请输入要修改的请求id")
        label.pack(side='top', pady=10)

        quest_id = tk.StringVar()
        id_entry = ttk.Entry(dialog, width=20, font="Arial 16", textvariable=quest_id, takefocus=False)
        id_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)

        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm(id_entry.get(), dialog, 1))
        confirm_button.pack(side='left', padx=10, pady=10)
        button_frame.pack(side='top', padx=(10, 10))

    def confirm(self, quest_id, dialog, flag):
        quest_id = int(quest_id)
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query = '''
                    SELECT id FROM quests WHERE activator_name = ?
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
            if quest_status == '已拒绝' or quest_status == '已通过':
                messagebox.showwarning("提示信息", "该请求已终止，不能再修改备注")
                return
            self.modify_note(quest_id, dialog)
        elif flag == 0:
            if quest_status == '已拒绝' or quest_status == '已通过':
                messagebox.showwarning("提示信息", "该请求已终止，不能撤回")
                return
            confirm = messagebox.askyesno("确认撤回", "您确定要撤回该交易请求吗？")
            if confirm:
                connection = sqlite3.connect(resource_path('databases/database.db'))
                cur = connection.cursor()
                query = '''
                            DELETE FROM quests WHERE id = ?
                        '''
                cur.execute(query, (quest_id,))
                connection.commit()
                messagebox.showinfo("提交成功", "已将该交易请求撤回")
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

    def modify_note(self, quest_id, dialog):
        dialog.destroy()
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query = '''
                    SELECT note FROM quests WHERE id = ?
                '''
        cur.execute(query, (quest_id,))
        note = cur.fetchone()[0]
        connection.commit()

        dialog = tk.Toplevel(self.root)
        dialog.title("修改请求备注")
        center_window(dialog, 300, 100)
        note_entry = ttk.Entry(dialog, width=40, font="Arial 11", takefocus=False)
        note_entry.pack(side='top', padx=(10, 10),pady=(20, 0))
        note_entry.insert('end', note)

        button_frame = tk.Frame(dialog)
        button_frame.pack(side='top', padx=(10, 10))
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=(20, 0))

        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm_modify(quest_id, note_entry.get(), dialog))
        confirm_button.pack(side='left', padx=10, pady=(20, 0))
    
    def confirm_modify(self, quest_id, note, dialog):
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query = '''
                    UPDATE quests SET note  = ? WHERE id = ?
                '''
        cur.execute(query, (note, quest_id))
        connection.commit()
        messagebox.showinfo("提交成功", "已修改该交易请求的备注")
        dialog.destroy()
        self.refresh()
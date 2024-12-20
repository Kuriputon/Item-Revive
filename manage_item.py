import tkinter as tk
import sqlite3
import os

from tkinter import ttk, messagebox

from base_class import ManageFrame
from item_edit import ItemDetailEditFrame
from utilities import resource_path
from utilities_new import center_window

class ManageItemFrame(ManageFrame):   # 管理物品界面
    def __init__(self, master):
        super().__init__(master)
        tag_label = ttk.Label(self.title_frame, text='物品信息', style='ThemeFont.TLabel')
        tag_label.pack(side='left')

        # 功能按钮
        refresh_button = ttk.Button(self.title_frame, text="刷新数据", command=self.refresh, style='ButtonFont.TButton',
                                    takefocus=False)
        refresh_button.pack(side='left', padx=(20, 10), pady=(0, 0))
        modify_button = ttk.Button(self.title_frame, text="修改物品信息", command=self.modify, style='ButtonFont.TButton',
                                   takefocus=False)
        modify_button.pack(side='left', padx=(10, 5), pady=(0, 0))
        delete_button = ttk.Button(self.title_frame, text="删除物品", command=self.delete_item, style='ButtonFont.TButton',
                                   takefocus=False)
        delete_button.pack(side='left', padx=(10, 5), pady=(0, 0))
        add_button = ttk.Button(self.title_frame, text="增加物品类别", command=self.add, style='ButtonFont.TButton',
                                takefocus=False)
        add_button.pack(side='left', padx=(10, 5), pady=(0, 0))
        add_button = ttk.Button(self.title_frame, text="删除物品类别", command=self.delete_category,
                                style='ButtonFont.TButton', takefocus=False)
        add_button.pack(side='left', padx=(10, 5), pady=(0, 0))

        columns = ('item_id', 'name', 'category', 'uploaded_by', 'status' )
        self.treeview = ttk.Treeview(self, show='headings', columns=columns)
        self.treeview.column('item_id', width=10, anchor='center')
        self.treeview.column('name', width=120, anchor='center')
        self.treeview.column('category', width=20, anchor='center')
        self.treeview.column('uploaded_by', width=50, anchor='center')
        self.treeview.column('status', width=30, anchor='center')
        self.treeview.heading('item_id', text='物品id')
        self.treeview.heading('name', text='物品名称')
        self.treeview.heading('category', text='分类')
        self.treeview.heading('uploaded_by', text='发布者')
        self.treeview.heading('status', text='物品状态')
        self.treeview.pack(side='top', fill='both', expand=True)

        self.refresh()

    def refresh(self):
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query = '''
                    SELECT id, name, category, uploaded_by, status
                    FROM items
                '''
        cur.execute(query)
        item_info = cur.fetchall()
        self.treeview.delete(*self.treeview.get_children())
        for _ in item_info:
            self.treeview.insert('', 'end', values=_)

    def modify(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("更改物品信息")
        center_window(dialog, 300, 150)

        label = tk.Label(dialog, text="请输入要更改信息的物品id")
        label.pack(side='top', pady=10)

        item_id = tk.StringVar()
        item_id_entry = ttk.Entry(dialog, width=20, font="Arial 16", textvariable=item_id, takefocus=False)
        item_id_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)

        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm_item(item_id_entry.get(), dialog, 1))
        confirm_button.pack(side='left', padx=10, pady=10)
        button_frame.pack(side='top', padx=(10,10))


    def delete_item(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("删除物品")
        center_window(dialog, 300, 150)

        label = tk.Label(dialog, text="请输入要删除的物品id")
        label.pack(side='top', pady=10)

        item_id = tk.StringVar()
        item_id_entry = ttk.Entry(dialog, width=20, font="Arial 16", textvariable=item_id, takefocus=False)
        item_id_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)

        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm_item(item_id_entry.get(), dialog, 0))
        confirm_button.pack(side='left', padx=10, pady=10)
        button_frame.pack(side='top', padx=(10, 10))

    def add(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("添加物品类别")
        center_window(dialog, 300, 150)

        label = tk.Label(dialog, text="请输入要添加的物品类别")
        label.pack(side='top', pady=10)

        item_id = tk.StringVar()
        category_entry = ttk.Entry(dialog, width=20, font="Arial 16", textvariable=item_id, takefocus=False)
        category_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)

        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm_category('#'+(category_entry.get()), dialog, 2))
        confirm_button.pack(side='left', padx=10, pady=10)
        button_frame.pack(side='top', padx=(10, 10))

    def delete_category(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("删除物品类别")
        center_window(dialog, 300, 150)

        label = tk.Label(dialog, text="请输入要删除的物品类别")
        label.pack(side='top', pady=10)

        item_id = tk.StringVar()
        category_entry = ttk.Entry(dialog, width=20, font="Arial 16", textvariable=item_id, takefocus=False)
        category_entry.pack(side='top', padx=(10, 10))

        button_frame = tk.Frame(dialog)
        cancel_button = tk.Button(button_frame, text="取消")
        cancel_button.bind("<Button-1>", lambda e: dialog.destroy())
        cancel_button.pack(side='left', padx=10, pady=10)

        confirm_button = tk.Button(button_frame, text="确认")
        confirm_button.bind("<Button-1>", lambda e: self.confirm_category('#'+(category_entry.get()), dialog, 3))
        confirm_button.pack(side='left', padx=10, pady=10)
        button_frame.pack(side='top', padx=(10, 10))

    def confirm_item(self, item_id, dialog, mode):
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        query = '''
                    SELECT count(*) FROM items WHERE id = ?
                '''
        cur.execute(query, (item_id,))
        cnt = cur.fetchone()[0]
        if cnt == 0:
            messagebox.showwarning("提示信息", "请输入有效的物品id")
            return
        if mode == 1:
            dialog.destroy()
            connection = sqlite3.connect(resource_path('databases/database.db'))
            cur = connection.cursor()
            query = '''
                        SELECT name, category, description, image_path, upload_time, uploaded_by, price, status
                        FROM items
                        WHERE id = ?
                    '''
            cur.execute(query, (item_id,))
            item_info = cur.fetchall()
            name, category, description, image_path, upload_time, uploaded_by, price, status = item_info[0]
            edit_window = tk.Toplevel(self.root)
            edit_window.title("更改物品信息")
            center_window(edit_window, 800, 600)
            edit_frame = ItemDetailEditFrame(edit_window, item_id, name, category, description, image_path, upload_time, uploaded_by, price, status)
            edit_frame.pack(fill='both', expand=True)
        elif mode == 0:
            confirm = messagebox.askyesno("确认删除", "您确定要将此物品删除吗？")
            if confirm:
                connection = sqlite3.connect(resource_path('databases/database.db'))
                cur = connection.cursor()
                query = '''
                             DELETE FROM items WHERE id = ?
                         '''
                cur.execute(query, (item_id,))
                connection.commit()
                messagebox.showinfo("提交成功", "已将id为 "+ item_id +" 的物品删除")
                cur.execute('''SELECT image_path FROM items WHERE id = ?''', (item_id,))
                image_path = cur.fetchall()[0]
                connection.close()
                os.remove(image_path)
                dialog.destroy()
                self.refresh()

    def confirm_category(self, category, dialog, mode):
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cur = connection.cursor()
        cur.execute('''SELECT count(*) FROM categories WHERE category = ?''',  (category,))
        cnt = cur.fetchone()[0]
        if mode == 2:
            if cnt != 0:
                messagebox.showwarning("提示信息", "该类别名称已存在")
                return
            confirm = messagebox.askyesno("确认添加", f"您确定要添加物品类别 {category} 吗？")
            if confirm:
                cur.execute('''INSERT INTO categories (category) VALUES (?)''', (category,))
                connection.commit()
                messagebox.showinfo("提交成功", "已将 "+ category +" 加入物品类别")
                dialog.destroy()
        elif mode == 3:
            if cnt == 0:
                messagebox.showwarning("提示信息", "该类别名称不存在")
                return
            confirm = messagebox.askyesno("确认删除", "您确定要删除物品类别 "+ category + ' 吗？\n该类别下的所有物品也将被删除')
            if confirm:
                cur.execute('''DELETE FROM categories WHERE category = ?''', (category,))
                connection.commit()
                messagebox.showinfo("提交成功", "已将 " + category + " 物品类别删除")
                dialog.destroy()
                self.refresh()


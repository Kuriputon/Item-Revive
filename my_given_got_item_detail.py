import os
import tkinter as tk
import sqlite3

from tkinter import ttk, messagebox
from base_class import DetailFrame
from utilities_new import resource_path


class MyGivenGotDetailFrame(DetailFrame):  # 已出、已得物品详细页面
    def __init__(self, master, item_id, name, category, description, image_path, upload_time, uploaded_by, price,
                 status):
        super().__init__(master, item_id, name, category, description, image_path, upload_time, uploaded_by, price)
        self.status = status

        self.delete_button_frame = tk.Frame(self.image_frame)
        self.delete_button = ttk.Button(self.delete_button_frame, text="删除记录", style='ButtonFont.TButton',
                                        takefocus=False)
        self.delete_button.config(command=lambda: self.delete_item(self.item_id))
        self.delete_button.pack(side='left', padx=(10, 0), pady=(0, 1))
        self.delete_button_frame.pack(side='top', padx=(10,0), pady=(35,10))
        self.attributes_frame.pack(side='left', padx=(40, 10), pady=(50, 10))

    def delete_item(self, item_id):
        confirm = messagebox.askyesno("确认删除", "您确定要删除这个物品记录吗？")
        if confirm:
            connection = sqlite3.connect(resource_path('databases/database.db'))
            cursor = connection.cursor()
            cursor.execute("SELECT image_path FROM items WHERE id = ?", (item_id,))
            row = cursor.fetchone()
            if row:
                image_path = row[0]
                cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
                connection.commit()
                if image_path is None:
                    messagebox.showinfo("删除成功", "物品记录已删除")
                elif image_path and os.path.isfile(image_path):
                    os.remove(image_path)
                    messagebox.showinfo("删除成功", "物品记录已删除")
            else:
                messagebox.showwarning("警告", "未找到该物品，请刷新后重试")
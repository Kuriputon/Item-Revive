import tkinter as tk
import os
import sqlite3

from base_class import DetailFrame
from tkinter import ttk, messagebox
from utilities_new import resource_path
from item_edit import ItemDetailEditFrame
from controller import GetFrames

class MyItemFrame(DetailFrame):    # 管理我的物品界面
    def __init__(self, master, item_id, name, category, description, image_path, upload_time, uploaded_by, price, status):
        super().__init__(master, item_id, name, category, description, image_path, upload_time, uploaded_by, price)
        self.status = status

        get_frames_instance = GetFrames.get_instance()
        frames = get_frames_instance.get_frames()
        self.edit_frame=ItemDetailEditFrame(self.root, self.item_id, self.name,
                                      self.category, self.description, self.image_path,
                                      self.upload_time, self.uploaded_by, self.price, self.status)
        key_name = "user_publish_edit_frame_"+str(item_id)
        frames[key_name] = self.edit_frame

        self.delete_button_frame = tk.Frame(self.image_frame)
        self.delete_button = ttk.Button(self.delete_button_frame, text="删除物品", style='ButtonFont.TButton', takefocus=False)
        self.delete_button.config(command=lambda: self.delete_item(self.item_id))
        self.delete_button.pack(side='left', padx=(10,0),pady=(0,1))
        if self.status == '闲置中':
            self.set_button = ttk.Button(self.delete_button_frame, text="设为已出", style='ButtonFont.TButton', takefocus=False)
            self.set_button.config(command=lambda: self.set_given(self.item_id))
        elif self.status == '求物中':
            self.set_button = ttk.Button(self.delete_button_frame, text="设为已得", style='ButtonFont.TButton', takefocus=False)
            self.set_button.config(command=lambda: self.set_got(self.item_id))
        self.set_button.pack(side='left', padx=(10,0), pady=(0,0))
        self.delete_button_frame.pack(side='top', padx=(5,0), pady=(0,1))
        self.image_frame.pack(side='left', padx=(10, 10), pady=(0, 0))


        self.edit_button_frame = tk.Frame(self.attributes_frame)
        self.edit_button = ttk.Button(self.edit_button_frame, text="编辑物品", style='ButtonFont.TButton', takefocus=False)
        self.edit_button.config(command=lambda: self.show_edit_frame(self.edit_frame))
        self.edit_button.pack(side='top', padx=(20, 0), pady=(0, 0))
        self.edit_button_frame.pack(side='top', padx=(10,0), pady=(35,10))
        self.attributes_frame.pack(side='left', padx=(40, 10), pady=(50, 10))

    def delete_item(self, item_id):
        confirm = messagebox.askyesno("确认删除", "您确定要删除这个物品吗？")
        if confirm:
            connection = sqlite3.connect(resource_path('databases/database.db'))
            cursor1 = connection.cursor()
            cursor1.execute("SELECT status FROM items WHERE id = ?", (item_id,))
            if cursor1.fetchone()[0] == '已出' or cursor1.fetchone()[0] == '已得':
                messagebox.showinfo("操作错误", "物品状态已更新，请刷新页面")
                connection.close()
                return
            cursor = connection.cursor()
            cursor.execute("SELECT image_path FROM items WHERE id = ?", (item_id,))
            row = cursor.fetchone()
            if row:
                image_path = row[0]
                cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
                connection.commit()
                if image_path is None:
                    messagebox.showinfo("删除成功", "物品已删除")
                elif image_path and os.path.isfile(image_path):
                    os.remove(image_path)
                    messagebox.showinfo("删除成功", "物品已删除")
            else:
                messagebox.showwarning("警告", "未找到该物品，请刷新后重试")

    def show_edit_frame(self, edit_frame):
        get_frames_instance = GetFrames.get_instance()
        frames = get_frames_instance.get_frames()

        for frame in frames.values():
            frame.pack_forget()

        new_edit_frame = ItemDetailEditFrame(self.root, self.item_id, self.name,
                                      self.category, self.description, self.image_path,
                                      self.upload_time, self.uploaded_by, self.price, self.status)
        edit_frame.destroy()
        key_name = "user_publish_edit_frame_" + str(self.item_id)
        frames[key_name] = new_edit_frame
        new_edit_frame.pack(fill='both', expand=True)

    def set_given(self, item_id):
        confirm = messagebox.askyesno("确认设置", "您确定要将这个物品设为已出吗？")
        if confirm:
            connection = sqlite3.connect(resource_path('databases/database.db'))
            cursor1 = connection.cursor()
            cursor1.execute("SELECT status FROM items WHERE id = ?", (item_id,))
            if cursor1.fetchone()[0] == '已出':
                messagebox.showinfo("操作错误", "物品状态已更新，请刷新页面")
                connection.close()
                return
            cursor2 = connection.cursor()
            cursor2.execute("UPDATE items SET status = '已出' WHERE id = ?", (item_id,))
            connection.commit()
            messagebox.showinfo("设置成功", "已将物品状态设置为已出")
            connection.close()

    def set_got(self, item_id):
        confirm = messagebox.askyesno("确认设置", "您确定要将这个物品设为已得吗？")
        if confirm:
            connection = sqlite3.connect(resource_path('databases/database.db'))
            cursor1 = connection.cursor()
            cursor1.execute("SELECT status FROM items WHERE id = ?", (item_id,))
            if cursor1.fetchone()[0] == '已得':
                messagebox.showinfo("操作错误", "物品状态已更新，请刷新页面")
                connection.close()
                return
            cursor2 = connection.cursor()
            cursor2.execute("UPDATE items SET status = '已得' WHERE id = ?", (item_id,))
            connection.commit()
            messagebox.showinfo("设置成功", "已将物品状态设置为已得")
            connection.close()



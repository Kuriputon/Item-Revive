import os
import tkinter as tk
import shutil
import sqlite3

from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from datetime import datetime

from base_class import PublishFrame
from utilities import resource_path, create_new_item_detail_frame
from controller import GetFrames


class PublishItemFrame(PublishFrame):  # 发布闲置页面
    def __init__(self, master, username):
        super().__init__(master, username)
        self.default_image = Image.open(resource_path("images/configs/default_image.jpg"))
        self.default_photo = ImageTk.PhotoImage(self.default_image)
        self.upload_image_path = None
        self.tittle_label = ttk.Label(self.tittle_frame, text="发布闲置信息", style="TittleFont.TLabel")
        self.tittle_label.pack(side='left', padx=(0, 5), pady=(0, 5))
        self.create_labels()

    def submit_item(self):
        confirm = messagebox.askyesno("确认发布", "您确定要发布此物品吗？")
        if confirm:
            item_name = self.name_entry.get()
            if self.price_entry.get()=='':
                messagebox.showwarning("提示信息", "请填写所有字段并上传图片")
                return
            else:
                price = float(self.price_entry.get())
            description = self.description_text.get("1.0", tk.END).strip()
            image_path = self.upload_image_path
            selected_tag = self.tag_var.get()
            username = self.username

            if image_path:
                file_name = os.path.basename(self.upload_image_path)
                name, ext = os.path.splitext(file_name)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                new_file_name = f"{name}_{timestamp}{ext}"
                new_file_path = resource_path(os.path.join(self.images_folder, new_file_name))

            if not item_name or not price or not description or not image_path or selected_tag == "选择":
                messagebox.showwarning("提示信息", "请填写所有字段并上传图片")
                return
            else:
                connection = sqlite3.connect(resource_path('databases/database.db'))
                cursor = connection.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO items (name, category, description, image_path, upload_time, uploaded_by, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (item_name, selected_tag, description, new_file_path, timestamp, username, price, '闲置中')
                        )
                    connection.commit()
                    last_id = cursor.lastrowid
                    connection.close()
                    shutil.copy(self.upload_image_path, new_file_path)
                    self.image_label.file_path = new_file_path
                    messagebox.showinfo("提交成功", "闲置物品已成功发布！")
                    new_frame = create_new_item_detail_frame(self.root, last_id)
                    get_frames_instance = GetFrames.get_instance()
                    get_frames_instance.frames.update(new_frame)
                except sqlite3.Error as e:
                    print("Database error:", e)
                    connection.close()
                self.reset_form()


class PublishWantingFrame(PublishFrame):   # 发布求物页面
    def __init__(self, master, username):
        super().__init__(master, username)
        self.default_image = Image.open(resource_path("images/configs/default_wanting_image.jpg"))
        self.default_photo = ImageTk.PhotoImage(self.default_image)
        self.tittle_label = ttk.Label(self.tittle_frame, text="发布求物信息", style="TittleFont.TLabel")
        self.tittle_label.pack(side='left', padx=(0, 5), pady=(0, 5))
        self.create_labels()
        self.tip_font_style = ttk.Style()
        self.tip_font_style.theme_use('default')
        self.tip_font_style.configure('TipFont.TLabel', font=('方正小标宋_GBK', 10), background='#f0f0f0', foreground='gray')
        self.use_default_frame = tk.Frame(self.image_frame)
        self.use_default_label = ttk.Label(self.use_default_frame, text="也可不上传，使用默认图片",
                                           style='TipFont.TLabel')
        self.use_default_label.pack(side='left', padx=(0, 0), pady=(0, 10))
        self.use_default_frame.pack(side='top', padx=(20, 0), pady=(0, 10))

    def submit_item(self):
        confirm = messagebox.askyesno("确认提交", "您确定要发布此物品吗？")
        if confirm:
            item_name = self.name_entry.get()
            if self.price_entry.get() == '':
                messagebox.showwarning("提示信息", "请填写所有字段")
                return
            else:
                price = float(self.price_entry.get())
            description = self.description_text.get("1.0", tk.END).strip()
            image_path = self.upload_image_path
            selected_tag = self.tag_var.get()
            username = self.username
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            if image_path:
                file_name = os.path.basename(self.upload_image_path)
                name, ext = os.path.splitext(file_name)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                new_file_name = f"{name}_{timestamp}{ext}"
                new_file_path = resource_path(os.path.join(self.images_folder, new_file_name))

            if not item_name or not price or not description or selected_tag == "选择标签":
                messagebox.showwarning("提示信息", "请填写所有字段")
                return
            elif image_path:
                connection = sqlite3.connect(resource_path('databases/database.db'))
                cursor = connection.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO items (name, category, description, image_path, upload_time, uploaded_by, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (item_name, selected_tag, description, new_file_path, timestamp, username, price, '求物中')
                        )
                    connection.commit()
                    last_id = cursor.lastrowid
                    connection.close()
                    shutil.copy(self.upload_image_path, new_file_path)
                    self.image_label.file_path = new_file_path
                    messagebox.showinfo("提交成功", "求物信息已成功发布！")
                    new_frame = create_new_item_detail_frame(self.root, last_id)
                    get_frames_instance = GetFrames.get_instance()
                    get_frames_instance.frames.update(new_frame)
                except sqlite3.Error as e:
                    print("Database error:", e)
                    connection.close()
                self.reset_form()
            else:
                connection = sqlite3.connect(resource_path('databases/database.db'))
                cursor = connection.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO items (name, category, description, upload_time, uploaded_by, price, status) VALUES (?, ?, ?, ?, ?, ?, ?)", (item_name, selected_tag, description, timestamp, username, price, '求物中')
                        )
                    connection.commit()
                    last_id = cursor.lastrowid
                    connection.close()
                    messagebox.showinfo("提交成功", "求物信息已成功发布！")
                    new_frame = create_new_item_detail_frame(self.root, last_id)
                    get_frames_instance = GetFrames.get_instance()
                    get_frames_instance.frames.update(new_frame)
                except sqlite3.Error as e:
                    print("Database error:", e)
                    connection.close()
                self.reset_form()

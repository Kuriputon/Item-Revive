import os
import tkinter as tk
import shutil
import sqlite3
import pyglet

from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from datetime import datetime

from utilities import resource_path


class PublishItemFrame(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.root = master
        self.images_folder = "images"
        self.default_image = Image.open(resource_path("images/configs/default_image.jpg"))
        self.default_photo = ImageTk.PhotoImage(self.default_image)
        self.upload_image_path = None
        self.username = username

        self.tittle_frame = tk.Frame(self)
        self.upload_frame = tk.Frame(self)
        self.image_frame = tk.Frame(self.upload_frame)
        self.attributes_frame = tk.Frame(self.upload_frame)
        self.create_widgets()

        pyglet.font.add_file(resource_path('fonts/方正像素12.TTF'))
        pyglet.font.load('方正像素12')

        pyglet.font.add_file(resource_path('fonts/方正小标宋_GBK.TTF'))
        pyglet.font.load('方正小标宋_GBK')

    def create_widgets(self):
        tittle_font_style = ttk.Style()
        tittle_font_style.theme_use('default')
        tittle_font_style.configure('TittleFont.TLabel', font=('方正小标宋_GBK', 22), background='#f0f0f0')


        self.tittle_label = ttk.Label(self.tittle_frame, text="发布闲置信息", style="TittleFont.TLabel")
        self.tittle_label.pack(side='left', padx=(0, 5), pady=(0, 5))
        self.tittle_frame.pack(side='top', padx=(0, 0), pady=(20, 0))
        self.upload_frame.pack(side='top', padx=(0, 0), pady=(0, 5))

        button_font_style = ttk.Style()
        button_font_style.theme_use('default')
        button_font_style.configure('ButtonFont.TButton', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        self.image_label_frame = tk.Frame(self.image_frame)
        self.image_label = tk.Label(self.image_label_frame, image=self.default_photo, width=300, height=400)
        self.image_label.pack(side='left', padx=(10,0),pady=(0,0))
        self.image_label_frame.pack(side='top', padx=(20,0), pady=(0,0))

        self.upload_button_frame = tk.Frame(self.image_frame)
        self.upload_button = ttk.Button(self.upload_button_frame, text="上传图片", command=self.upload_image, style='ButtonFont.TButton', takefocus=False)
        self.upload_button.pack(side='left', padx=(10,0),pady=(0,1))
        self.upload_button_frame.pack(side='top', padx=(20,0), pady=(0,1))

        self.image_frame.pack(side='left', padx=(10, 10), pady=(0, 0))

        attributes_font_style = ttk.Style()
        attributes_font_style.theme_use('default')
        attributes_font_style.configure('AttributesFont.TLabel', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        self.name_frame = tk.Frame(self.attributes_frame)
        self.name_label = ttk.Label(self.name_frame, text="物品名称", style="AttributesFont.TLabel")
        self.name_label.pack(side='left', padx=(5,55), pady=(5,5))
        self.name_entry = tk.Entry(self.name_frame)
        self.name_entry.pack(side='left', padx=(0,0), pady=(5,5))
        self.name_frame.pack(side='top', padx=(0,40), pady=(5,5))

        self.price_frame = tk.Frame(self.attributes_frame)
        self.price_label = ttk.Label(self.price_frame, text="物品价格", style="AttributesFont.TLabel")
        self.price_label.pack(side='left', padx=(5,55), pady=(0,5))
        self.price_entry = tk.Entry(self.price_frame)
        self.price_entry.pack(side='left', padx=(0,0), pady=(0,5))
        self.price_frame.pack(side='top', padx=(0,40), pady=(5,5))

        self.tag_var = tk.StringVar()
        self.tag_frame = tk.Frame(self.attributes_frame)
        self.tag_label = ttk.Label(self.tag_frame, text="物品标签", style="AttributesFont.TLabel")
        self.tag_label.pack(side='left', padx=(18,58), pady=(0,5))
        self.tag_options = ['#书籍', '#数码', '#居家', '#食品', '#衣饰', '#鞋包', '#运动', '#文具', '#周边', '#其他']
        self.tag_dropdown = ttk.Combobox(self.tag_frame, textvariable=self.tag_var, values=self.tag_options, state='readonly', takefocus=False)
        self.tag_dropdown.set("选择")
        self.tag_dropdown.pack(side='left', padx=(0,0), pady=(0,5))
        self.tag_frame.pack(side='top', padx=(0,40), pady=(5,5))

        self.desc_frame = tk.Frame(self.attributes_frame)
        self.description_label = ttk.Label(self.desc_frame, text="物品描述", style="AttributesFont.TLabel")
        self.description_label.pack(side='left', padx=(0,55), pady=(0,10))
        self.description_text = tk.Text(self.desc_frame, height=15, width=30)
        self.description_text.pack(side='left', padx=(0,0), pady=(0,5))
        self.desc_frame.pack(side='top', padx=(30,0), pady=(5,10))

        self.submit_button_frame = tk.Frame(self.attributes_frame)
        self.submit_button = ttk.Button(self.submit_button_frame, text="提交", command=self.submit_item, style='ButtonFont.TButton', takefocus=False)
        self.submit_button.pack(side='top', padx=(20, 0), pady=(0, 0))
        self.submit_button_frame.pack(side='top', padx=(10,0), pady=(35,10))

        self.attributes_frame.pack(side='left', padx=(40, 10), pady=(50, 10))

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="选择图片",
                                                filetypes=(("Image Files", "*.png;*.jpg;*.jpeg;*.gif"), ("All Files", "*.*")))
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((300, 300))
            self.photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo
            self.upload_image_path = file_path

    def submit_item(self):
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
            connection = sqlite3.connect(resource_path('databases/items.db'))
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO items (name, category, description, image_path, upload_time, uploaded_by, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (item_name, selected_tag, description, new_file_path, timestamp, username, price, '闲置中')
                    )
                connection.commit()
                connection.close()
                shutil.copy(self.upload_image_path, new_file_path)
                self.image_label.file_path = new_file_path
                messagebox.showinfo("提交成功", "闲置物品已成功发布！")
            except sqlite3.Error as e:
                print("Database error:", e)
                connection.close()

            self.reset_form()

    def reset_form(self):
        self.name_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.description_text.delete("1.0", 'end')
        self.tag_dropdown.set("选择")
        self.image_label.config(image=self.default_photo)

class PublishWantingFrame(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.root = master
        self.images_folder = "images"
        self.default_image = Image.open(resource_path("images/configs/default_wanting_image.jpg"))
        self.default_photo = ImageTk.PhotoImage(self.default_image)
        self.upload_image_path = None
        self.username = username

        self.tittle_frame = tk.Frame(self)
        self.upload_frame = tk.Frame(self)
        self.image_frame = tk.Frame(self.upload_frame)
        self.attributes_frame = tk.Frame(self.upload_frame)
        self.create_widgets()

    def create_widgets(self):
        tittle_font_style = ttk.Style()
        tittle_font_style.theme_use('default')
        tittle_font_style.configure('TittleFont.TLabel', font=('方正小标宋_GBK', 22), background='#f0f0f0')


        self.tittle_label = ttk.Label(self.tittle_frame, text="发布求物信息", style="TittleFont.TLabel")
        self.tittle_label.pack(side='left', padx=(0, 5), pady=(0, 5))
        self.tittle_frame.pack(side='top', padx=(0, 0), pady=(20, 5))
        self.upload_frame.pack(side='top', padx=(0, 0), pady=(0, 5))

        button_font_style = ttk.Style()
        button_font_style.theme_use('default')
        button_font_style.configure('ButtonFont.TButton', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        self.image_label_frame = tk.Frame(self.image_frame)
        self.image_label = tk.Label(self.image_label_frame, image=self.default_photo, width=300, height=400)
        self.image_label.pack(side='left', padx=(10,0),pady=(0,0))
        self.image_label_frame.pack(side='top', padx=(20,0), pady=(0,0))

        tip_font_style = ttk.Style()
        tip_font_style.theme_use('default')
        tip_font_style.configure('TipFont.TLabel', font=('方正小标宋_GBK', 10), background='#f0f0f0', foreground='gray')

        self.upload_button_frame = tk.Frame(self.image_frame)
        self.upload_button = ttk.Button(self.upload_button_frame, text="上传图片", command=self.upload_image, style='ButtonFont.TButton', takefocus=False)
        self.upload_button.pack(side='left', padx=(10,0),pady=(0,1))
        self.upload_button_frame.pack(side='top', padx=(20,0), pady=(0,1))
        self.use_default_frame = tk.Frame(self.image_frame)
        self.use_default_label = ttk.Label(self.use_default_frame, text="也可不上传，使用默认图片", style='TipFont.TLabel')
        self.use_default_label.pack(side='left', padx=(0, 0), pady=(0, 10))
        self.use_default_frame.pack(side='top', padx=(20,0), pady=(0,10))

        self.image_frame.pack(side='left', padx=(10, 10), pady=(0, 10))

        attributes_font_style = ttk.Style()
        attributes_font_style.theme_use('default')
        attributes_font_style.configure('AttributesFont.TLabel', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        self.name_frame = tk.Frame(self.attributes_frame)
        self.name_label = ttk.Label(self.name_frame, text="物品名称", style="AttributesFont.TLabel")
        self.name_label.pack(side='left', padx=(5,55), pady=(5,5))
        self.name_entry = tk.Entry(self.name_frame)
        self.name_entry.pack(side='left', padx=(0,0), pady=(5,5))
        self.name_frame.pack(side='top', padx=(0,40), pady=(5,5))

        self.price_frame = tk.Frame(self.attributes_frame)
        self.price_label = ttk.Label(self.price_frame, text="物品价格", style="AttributesFont.TLabel")
        self.price_label.pack(side='left', padx=(5,55), pady=(0,5))
        self.price_entry = tk.Entry(self.price_frame)
        self.price_entry.pack(side='left', padx=(0,0), pady=(0,5))
        self.price_frame.pack(side='top', padx=(0,40), pady=(5,5))

        self.tag_var = tk.StringVar()
        self.tag_frame = tk.Frame(self.attributes_frame)
        self.tag_label = ttk.Label(self.tag_frame, text="物品标签", style="AttributesFont.TLabel")
        self.tag_label.pack(side='left', padx=(18,58), pady=(0,5))
        self.tag_options = ['#书籍', '#数码', '#居家', '#食品', '#衣饰', '#鞋包', '#运动', '#文具', '#周边', '#其他']
        self.tag_dropdown = ttk.Combobox(self.tag_frame, textvariable=self.tag_var, values=self.tag_options, state='readonly', takefocus=False)
        self.tag_dropdown.set("选择")
        self.tag_dropdown.pack(side='left', padx=(0,0), pady=(0,5))
        self.tag_frame.pack(side='top', padx=(0,40), pady=(5,5))

        self.desc_frame = tk.Frame(self.attributes_frame)
        self.description_label = ttk.Label(self.desc_frame, text="物品描述", style="AttributesFont.TLabel")
        self.description_label.pack(side='left', padx=(0,55), pady=(0,10))
        self.description_text = tk.Text(self.desc_frame, height=15, width=30)
        self.description_text.pack(side='left', padx=(0,0), pady=(0,5))
        self.desc_frame.pack(side='top', padx=(30,0), pady=(5,10))

        self.submit_button_frame = tk.Frame(self.attributes_frame)
        self.submit_button = ttk.Button(self.submit_button_frame, text="提交", command=self.submit_item, style='ButtonFont.TButton', takefocus=False)
        self.submit_button.pack(side='top', padx=(20,0), pady=(0,0))
        self.submit_button_frame.pack(side='top', padx=(10,0), pady=(20,10))

        self.attributes_frame.pack(side='left', padx=(50, 10), pady=(20, 10))

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="选择图片",
                                                filetypes=(("Image Files", "*.png;*.jpg;*.jpeg;*.gif"), ("All Files", "*.*")))
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((300, 300))
            self.photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo
            self.upload_image_path = file_path

    def submit_item(self):
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
            new_file_name = f"{name}_{timestamp}{ext}"
            new_file_path = resource_path(os.path.join(self.images_folder, new_file_name))


        if not item_name or not price or not description or selected_tag == "选择标签":
            messagebox.showwarning("提示信息", "请填写所有字段")
            return
        elif image_path:
            connection = sqlite3.connect(resource_path('databases/items.db'))
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO items (name, category, description, image_path, upload_time, uploaded_by, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (item_name, selected_tag, description, new_file_path, timestamp, username, price, '求物中')
                    )
                connection.commit()
                connection.close()
                shutil.copy(self.upload_image_path, new_file_path)
                self.image_label.file_path = new_file_path
                messagebox.showinfo("提交成功", "求物信息已成功发布！")
            except sqlite3.Error as e:
                print("Database error:", e)
                connection.close()
            self.reset_form()
        else:
            connection = sqlite3.connect(resource_path('databases/items.db'))
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO items (name, category, description, upload_time, uploaded_by, price, status) VALUES (?, ?, ?, ?, ?, ?, ?)", (item_name, selected_tag, description, timestamp, username, price, '求物中')
                    )
                connection.commit()
                connection.close()
                messagebox.showinfo("提交成功", "求物信息已成功发布！")
            except sqlite3.Error as e:
                print("Database error:", e)
                connection.close()
            self.reset_form()

    def reset_form(self):
        self.name_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.description_text.delete("1.0", 'end')
        self.tag_dropdown.set("选择")
        self.upload_image_path = None
        self.image_label.config(image=self.default_photo)
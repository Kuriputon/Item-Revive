import tkinter as tk
import pyglet
import os
import sqlite3
import shutil

from datetime import datetime
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
from utilities_new import resource_path

class ItemDetailEditFrame(tk.Frame):
    def __init__(self, master, item_id, name, category, description, image_path, upload_time, uploaded_by, price, status):
        super().__init__(master)
        self.root = master
        self.image_path = image_path
        self.item_id = item_id
        self.category = category
        self.description = description
        self.upload_time = upload_time
        self.name = name
        self.uploaded_by = uploaded_by
        self.price = price
        self.status = status
        self.images_folder = resource_path('images')
        self.upload_time=upload_time
        self.upload_image_path=None

        pyglet.font.add_file(resource_path('fonts/方正小标宋_GBK.TTF'))
        pyglet.font.load('方正小标宋_GBK')

        img = Image.open(self.image_path)
        img.thumbnail((300, 300))
        self.photo = ImageTk.PhotoImage(img)

        self.tittle_frame = tk.Frame(self)
        self.detail_frame = tk.Frame(self)
        self.image_frame = tk.Frame(self.detail_frame)
        self.attributes_frame = tk.Frame(self.detail_frame)
        self.create_widgets()

    def create_widgets(self):
        tittle_font_style = ttk.Style()
        tittle_font_style.theme_use('default')
        tittle_font_style.configure('TittleFont.TEntry', font=('方正小标宋_GBK', 22), background='#f0f0f0',
                                    wraplength=600)

        self.tittle_label = ttk.Entry(self.tittle_frame, style="TittleFont.TEntry")
        self.tittle_label.insert('end', self.name)
        self.tittle_label.pack(side='left', padx=(0, 5), pady=(0, 5))
        self.tittle_frame.pack(side='top', padx=(0, 0), pady=(20, 0))
        self.detail_frame.pack(side='top', padx=(0, 0), pady=(0, 5))

        button_font_style = ttk.Style()
        button_font_style.theme_use('default')
        button_font_style.configure('ButtonFont.TButton', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        self.image_label_frame = tk.Frame(self.image_frame)
        self.image_label = tk.Label(self.image_label_frame, image=self.photo, width=300, height=400)
        self.image_label.image = self.photo
        self.image_label.pack(side='left', padx=(10, 0), pady=(0, 0))
        self.image_label_frame.pack(side='top', padx=(20, 0), pady=(0, 0))

        self.upload_button_frame = tk.Frame(self.image_frame)
        self.upload_button = ttk.Button(self.upload_button_frame, text="上传图片", style='ButtonFont.TButton',
                                        takefocus=False)
        self.upload_button.config(command=lambda: self.upload_image())
        self.upload_button.pack(side='left', padx=(10, 0), pady=(0, 1))
        self.upload_button_frame.pack(side='top', padx=(20, 0), pady=(0, 1))

        self.image_frame.pack(side='left', padx=(10, 10), pady=(0, 0))

        attributes_font_style = ttk.Style()
        attributes_font_style.theme_use('default')
        attributes_font_style.configure('AttributesFont.TLabel', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        item_detail_price_font_style = ttk.Style()
        item_detail_price_font_style.theme_use('default')
        item_detail_price_font_style.configure('ItemDetailPriceFont.TEntry', font=('方正小标宋_GBK', 11),
                                               background='#f0f0f0',
                                               foreground='red', width=10)

        self.price_frame = tk.Frame(self.attributes_frame)
        self.price_label = ttk.Label(self.price_frame, text="物品价格", style="AttributesFont.TLabel")
        self.price_label.pack(side='left', padx=(70, 40), pady=(5, 5))
        self.price_value_label = ttk.Entry(self.price_frame, style="ItemDetailPriceFont.TEntry")
        self.price_value_label.insert('end', self.price)
        self.price_value_label.pack(side='left', padx=(0, 0), pady=(5, 5))
        self.price_frame.pack(side='top', padx=(0, 40), pady=(5, 5))

        self.tag_var = tk.StringVar()
        self.tag_frame = tk.Frame(self.attributes_frame)
        self.tag_label = ttk.Label(self.tag_frame, text="物品标签", style="AttributesFont.TLabel")
        self.tag_label.pack(side='left', padx=(0, 80), pady=(0, 5))
        self.tag_options = ['#书籍', '#数码', '#居家', '#食品', '#衣饰', '#鞋包', '#运动', '#文具', '#周边', '#其他']
        self.tag_dropdown = ttk.Combobox(self.tag_frame, textvariable=self.tag_var, values=self.tag_options, takefocus=False)
        self.tag_dropdown.set(self.category)
        self.tag_dropdown.pack(side='left', padx=(0, 0), pady=(0, 5))

        self.desc_frame = tk.Frame(self.attributes_frame)
        self.description_label = ttk.Label(self.desc_frame, text="物品描述", style="AttributesFont.TLabel")
        self.description_label.pack(side='left', padx=(0, 20), pady=(0, 10))
        self.description_text = tk.Text(self.desc_frame, height=15, width=25)
        self.description_text.insert('end', self.description)
        self.description_text.pack(side='left', padx=(20, 0), pady=(0, 5))
        self.desc_frame.pack(side='top', padx=(60, 0), pady=(5, 10))

        self.edit_button_frame = tk.Frame(self.attributes_frame)
        self.edit_button = ttk.Button(self.edit_button_frame, text="保存更改", style='ButtonFont.TButton',
                                      takefocus=False)
        self.edit_button.config(command=lambda: self.submit_item())
        self.edit_button.pack(side='top', padx=(20, 0), pady=(0, 0))
        self.edit_button_frame.pack(side='top', padx=(10, 0), pady=(80, 10))

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
        item_name = self.tittle_label.get()
        description = self.description_text.get("1.0", tk.END).strip()
        image_path = self.upload_image_path
        selected_tag = self.tag_var.get()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        if self.price_value_label.get() == '' or not item_name or not description:
            messagebox.showwarning("提示信息", "所有字段不能为空")
            return
        else:
            price = float(self.price_value_label.get())

        if image_path:
            file_name = os.path.basename(self.upload_image_path)
            name, ext = os.path.splitext(file_name)
            new_file_name = f"{name}_{timestamp}{ext}"
            new_file_path = resource_path(os.path.join(self.images_folder, new_file_name))

            connection = sqlite3.connect(resource_path('databases/items.db'))
            cursor = connection.cursor()
            try:
                update_query = '''
                    UPDATE items
                    SET name = ?, category = ?, description = ?, image_path = ?, price = ?
                    WHERE id = ?
                '''
                cursor.execute(update_query, (item_name, selected_tag, description, image_path, price, self.item_id))
                connection.commit()
                connection.close()
                shutil.copy(self.upload_image_path, new_file_path)
                self.image_label.file_path = new_file_path
                messagebox.showinfo("提交成功", "物品信息已成功修改！")
            except sqlite3.Error as e:
                print("Database error:", e)
                connection.close()
            if self.image_path and self.image_path != resource_path("images/configs/default_wanting_image.jpg"):
                os.remove(image_path)
        else:
            connection = sqlite3.connect(resource_path('databases/items.db'))
            cursor = connection.cursor()
            try:
                update_query = '''
                                    UPDATE items
                                    SET name = ?, category = ?, description = ?, price = ?
                                    WHERE id = ?
                                '''
                cursor.execute(update_query, (item_name, selected_tag, description, price, self.item_id))
                connection.commit()
                connection.close()
                messagebox.showinfo("提交成功", "物品信息已成功修改！")
            except sqlite3.Error as e:
                print("Database error:", e)
                connection.close()
import sqlite3
import tkinter as tk

from datetime import datetime
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from utilities_new import resource_path


class DetailFrame(tk.Frame):
    def __init__(self, master, item_id, name, category, description, image_path, upload_time, uploaded_by, price):
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

        dt = datetime.strptime(str(self.upload_time), "%Y%m%d%H%M%S")
        self.upload_time = dt.strftime("%Y.%m.%d %H:%M")
        if self.image_path:
            img = Image.open(self.image_path)
        else:
            img = Image.open(resource_path("images/configs/default_wanting_image.jpg"))
        img.thumbnail((300, 300))
        self.photo = ImageTk.PhotoImage(img)

        self.tittle_font_style = ttk.Style()
        self.tittle_font_style.theme_use('default')
        self.tittle_font_style.configure('TittleFont.TLabel', font=('方正小标宋_GBK', 22), background='#f0f0f0', wraplength=600)

        self.button_font_style = ttk.Style()
        self.button_font_style.theme_use('default')
        self.button_font_style.configure('ButtonFont.TButton', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        self.attributes_font_style = ttk.Style()
        self.attributes_font_style.theme_use('default')
        self.attributes_font_style.configure('AttributesFont.TLabel', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        self.font_style = ttk.Style()
        self.font_style.theme_use('default')
        self.font_style.configure('NormalFont.TLabel', font=("方正像素12", 11), background='#f0f0f0')

        item_detail_price_font_style = ttk.Style()
        item_detail_price_font_style.theme_use('default')
        item_detail_price_font_style.configure('ItemDetailPriceFont.TLabel', font=('方正小标宋_GBK', 11),
                                               background='#f0f0f0',
                                               foreground='red', width=10)
        time_font_style = ttk.Style()
        time_font_style.theme_use('default')
        time_font_style.configure('TimeFont.TLabel', font=('方正小标宋_GBK', 10), background='#f0f0f0', foreground='#777674')

        self.tittle_frame = tk.Frame(self)
        self.detail_frame = tk.Frame(self)
        self.image_frame = tk.Frame(self.detail_frame)
        self.attributes_frame = tk.Frame(self.detail_frame)

        tittle_label = ttk.Label(self.tittle_frame, text=self.name, style="TittleFont.TLabel")
        tittle_label.pack(side='left', padx=(0, 5), pady=(0, 5))
        self.tittle_frame.pack(side='top', padx=(0, 0), pady=(20, 0))
        self.detail_frame.pack(side='top', padx=(0, 0), pady=(0, 5))

        image_label_frame = tk.Frame(self.image_frame)
        image_label = tk.Label(image_label_frame, image=self.photo, width=300, height=400)
        image_label.image = self.photo
        image_label.pack(side='left', padx=(10,0),pady=(0,0))
        image_label_frame.pack(side='top', padx=(20,0), pady=(0,0))

        self.image_frame.pack(side='left', padx=(10, 10), pady=(0, 0))
        price_frame = tk.Frame(self.attributes_frame)
        price_label = ttk.Label(price_frame, text="物品价格", style="AttributesFont.TLabel")
        price_label.pack(side='left', padx=(40,70), pady=(5,5))
        price_value_label = ttk.Label(price_frame, text='￥ ' + str(self.price), style="ItemDetailPriceFont.TLabel")
        price_value_label.pack(side='left', padx=(0, 0), pady=(5, 5))
        price_frame.pack(side='top', padx=(0,40), pady=(5,5))

        time_frame = tk.Frame(self.attributes_frame)
        time_label = ttk.Label(time_frame, text="发布时间", style="AttributesFont.TLabel")
        time_label.pack(side='left', padx=(40,30), pady=(0,5))
        time_value_label = ttk.Label(time_frame, text=self.upload_time, style="TimeFont.TLabel")
        time_value_label.pack(side='left', padx=(25,0), pady=(0,5))
        time_frame.pack(side='top', padx=(0,40), pady=(5,5))

        tag_frame = tk.Frame(self.attributes_frame)
        tag_label = ttk.Label(tag_frame, text="物品标签", style="AttributesFont.TLabel")
        tag_label.pack(side='left', padx=(0,80), pady=(0,5))
        tag_value_label = ttk.Label(tag_frame, text=self.category, style="TimeFont.TLabel")
        tag_value_label.pack(side='left', padx=(0,0), pady=(0,5))
        tag_frame.pack(side='top', padx=(0,40), pady=(5,5))

        desc_frame = tk.Frame(self.attributes_frame)
        description_label = ttk.Label(desc_frame, text="物品描述", style="AttributesFont.TLabel")
        description_label.pack(side='left', padx=(0,20), pady=(0,10))
        description_text = tk.Text(desc_frame, height=15, width=25)
        description_text.insert('end', self.description)
        description_text.config(state='disabled')
        description_text.pack(side='left', padx=(20,0), pady=(0,5))
        desc_frame.pack(side='top', padx=(60,0), pady=(5,10))

class ScrollFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.root = master
        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.horizontal_scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.horizontal_scrollbar.pack(side='bottom', fill='x')

        self.canvas.configure(xscrollcommand=self.horizontal_scrollbar.set, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=True)

        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.frame.bind("<Configure>", self.on_frame_configure)
        self.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.bind_all("<Button-4>", self.scroll_up)
        self.bind_all("<Button-5>", self.scroll_down)

        self.button_font_style = ttk.Style()
        self.button_font_style.theme_use('default')
        self.button_font_style.configure('ButtonFont.TButton', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        self.theme_font_style = ttk.Style()
        self.theme_font_style.theme_use('default')
        self.theme_font_style.configure('ThemeFont.TLabel', font=("方正像素12", 18), background='#f0f0f0')

        self.tag_font_style = ttk.Style()
        self.tag_font_style.theme_use("default")
        self.tag_font_style.configure('TagFont.TButton', font=("方正像素12", 12), padding=1, thickness=10, relief='flat')
        self.tag_font_style.map("TagFont.TButton",
                           foreground=[('!active', '#333333'), ('pressed', 'white'), ('active', 'white')],
                           background=[('!active', 'white'), ('pressed', '#d9b756'), ('active', '#d9b756')])

        self.create_labels()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def scroll_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def scroll_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def create_labels(self):
        self.title_frame = tk.Frame(self.frame)
        self.title_frame.pack(side='top', anchor='w',pady=(5, 0))
        self.items_frame = tk.Frame(self.frame)
        self.items_frame.pack(side='top', anchor='w',pady=(5, 0))
        rectangle = tk.Label(self.title_frame, bg='#d9b756', width=1, height=2)
        rectangle.pack(side='left', padx=(5, 10), pady=5)

class PublishFrame(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.root = master
        self.images_folder = "images"
        self.upload_image_path = None
        self.default_photo = None
        self.username = username
        self.tittle_frame = tk.Frame(self)
        self.upload_frame = tk.Frame(self)
        self.image_frame = tk.Frame(self.upload_frame)
        self.attributes_frame = tk.Frame(self.upload_frame)

    def create_labels(self):
        self.tittle_font_style = ttk.Style()
        self.tittle_font_style.theme_use('default')
        self.tittle_font_style.configure('TittleFont.TLabel', font=('方正小标宋_GBK', 22), background='#f0f0f0')

        self.tittle_frame.pack(side='top', padx=(0, 0), pady=(20, 0))
        self.upload_frame.pack(side='top', padx=(0, 0), pady=(0, 5))

        self.button_font_style = ttk.Style()
        self.button_font_style.theme_use('default')
        self.button_font_style.configure('ButtonFont.TButton', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        self.image_label_frame = tk.Frame(self.image_frame)
        self.image_label = tk.Label(self.image_label_frame, image=self.default_photo, width=300, height=400)
        self.image_label.pack(side='left', padx=(10, 0), pady=(0, 0))
        self.image_label_frame.pack(side='top', padx=(20, 0), pady=(0, 0))

        self.upload_button_frame = tk.Frame(self.image_frame)
        self.upload_button = ttk.Button(self.upload_button_frame, text="上传图片", command=self.upload_image,
                                        style='ButtonFont.TButton', takefocus=False)
        self.upload_button.pack(side='left', padx=(10, 0), pady=(0, 1))
        self.upload_button_frame.pack(side='top', padx=(20, 0), pady=(0, 1))

        self.image_frame.pack(side='left', padx=(10, 10), pady=(0, 0))

        self.attributes_font_style = ttk.Style()
        self.attributes_font_style.theme_use('default')
        self.attributes_font_style.configure('AttributesFont.TLabel', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        self.name_frame = tk.Frame(self.attributes_frame)
        self.name_label = ttk.Label(self.name_frame, text="物品名称", style="AttributesFont.TLabel")
        self.name_label.pack(side='left', padx=(5, 55), pady=(5, 5))
        self.name_entry = tk.Entry(self.name_frame)
        self.name_entry.pack(side='left', padx=(0, 0), pady=(5, 5))
        self.name_frame.pack(side='top', padx=(0, 40), pady=(5, 5))

        self.price_frame = tk.Frame(self.attributes_frame)
        self.price_label = ttk.Label(self.price_frame, text="物品价格", style="AttributesFont.TLabel")
        self.price_label.pack(side='left', padx=(5, 55), pady=(0, 5))
        self.price_entry = tk.Entry(self.price_frame)
        self.price_entry.pack(side='left', padx=(0, 0), pady=(0, 5))
        self.price_frame.pack(side='top', padx=(0, 40), pady=(5, 5))

        self.tag_var = tk.StringVar()
        self.tag_frame = tk.Frame(self.attributes_frame)
        self.tag_label = ttk.Label(self.tag_frame, text="物品标签", style="AttributesFont.TLabel")
        self.tag_label.pack(side='left', padx=(18, 58), pady=(0, 5))
        self.tag_options = self.check_categories()
        self.tag_dropdown = ttk.Combobox(self.tag_frame, textvariable=self.tag_var, values=self.tag_options,
                                         state='readonly', takefocus=False)
        self.tag_dropdown.set("选择")
        self.tag_dropdown.pack(side='left', padx=(0, 0), pady=(0, 5))
        self.tag_frame.pack(side='top', padx=(0, 40), pady=(5, 5))

        self.desc_frame = tk.Frame(self.attributes_frame)
        self.description_label = ttk.Label(self.desc_frame, text="物品描述", style="AttributesFont.TLabel")
        self.description_label.pack(side='left', padx=(0, 55), pady=(0, 10))
        self.description_text = tk.Text(self.desc_frame, height=15, width=30)
        self.description_text.pack(side='left', padx=(0, 0), pady=(0, 5))
        self.desc_frame.pack(side='top', padx=(30, 0), pady=(5, 10))

        self.submit_button_frame = tk.Frame(self.attributes_frame)
        self.submit_button = ttk.Button(self.submit_button_frame, text="提交", command=self.submit_item,
                                        style='ButtonFont.TButton', takefocus=False)
        self.submit_button.pack(side='top', padx=(20, 0), pady=(0, 0))
        self.submit_button_frame.pack(side='top', padx=(10, 0), pady=(35, 10))

        self.attributes_frame.pack(side='left', padx=(40, 10), pady=(50, 10))

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="选择图片",
                                               filetypes=(
                                               ("Image Files", "*.png;*.jpg;*.jpeg;*.gif"), ("All Files", "*.*")))
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((300, 300))
            self.photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo
            self.upload_image_path = file_path

    def check_categories(self):
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cursor = connection.cursor()
        query = ''' SELECT category FROM categories '''
        cursor.execute(query)
        categories = cursor.fetchall()
        category_list = []
        for category in categories:
            if category[0] == '#其他':
                continue
            category_list.append(category[0])
        category_list.append('#其他')
        return category_list

    def submit_item(self):
        pass

    def reset_form(self):
        self.name_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.description_text.delete("1.0", 'end')
        self.tag_dropdown.set("选择")
        self.image_label.config(image=self.default_photo)
        self.upload_image_path = None

class ManageFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.root = master

        self.theme_font_style = ttk.Style()
        self.theme_font_style.theme_use('default')
        self.theme_font_style.configure('ThemeFont.TLabel', font=("方正像素12", 18), background='#f0f0f0')
        self.button_font_style = ttk.Style()
        self.button_font_style.theme_use('default')
        self.button_font_style.configure('ButtonFont.TButton', font=('方正小标宋_GBK', 11), background='#f0f0f0')
        self.font_style = ttk.Style()
        self.font_style.theme_use('default')
        self.font_style.configure('NormalFont.TLabel', font=("方正像素12", 12), background='#f0f0f0')
        # 标题
        self.title_frame = tk.Frame(self)
        self.title_frame.pack(side='top', anchor='w', pady=(5, 0))
        self.rectangle = tk.Label(self.title_frame, bg='#d9b756', width=1, height=2)
        self.rectangle.pack(side='left', padx=(5, 10), pady=5)

import tkinter as tk
import pyglet

from datetime import datetime
from tkinter import ttk
from PIL import Image, ImageTk
from utilities_new import resource_path


class AvailableItemDetailFrame(tk.Frame):
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

        pyglet.font.add_file(resource_path('fonts/方正小标宋_GBK.TTF'))
        pyglet.font.load('方正小标宋_GBK')

        dt = datetime.strptime(str(self.upload_time), "%Y%m%d%H%M%S")
        self.upload_time = dt.strftime("%Y.%m.%d %H:%M")

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
        tittle_font_style.configure('TittleFont.TLabel', font=('方正小标宋_GBK', 22), background='#f0f0f0', wraplength=600)


        self.tittle_label = ttk.Label(self.tittle_frame, text=self.name, style="TittleFont.TLabel")
        self.tittle_label.pack(side='left', padx=(0, 5), pady=(0, 5))
        self.tittle_frame.pack(side='top', padx=(0, 0), pady=(20, 0))
        self.detail_frame.pack(side='top', padx=(0, 0), pady=(0, 5))

        button_font_style = ttk.Style()
        button_font_style.theme_use('default')
        button_font_style.configure('ButtonFont.TButton', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        self.image_label_frame = tk.Frame(self.image_frame)
        self.image_label = tk.Label(self.image_label_frame, image=self.photo, width=300, height=400)
        self.image_label.image = self.photo
        self.image_label.pack(side='left', padx=(10,0),pady=(0,0))
        self.image_label_frame.pack(side='top', padx=(20,0), pady=(0,0))

        self.upload_button_frame = tk.Frame(self.image_frame)
        self.upload_button = ttk.Button(self.upload_button_frame, text="收藏物品", style='ButtonFont.TButton', takefocus=False)
        self.upload_button.pack(side='left', padx=(10,0),pady=(0,1))
        self.upload_button_frame.pack(side='top', padx=(20,0), pady=(0,1))

        self.image_frame.pack(side='left', padx=(10, 10), pady=(0, 0))

        attributes_font_style = ttk.Style()
        attributes_font_style.theme_use('default')
        attributes_font_style.configure('AttributesFont.TLabel', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        item_detail_price_font_style = ttk.Style()
        item_detail_price_font_style.theme_use('default')
        item_detail_price_font_style.configure('ItemDetailPriceFont.TLabel', font=('方正小标宋_GBK', 11),
                                               background='#f0f0f0',
                                               foreground='red', width=10)

        self.price_frame = tk.Frame(self.attributes_frame)
        self.price_label = ttk.Label(self.price_frame, text="物品价格", style="AttributesFont.TLabel")
        self.price_label.pack(side='left', padx=(40,70), pady=(5,5))
        self.price_value_label = ttk.Label(self.price_frame, text='￥ ' + str(self.price), style="ItemDetailPriceFont.TLabel")
        self.price_value_label.pack(side='left', padx=(0, 0), pady=(5, 5))
        self.price_frame.pack(side='top', padx=(0,40), pady=(5,5))

        time_font_style = ttk.Style()
        time_font_style.theme_use('default')
        time_font_style.configure('TimeFont.TLabel', font=('方正小标宋_GBK', 10), background='#f0f0f0', foreground='#777674')

        self.time_frame = tk.Frame(self.attributes_frame)
        self.time_label = ttk.Label(self.time_frame, text="发布时间", style="AttributesFont.TLabel")
        self.time_label.pack(side='left', padx=(40,30), pady=(0,5))
        self.time_value_label = ttk.Label(self.time_frame, text=self.upload_time, style="TimeFont.TLabel")
        self.time_value_label.pack(side='left', padx=(25,0), pady=(0,5))
        self.time_frame.pack(side='top', padx=(0,40), pady=(5,5))

        self.tag_frame = tk.Frame(self.attributes_frame)
        self.tag_label = ttk.Label(self.tag_frame, text="物品标签", style="AttributesFont.TLabel")
        self.tag_label.pack(side='left', padx=(0,80), pady=(0,5))
        self.tag_value_label = ttk.Label(self.tag_frame, text=self.category, style="TimeFont.TLabel")
        self.tag_value_label.pack(side='left', padx=(0,0), pady=(0,5))
        self.tag_frame.pack(side='top', padx=(0,40), pady=(5,5))

        self.desc_frame = tk.Frame(self.attributes_frame)
        self.description_label = ttk.Label(self.desc_frame, text="物品描述", style="AttributesFont.TLabel")
        self.description_label.pack(side='left', padx=(0,20), pady=(0,10))
        self.description_text = tk.Text(self.desc_frame, height=15, width=25)
        self.description_text.insert('end', self.description)
        self.description_text.config(state='disabled')
        self.description_text.pack(side='left', padx=(20,0), pady=(0,5))
        self.desc_frame.pack(side='top', padx=(60,0), pady=(5,10))

        self.submit_button_frame = tk.Frame(self.attributes_frame)
        self.submit_button = ttk.Button(self.submit_button_frame, text="我想要", style='ButtonFont.TButton', takefocus=False)
        self.submit_button.pack(side='top', padx=(20, 0), pady=(0, 0))
        self.submit_button_frame.pack(side='top', padx=(10,0), pady=(35,10))

        self.attributes_frame.pack(side='left', padx=(40, 10), pady=(50, 10))

class WantingItemDetailFrame(tk.Frame):
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
        tittle_font_style.configure('TittleFont.TLabel', font=('方正小标宋_GBK', 22), background='#f0f0f0', wraplength=600)


        self.tittle_label = ttk.Label(self.tittle_frame, text=self.name, style="TittleFont.TLabel")
        self.tittle_label.pack(side='left', padx=(0, 5), pady=(0, 5))
        self.tittle_frame.pack(side='top', padx=(0, 0), pady=(20, 0))
        self.detail_frame.pack(side='top', padx=(0, 0), pady=(0, 5))

        button_font_style = ttk.Style()
        button_font_style.theme_use('default')
        button_font_style.configure('ButtonFont.TButton', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        self.image_label_frame = tk.Frame(self.image_frame)
        self.image_label = tk.Label(self.image_label_frame, image=self.photo, width=300, height=400)
        self.image_label.image = self.photo
        self.image_label.pack(side='left', padx=(10,0),pady=(0,0))
        self.image_label_frame.pack(side='top', padx=(20,0), pady=(0,0))

        self.upload_button_frame = tk.Frame(self.image_frame)
        self.upload_button = ttk.Button(self.upload_button_frame, text="收藏物品", style='ButtonFont.TButton', takefocus=False)
        self.upload_button.pack(side='left', padx=(10,0),pady=(0,1))
        self.upload_button_frame.pack(side='top', padx=(20,0), pady=(0,1))

        self.image_frame.pack(side='left', padx=(10, 10), pady=(0, 0))

        attributes_font_style = ttk.Style()
        attributes_font_style.theme_use('default')
        attributes_font_style.configure('AttributesFont.TLabel', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        item_detail_price_font_style = ttk.Style()
        item_detail_price_font_style.theme_use('default')
        item_detail_price_font_style.configure('ItemDetailPriceFont.TLabel', font=('方正小标宋_GBK', 11), background='#f0f0f0',
                                        foreground='red', width=10)

        self.price_frame = tk.Frame(self.attributes_frame)
        self.price_label = ttk.Label(self.price_frame, text="物品价格", style="AttributesFont.TLabel")
        self.price_label.pack(side='left', padx=(40,70), pady=(5,5))
        self.price_value_label = ttk.Label(self.price_frame, text='￥ ' + str(self.price), style="ItemDetailPriceFont.TLabel")
        self.price_value_label.pack(side='left', padx=(0, 0), pady=(5, 5))
        self.price_frame.pack(side='top', padx=(0,40), pady=(5,5))

        time_font_style = ttk.Style()
        time_font_style.theme_use('default')
        time_font_style.configure('TimeFont.TLabel', font=('方正小标宋_GBK', 10), background='#f0f0f0', foreground='#777674')

        self.time_frame = tk.Frame(self.attributes_frame)
        self.time_label = ttk.Label(self.time_frame, text="发布时间", style="AttributesFont.TLabel")
        self.time_label.pack(side='left', padx=(40,30), pady=(0,5))
        self.time_value_label = ttk.Label(self.time_frame, text=self.upload_time, style="TimeFont.TLabel")
        self.time_value_label.pack(side='left', padx=(25,0), pady=(0,5))
        self.time_frame.pack(side='top', padx=(0,40), pady=(5,5))

        self.tag_frame = tk.Frame(self.attributes_frame)
        self.tag_label = ttk.Label(self.tag_frame, text="物品标签", style="AttributesFont.TLabel")
        self.tag_label.pack(side='left', padx=(0,80), pady=(0,5))
        self.tag_value_label = ttk.Label(self.tag_frame, text=self.category, style="TimeFont.TLabel")
        self.tag_value_label.pack(side='left', padx=(0,0), pady=(0,5))
        self.tag_frame.pack(side='top', padx=(0,40), pady=(5,5))

        self.desc_frame = tk.Frame(self.attributes_frame)
        self.description_label = ttk.Label(self.desc_frame, text="物品描述", style="AttributesFont.TLabel")
        self.description_label.pack(side='left', padx=(0,20), pady=(0,10))
        self.description_text = tk.Text(self.desc_frame, height=15, width=25)
        self.description_text.insert('end', self.description)
        self.description_text.config(state='disabled')
        self.description_text.pack(side='left', padx=(20,0), pady=(0,5))
        self.desc_frame.pack(side='top', padx=(60,0), pady=(5,10))

        self.submit_button_frame = tk.Frame(self.attributes_frame)
        self.submit_button = ttk.Button(self.submit_button_frame, text="我有", style='ButtonFont.TButton', takefocus=False)
        self.submit_button.pack(side='top', padx=(20, 0), pady=(0, 0))
        self.submit_button_frame.pack(side='top', padx=(10,0), pady=(35,10))

        self.attributes_frame.pack(side='left', padx=(40, 10), pady=(50, 10))


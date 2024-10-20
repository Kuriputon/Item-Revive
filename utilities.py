import tkinter as tk
import sqlite3
import pyglet
import os

from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from item_detail import AvailableItemDetailFrame, WantingItemDetailFrame
from utilities_new import resource_path
from my_item import MyItemFrame
from item_edit import ItemDetailEditFrame


pyglet.font.add_file(resource_path('fonts/方正小标宋_GBK.TTF'))
pyglet.font.load('方正小标宋_GBK')

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

class HoverPlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="", is_password=False, **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.is_password = is_password
        self.config(foreground="black")
        if self.is_password:
            self.config(show='*')
        self.is_placeholder_shown = False

        self.bind("<Enter>", self.show_placeholder)
        self.bind("<Leave>", self.clear_placeholder)
        self.bind("<FocusIn>", self.clear_placeholder)
        self.bind("<FocusOut>", self.on_focus_out)

    def show_placeholder(self, event):
        if not self.get() and not self.is_placeholder_shown:
            self.config(foreground="gray")
            self.insert(0, self.placeholder)
            if self.is_password:
                self.config(show='')
            self.is_placeholder_shown = True

    def clear_placeholder(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(foreground="black")
            if self.is_password:
                self.config(show='*')
            self.is_placeholder_shown = False

    def on_focus_out(self, event):
        if not self.get():
            self.show_placeholder(event)

    def reset_entry(self, event):
        if self.is_password:
            self.config(foreground="black", show='*')
        else:
            self.config(foreground="black", show='')

def load_and_crop_image(image_path, target_width, target_height):
    img = Image.open(image_path)

    scale_width = target_width / img.width
    scale_height = target_height / img.height
    scale = max(scale_width, scale_height)

    new_size = (int(img.width * scale), int(img.height * scale))
    img = img.resize(new_size, Image.LANCZOS)

    left = (img.width - target_width) / 2
    top = (img.height - target_height) / 2
    right = (img.width + target_width) / 2
    bottom = (img.height + target_height) / 2

    img = img.crop((left, top, right, bottom))

    return ImageTk.PhotoImage(img)

def create_item_frames(frame, row):
    row_item_frames = []
    item_frames = []

    item_frame_style = ttk.Style()
    item_frame_style.theme_use('default')
    item_frame_style.configure('ItemFrame.TFrame', background='white')

    row_frame_style = ttk.Style()
    row_frame_style.theme_use('default')
    row_frame_style.configure('RowFrame.TFrame', background='#f0f0f0')

    for i in range(row):
        row_item_frame = ttk.Frame(frame, style="RowFrame.TFrame")
        row_item_frame.pack(side='top', fill='x', padx=(5, 5), pady=(5, 5))
        row_item_frames.append(row_item_frame)
        for j in range(4):
            item_frame = ttk.Frame(row_item_frame, style="ItemFrame.TFrame")
            item_frame.pack(side=tk.LEFT, padx=(5, 5), pady=(0, 5))
            item_frames.append(item_frame)
    return row_item_frames, item_frames

def create_item_labels(item_frame, item_id, image_path, item_name, item_tag, item_price, frames):
    detail_frame_name = "detail_frame_"+str(item_id)
    item_image_frame = tk.Frame(item_frame, background='white')
    item_image_frame.pack(side='top', pady=(5, 0))
    image = load_and_crop_image(image_path, 150, 150)
    image_label = tk.Label(item_image_frame, image=image, height=150, width=150)
    image_label.image = image
    image_label.pack(side='top', padx=(5, 5), pady=(0, 0))
    image_label.bind("<Button-1>", lambda e: show_frame(frames, detail_frame_name))
    image_label.bind("<Enter>", lambda e: image_label.config(cursor="hand2"))

    item_name_font_style = ttk.Style()
    item_name_font_style.theme_use('default')
    item_name_font_style.configure('ItemNameFont.TLabel', font=('方正小标宋_GBK', 11), background='white')

    item_name_frame = tk.Frame(item_frame, background='white')
    item_name_frame.pack(side='top', pady=(0, 1), fill='x')
    item_name_label = ttk.Label(item_name_frame, text=item_name, style='ItemNameFont.TLabel')
    item_name_label.pack(side='left', padx=(5, 0), pady=(0, 0))

    item_tag_frame = tk.Frame(item_frame, background='white')
    item_tag_frame.pack(side='top', pady=(0, 1), fill='x')
    item_tag_font_style = ttk.Style()
    item_tag_font_style.theme_use('default')
    item_tag_font_style.configure('ItemTagFont.TLabel', font=('方正小标宋_GBK', 10), background='white',
                                  foreground='#777674')
    item_tag_label = ttk.Label(item_tag_frame, text=item_tag, style='ItemTagFont.TLabel', width=10)
    item_tag_label.pack(side='left', padx=(5, 0), pady=(0, 0))

    item_price_frame = tk.Frame(item_frame, background='white')
    item_price_frame.pack(side='top', pady=(0, 1), fill='x')
    item_price_font_style = ttk.Style()
    item_price_font_style.theme_use('default')
    item_price_font_style.configure('ItemPriceFont.TLabel', font=('方正小标宋_GBK', 11), background='white',
                                    foreground='red')
    item_price_label = ttk.Label(item_price_frame, text='￥ ' + item_price, style='ItemPriceFont.TLabel')
    item_price_label.pack(side='left', padx=(5, 0), pady=(0, 0))


def create_item_widgets(frame, row, status, frames):
    row_item_frames, item_frames = create_item_frames(frame, row)
    item_status = status
    connection = sqlite3.connect(resource_path('databases/items.db'))
    cursor = connection.cursor()
    query = '''
        SELECT id, name, category, description, image_path, upload_time, uploaded_by, price 
        FROM items
        WHERE status = ? 
        ORDER BY upload_time DESC;
    '''
    cursor.execute(query, (item_status,))
    items = cursor.fetchall()
    item_lists = []
    for item in items:
        item_lists.append(item)
    for i in range(len(item_frames)):
        if i < len(item_lists):
            item_id, name, category, description, image_path, upload_time, uploaded_by, price = item_lists[i]
            if len(name) > 8:
                name = name[:8] + "……"
            if image_path == None:
                create_item_labels(item_frames[i], item_id, resource_path("images/configs/default_wanting_image.jpg"), name, category, str(price), frames)
            else:
                create_item_labels(item_frames[i], item_id, resource_path(image_path), name, category, str(price), frames)
    connection.close()

def show_frame(frames, frame_name):
    for frame in frames.values():
        frame.pack_forget()
    frame = frames[frame_name]
    frame.pack(fill='both', expand=True)

def create_user_publish_item_labels(item_frame, item_id, image_path, item_name, item_tag, item_price, frames):
    detail_frame_name = "user_publish_frame_"+str(item_id)
    item_image_frame = tk.Frame(item_frame, background='white')
    item_image_frame.pack(side='top', pady=(5, 0))
    image = load_and_crop_image(image_path, 150, 150)
    image_label = tk.Label(item_image_frame, image=image, height=150, width=150)
    image_label.image = image
    image_label.pack(side='top', padx=(5, 5), pady=(0, 0))
    image_label.bind("<Button-1>", lambda e: show_frame(frames, detail_frame_name))
    image_label.bind("<Enter>", lambda e: image_label.config(cursor="hand2"))

    item_name_font_style = ttk.Style()
    item_name_font_style.theme_use('default')
    item_name_font_style.configure('ItemNameFont.TLabel', font=('方正小标宋_GBK', 11), background='white')

    item_name_frame = tk.Frame(item_frame, background='white')
    item_name_frame.pack(side='top', pady=(0, 1), fill='x')
    item_name_label = ttk.Label(item_name_frame, text=item_name, style='ItemNameFont.TLabel')
    item_name_label.pack(side='left', padx=(5, 0), pady=(0, 0))

    item_tag_frame = tk.Frame(item_frame, background='white')
    item_tag_frame.pack(side='top', pady=(0, 1), fill='x')
    item_tag_font_style = ttk.Style()
    item_tag_font_style.theme_use('default')
    item_tag_font_style.configure('ItemTagFont.TLabel', font=('方正小标宋_GBK', 10), background='white',
                                  foreground='#777674')
    item_tag_label = ttk.Label(item_tag_frame, text=item_tag, style='ItemTagFont.TLabel', width=10)
    item_tag_label.pack(side='left', padx=(5, 0), pady=(0, 0))

    item_price_frame = tk.Frame(item_frame, background='white')
    item_price_frame.pack(side='top', pady=(0, 1), fill='x')
    item_price_font_style = ttk.Style()
    item_price_font_style.theme_use('default')
    item_price_font_style.configure('ItemPriceFont.TLabel', font=('方正小标宋_GBK', 11), background='white',
                                    foreground='red')
    item_price_label = ttk.Label(item_price_frame, text='￥ ' + item_price, style='ItemPriceFont.TLabel')
    item_price_label.pack(side='left', padx=(5, 0), pady=(0, 0))


def create_item_detail_frames(root, status):
    item_status = status
    detail_frames = {}

    connection = sqlite3.connect(resource_path('databases/items.db'))
    cursor = connection.cursor()
    query = '''
            SELECT id, name, category, description, image_path, upload_time, uploaded_by, price 
            FROM items
            WHERE status = ? 
            ORDER BY upload_time DESC;
        '''
    cursor.execute(query, (item_status,))
    items = cursor.fetchall()
    item_lists = []
    for item in items:
        item_lists.append(item)
    for i in range(len(item_lists)):
        item_id, name, category, description, image_path, upload_time, uploaded_by, price = item_lists[i]
        if item_status == "闲置中":
            item_detail_frame = AvailableItemDetailFrame(root, item_id, name, category, description, resource_path(image_path), upload_time, uploaded_by, price)
            key_name = "detail_frame_"+str(item_id)
            detail_frames[key_name] = item_detail_frame
        elif item_status == "求物中":
            if image_path:
                item_detail_frame = WantingItemDetailFrame(root, item_id, name, category, description, resource_path(image_path), upload_time, uploaded_by, price)
            else:
                item_detail_frame = WantingItemDetailFrame(root, item_id, name, category, description,
                                                           resource_path("images/configs/default_wanting_image.jpg"), upload_time,
                                                           uploaded_by, price)
            key_name = "detail_frame_"+str(item_id)
            detail_frames[key_name] = item_detail_frame
    return detail_frames

def check_user_items(username):
    connection = sqlite3.connect(resource_path('databases/items.db'))
    cursor = connection.cursor()
    query = '''
                SELECT id, name, category, description, image_path, upload_time, uploaded_by, price, status
                FROM items
                WHERE uploaded_by = ? 
                ORDER BY upload_time DESC;
            '''
    cursor.execute(query, (username,))
    items = cursor.fetchall()
    item_list = []
    item_count = 0
    for item in items:
        item_list.append(item)
        item_count += 1
    row_number = item_count // 4
    if row_number==0:
        row_number=1
    return item_list, row_number

def create_my_published_widgets(frame, username, frames):
    item_list, row_number = check_user_items(username)
    row_item_frames, item_frames = create_item_frames(frame, row_number)
    for i in range(len(item_frames)):
        if i < len(item_list):
            item_id, name, category, description, image_path, upload_time, uploaded_by, price, status = item_list[i]
            if len(name) > 8:
                name = name[:8] + "……"
            if image_path == None:
                create_user_publish_item_labels(item_frames[i], item_id, resource_path("images/configs/default_wanting_image.jpg"), name, category, str(price), frames)
            else:
                create_user_publish_item_labels(item_frames[i], item_id, resource_path(image_path), name, category, str(price), frames)
    return item_list, row_number

def create_my_publish_item_detail_frames(root, frames, item_list):
    detail_frames = {}
    for i in range(len(item_list)):
        item_id, name, category, description, image_path, upload_time, uploaded_by, price, status = item_list[i]
        if status == "闲置中":
            item_detail_frame = MyItemFrame(root, frames, item_id, name, category, description, resource_path(image_path), upload_time, uploaded_by, price, status)
            key_name = "user_publish_frame_"+str(item_id)
            detail_frames[key_name] = item_detail_frame
        elif status == "求物中":
            if image_path:
                item_detail_frame = MyItemFrame(root, frames, item_id, name, category, description, resource_path(image_path), upload_time, uploaded_by, price, status)
            else:
                item_detail_frame = MyItemFrame(root, frames, item_id, name, category, description,
                                                           resource_path("images/configs/default_wanting_image.jpg"), upload_time,
                                                           uploaded_by, price, status)
            key_name = "user_publish_frame_"+str(item_id)
            detail_frames[key_name] = item_detail_frame
    return detail_frames

def create_my_publish_item_edit_frames(root, item_list):
    edit_frames = {}
    for i in range(len(item_list)):
        item_id, name, category, description, image_path, upload_time, uploaded_by, price, status = item_list[i]
        if status == "闲置中":
            item_detail_frame = ItemDetailEditFrame(root, item_id, name, category, description, resource_path(image_path), upload_time, uploaded_by, price, status)
            key_name = "user_publish_edit_frame_"+str(item_id)
            edit_frames[key_name] = item_detail_frame
        elif status == "求物中":
            if image_path:
                item_detail_frame = ItemDetailEditFrame(root, item_id, name, category, description, resource_path(image_path), upload_time, uploaded_by, price, status)
            else:
                item_detail_frame = ItemDetailEditFrame(root, item_id, name, category, description,
                                                           resource_path("images/configs/default_wanting_image.jpg"), upload_time,
                                                           uploaded_by, price, status)
            key_name = "user_publish_edit_frame_"+str(item_id)
            edit_frames[key_name] = item_detail_frame
    return edit_frames

def check_items(status):
    connection = sqlite3.connect(resource_path('databases/items.db'))
    cursor = connection.cursor()
    query = '''
                SELECT id, name, category, description, image_path, upload_time, uploaded_by, price, status
                FROM items
                WHERE status = ? 
                ORDER BY upload_time DESC;
            '''
    cursor.execute(query, (status,))
    items = cursor.fetchall()
    item_list = []
    item_count = 0
    for item in items:
        item_list.append(item)
        item_count += 1
    row_number = (item_count // 4)+1
    return item_list, row_number

def like_search(keyword):
    connection = sqlite3.connect(resource_path('databases/items.db'))
    cursor = connection.cursor()
    query = '''
                            SELECT id, name, category, description, image_path, upload_time, uploaded_by, price, status
                            FROM items
                            WHERE name LIKE ? 
                            ORDER BY upload_time DESC;
                        '''
    cursor.execute(query, ('%'+keyword+'%',))
    items = cursor.fetchall()
    connection.close()

    item_list = []
    item_count = 0
    for item in items:
        item_list.append(item)
        item_count += 1
    row_number = item_count // 4
    if row_number == 0:
        row_number = 1
    return item_list, row_number

def create_item_widgets_from_list(frame, row_number, item_list, frames):
    row_item_frames, item_frames = create_item_frames(frame, row_number)
    for i in range(len(item_frames)):
        if i < len(item_list):
            item_id, name, category, description, image_path, upload_time, uploaded_by, price, status = item_list[i]
            if len(name) > 8:
                name = name[:8] + "……"
            if image_path == None:
                create_item_labels(item_frames[i], item_id, resource_path("images/configs/default_wanting_image.jpg"), name, category, str(price), frames)
            else:
                create_item_labels(item_frames[i], item_id, resource_path(image_path), name, category, str(price), frames)

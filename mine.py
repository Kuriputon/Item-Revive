import tkinter as tk
import pyglet

from tkinter import ttk
from utilities import create_my_published_widgets, resource_path, create_my_publish_item_detail_frames,create_my_publish_item_edit_frames

class MyPublishedFrame(tk.Frame):   # 我的界面
    def __init__(self, master, frames, username):
        super().__init__(master)
        self.root = master
        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)
        self.frames = frames
        self.username = username

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

        pyglet.font.add_file(resource_path('fonts/方正像素12.TTF'))
        pyglet.font.load('方正像素12')

        self.item_list = self.create_my_published_labels()
        item_frames = create_my_publish_item_detail_frames(self.root, self.frames, self.item_list)
        self.frames.update(item_frames)
        item_edit_frames = create_my_publish_item_edit_frames(self.root, self.item_list)
        self.frames.update(item_edit_frames)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def scroll_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def scroll_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def create_my_published_labels(self):
        theme_font_style = ttk.Style()
        theme_font_style.theme_use('default')
        theme_font_style.configure('ThemeFont.TLabel', font=("方正像素12", 18), background='#f0f0f0')

        title_frame = tk.Frame(self.frame)
        title_frame.pack(side='top', anchor='w',pady=(5, 0))
        rectangle = tk.Label(title_frame, bg='#d9b756', width=1, height=2)
        rectangle.pack(side='left', padx=(5, 10), pady=5)
        tag_label = ttk.Label(title_frame, text='已发布的物品信息', style='ThemeFont.TLabel')
        tag_label.pack(side='left')

        items_frame = tk.Frame(self.frame)
        items_frame.pack(side='top', anchor='w',pady=(5, 0))

        item_list, row = create_my_published_widgets(items_frame, self.username, self.frames)
        return item_list
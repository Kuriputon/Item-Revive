import tkinter as tk
import pyglet

from tkinter import ttk
from utilities import create_item_widgets, resource_path


class PlazaFrame(tk.Frame):   # 广场界面
    def __init__(self, master, frames):
        super().__init__(master)
        self.root = master
        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)
        self.frames = frames

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

        self.create_available_labels()
        self.create_wanting_labels()


    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def scroll_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def scroll_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def create_available_labels(self):
        theme_font_style = ttk.Style()
        theme_font_style.theme_use('default')
        theme_font_style.configure('ThemeFont.TLabel', font=("方正像素12", 18), background='#f0f0f0')

        tag_frame = tk.Frame(self.frame)
        tag_frame.pack(side='top', anchor='w',pady=(5, 0))

        # 分类标签
        tag_title_frame = tk.Frame(tag_frame)
        tag_title_frame.pack(side='top', anchor='w',pady=(0, 0))
        rectangle = tk.Label(tag_title_frame, bg='#d9b756', width=1, height=2)
        rectangle.pack(side='left', padx=(5, 10), pady=5)
        tag_label = ttk.Label(tag_title_frame, text='分类', style='ThemeFont.TLabel')
        tag_label.pack(side='left')

        tags_frame = tk.Frame(tag_frame)
        tags_frame.pack(side='top', anchor='w',pady=(5, 0))

        tag_font_style = ttk.Style()
        tag_font_style.theme_use("default")
        tag_font_style.configure('TagFont.TButton', font=("方正像素12", 12), padding=1, thickness=10, relief = 'flat')
        tag_font_style.map("TagFont.TButton",
                  foreground=[('!active', '#333333'), ('pressed', 'white'), ('active', 'white')],
                  background=[('!active', 'white'), ('pressed', '#d9b756'), ('active', '#d9b756')]
                  )
        book_tag = ttk.Button(tags_frame, text='#书籍', style='TagFont.TButton', width=6, cursor='hand2', takefocus=False)
        book_tag.pack(side='left', padx=(30, 5), pady=(0,5))

        digital_tag = ttk.Button(tags_frame, text='#数码', style='TagFont.TButton', width=6, cursor='hand2', takefocus=False)
        digital_tag.pack(side='left', padx=(10, 5), pady=(0,5))

        house_tag = ttk.Button(tags_frame, text='#居家', style='TagFont.TButton', width=6, cursor='hand2', takefocus=False)
        house_tag.pack(side='left', padx=(10, 5), pady=(0, 5))

        food_tag = ttk.Button(tags_frame, text='#食品', style='TagFont.TButton', width=6, cursor='hand2', takefocus=False)
        food_tag.pack(side='left', padx=(10, 5), pady=(0, 5))

        clothes_tag = ttk.Button(tags_frame, text='#衣饰', style='TagFont.TButton', width=6, cursor='hand2', takefocus=False)
        clothes_tag.pack(side='left', padx=(10, 5), pady=(0, 5))

        shoes_tag = ttk.Button(tags_frame, text='#鞋包', style='TagFont.TButton', width=6, cursor='hand2', takefocus=False)
        shoes_tag.pack(side='left', padx=(10, 5), pady=(0, 5))

        sports_tag = ttk.Button(tags_frame, text='#运动', style='TagFont.TButton', width=6, cursor='hand2', takefocus=False)
        sports_tag.pack(side='left', padx=(10, 5), pady=(0, 5))

        study_tag = ttk.Button(tags_frame, text='#文具', style='TagFont.TButton', width=6, cursor='hand2', takefocus=False)
        study_tag.pack(side='left', padx=(10, 5), pady=(0, 5))

        goods_tag = ttk.Button(tags_frame, text='#周边', style='TagFont.TButton', width=6, cursor='hand2', takefocus=False)
        goods_tag.pack(side='left', padx=(10, 5), pady=(0, 5))

        others_tag = ttk.Button(tags_frame, text='#其他', style='TagFont.TButton', width=6, cursor='hand2', takefocus=False)
        others_tag.pack(side='left', padx=(10, 5), pady=(0, 5))

        # 闲置标签
        idle_frame = tk.Frame(self.frame)
        idle_frame.pack(side='top',anchor='w',pady=(5, 0))

        idle_title_frame = tk.Frame(idle_frame)
        idle_title_frame.pack(side='top', anchor='w', pady=(0, 0))
        idle_rectangle = tk.Label(idle_title_frame, bg='#d9b756', width=1, height=2)
        idle_rectangle.pack(side='left', padx=(5, 10), pady=5)


        idle_label = ttk.Label(idle_title_frame, text='闲置', style='ThemeFont.TLabel')
        idle_label.pack(side='left')

        idle_item_frames = tk.Frame(idle_frame)
        idle_item_frames.pack(side='top',pady=(5, 0))

        create_item_widgets(idle_item_frames, 2, "闲置中", self.frames)

    def create_wanting_labels(self):
        theme_font_style = ttk.Style()
        theme_font_style.theme_use('default')
        theme_font_style.configure('ThemeFont.TLabel', font=("方正像素12", 18), background='#f0f0f0')

        tag_font_style = ttk.Style()
        tag_font_style.theme_use("default")
        tag_font_style.configure('TagFont.TButton', font=("方正像素12", 12), padding=1, thickness=10, relief='flat')
        tag_font_style.map("TagFont.TButton",
                           foreground=[('!active', '#333333'), ('pressed', 'white'), ('active', 'white')],
                           background=[('!active', 'white'), ('pressed', '#d9b756'), ('active', '#d9b756')]
                           )

        wanting_frame = tk.Frame(self.frame)
        wanting_frame.pack(side='top', anchor='w', pady=(5, 0))

        wanting_title_frame = tk.Frame(wanting_frame)
        wanting_title_frame.pack(side='top', anchor='w', pady=(0, 0))
        wanting_rectangle = tk.Label(wanting_title_frame, bg='#d9b756', width=1, height=2)
        wanting_rectangle.pack(side='left', padx=(5, 10), pady=5)

        wanting_label = ttk.Label(wanting_title_frame, text='求物', style='ThemeFont.TLabel')
        wanting_label.pack(side='left')

        wanting_item_frames = tk.Frame(wanting_frame)
        wanting_item_frames.pack(side='top', pady=(5, 0))

        create_item_widgets(wanting_item_frames, 2, "求物中", self.frames)













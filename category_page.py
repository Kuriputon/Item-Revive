import tkinter as tk
from tkinter import ttk
from utilities import create_category_item_widgets, create_new_item_detail_frame, category_items
from controller import GetFrames


class CategoryPage(tk.Frame):   # 分类界面
    def __init__(self, master, category):
        super().__init__(master)
        self.root = master
        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)
        self.category = category

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
        theme_font_style = ttk.Style()
        theme_font_style.theme_use('default')
        theme_font_style.configure('ThemeFont.TLabel', font=("方正像素12", 18), background='#f0f0f0')

        button_font_style = ttk.Style()
        button_font_style.theme_use('default')
        button_font_style.configure('ButtonFont.TButton', font=('方正小标宋_GBK', 11), background='#f0f0f0')

        wanting_frame = tk.Frame(self.frame)
        wanting_frame.pack(side='top', anchor='w', pady=(5, 0))

        wanting_title_frame = tk.Frame(wanting_frame)
        wanting_title_frame.pack(side='top', anchor='w', pady=(0, 0))
        wanting_rectangle = tk.Label(wanting_title_frame, bg='#d9b756', width=1, height=2)
        wanting_rectangle.pack(side='left', padx=(5, 10), pady=5)

        wanting_label = ttk.Label(wanting_title_frame, text=self.category, style='ThemeFont.TLabel')
        wanting_label.pack(side='left')

        wanting_item_frames = tk.Frame(wanting_frame)
        wanting_item_frames.pack(side='top', pady=(5, 0))

        self.item_list, row_number = category_items(self.category)
        create_category_item_widgets(wanting_item_frames, row_number, self.category, self.show_item_detail)

    def show_item_detail(self, item_id):
        frame_name = "detail_frame_" + str(item_id)
        get_frames_instance = GetFrames.get_instance()
        frames = get_frames_instance.get_frames()
        frame = create_new_item_detail_frame(self.root, item_id)
        frames.update(frame)
        for frame in frames.values():
            frame.pack_forget()
        frames[frame_name].pack(fill='both', expand=True)
        return

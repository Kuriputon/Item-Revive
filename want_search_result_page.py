import tkinter as tk
import pyglet

from tkinter import ttk
from utilities import resource_path, like_search, create_item_widgets_from_list

class WantResultFrame(tk.Frame):
    def __init__(self, master, frames, keyword, item_list, row_number):
        super().__init__(master)
        self.root = master
        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)
        self.frames = frames

        self.keyword = keyword
        self.item_list = item_list
        self.row_number = row_number

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

        self.keyword_var = tk.StringVar()

        self.create_result_labels()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def scroll_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def scroll_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def create_result_labels(self):
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

        wanting_label = ttk.Label(wanting_title_frame, text='已发布的求物信息', style='ThemeFont.TLabel')
        wanting_label.pack(side='left')

        search_entry = ttk.Entry(wanting_title_frame, width=30, font="Arial 16", textvariable=self.keyword_var,
                                takefocus=False)
        search_entry.insert('end', self.keyword)
        search_entry.pack(side='left', padx=(20, 10))

        search_button = ttk.Button(wanting_title_frame, text="搜索", style='ButtonFont.TButton',
                                   command=self.main_page_search)
        search_button.pack(side='left', padx=(5, 10), pady=5)

        wanting_item_frames = tk.Frame(wanting_frame)
        wanting_item_frames.pack(side='top', pady=(5, 0))
        create_item_widgets_from_list(wanting_item_frames, self.row_number, self.item_list, self.frames)

    def main_page_search(self):
        keyword = self.keyword_var.get()
        item_list, row_number = like_search(keyword)

        self.search_result_frame = WantResultFrame(self.root, self.frames, keyword, item_list, row_number)
        self.frames["search_result_new"] = self.search_result_frame
        self.pack_forget()
        self.search_result_frame.pack(side='left', fill='both', expand=True)

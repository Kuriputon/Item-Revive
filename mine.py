import tkinter as tk
from tkinter import ttk
from utilities import create_my_published_widgets, resource_path, create_new_publish_item_detail_frame
from controller import GetFrames

class MyPublishedFrame(tk.Frame):   # 我的已发布物品界面
    def __init__(self, master, username):
        super().__init__(master)
        self.root = master
        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)
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

        self.item_list = self.create_my_published_labels()

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


        item_list, row = create_my_published_widgets(items_frame, self.username, self.show_item_detail)
        return item_list

    def show_item_detail(self, item_id):
        get_frames_instance = GetFrames.get_instance()
        frames = get_frames_instance.get_frames()
        frame_name = "user_publish_frame_" + str(item_id)
        frame = create_new_publish_item_detail_frame(self.root, item_id)
        frames.update(frame)
        for frame in frames.values():
            frame.pack_forget()
        frames[frame_name].pack(fill='both', expand=True)
        return
import tkinter as tk
from tkinter import ttk
from base_class import ScrollFrame
from utilities import create_item_widgets, create_category_widgets, create_new_item_detail_frame
from controller import GetFrames
from category_page import CategoryPage


class PlazaFrame(ScrollFrame):   # 广场界面
    def __init__(self, master):
        super().__init__(master)

    def create_labels(self):
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

        create_category_widgets(tags_frame, self.create_category_page)

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

        create_item_widgets(idle_item_frames, 2, "闲置中", self.show_item_detail)

        # 求物标签
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

        create_item_widgets(wanting_item_frames, 2, "求物中", self.show_item_detail)

    def create_category_page(self, category):
        category_frame = CategoryPage(self.root, category)
        get_frames_instance = GetFrames.get_instance()
        frames = get_frames_instance.get_frames()
        for frame in frames.values():
            frame.pack_forget()
        frames["category_frame"] = category_frame
        frames["category_frame"].pack(fill='both', expand=True)

    def show_item_detail(self, item_id):
        frame_name = "detail_frame_" + str(item_id)
        get_frames_instance = GetFrames.get_instance()
        frames = get_frames_instance.get_frames()
        if not frame_name in frames:
            frame = create_new_item_detail_frame(self.root, item_id)
            frames.update(frame)
        for frame in frames.values():
            frame.pack_forget()
        frames[frame_name].pack(fill='both', expand=True)










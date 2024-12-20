import tkinter as tk
from tkinter import ttk
from base_class import ScrollFrame
from utilities import like_search, create_item_widgets_from_list, create_new_item_detail_frame
from controller import GetFrames

class AvailableResultFrame(ScrollFrame):
    def __init__(self, master, keyword, item_list, row_number):
        super().__init__(master)
        self.root = master
        self.keyword = keyword
        self.item_list = item_list
        self.row_number = row_number
        self.keyword_var = tk.StringVar()
        wanting_label = ttk.Label(self.title_frame, text='已发布的闲置信息', style='ThemeFont.TLabel')
        wanting_label.pack(side='left')
        search_entry = ttk.Entry(self.title_frame, width=30, font="Arial 16", textvariable=self.keyword_var,
                                takefocus=False)
        search_entry.insert('end', self.keyword)
        search_entry.pack(side='left', padx=(20, 10))
        search_button = ttk.Button(self.title_frame, text="搜索", style='ButtonFont.TButton',
                                   command=self.main_page_search)
        search_button.pack(side='left', padx=(5, 10), pady=5)
        create_item_widgets_from_list(self.items_frame, self.row_number, self.item_list, self.show_item_detail)

    def main_page_search(self):
        keyword = self.keyword_var.get()
        item_list, row_number = like_search(keyword, "闲置中")
        self.search_result_frame = AvailableResultFrame(self.root, keyword, item_list, row_number)
        get_frames_instance = GetFrames.get_instance()
        frames = get_frames_instance.get_frames()
        frames["search_result_new"] = self.search_result_frame
        self.pack_forget()
        self.search_result_frame.pack(side='left', fill='both', expand=True)

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

class WantResultFrame(ScrollFrame):
    def __init__(self, master, keyword, item_list, row_number):
        super().__init__(master)
        self.keyword = keyword
        self.item_list = item_list
        self.row_number = row_number
        self.keyword_var = tk.StringVar()
        wanting_label = ttk.Label(self.title_frame, text='已发布的求物信息', style='ThemeFont.TLabel')
        wanting_label.pack(side='left')
        search_entry = ttk.Entry(self.title_frame, width=30, font="Arial 16", textvariable=self.keyword_var,
                                takefocus=False)
        search_entry.insert('end', self.keyword)
        search_entry.pack(side='left', padx=(20, 10))
        search_button = ttk.Button(self.title_frame, text="搜索", style='ButtonFont.TButton',
                                   command=self.main_page_search)
        search_button.pack(side='left', padx=(5, 10), pady=5)
        create_item_widgets_from_list(self.items_frame, self.row_number, self.item_list, self.show_item_detail)

    def main_page_search(self):
        keyword = self.keyword_var.get()
        item_list, row_number = like_search(keyword, "求物中")

        self.search_result_frame = WantResultFrame(self.root, keyword, item_list, row_number)
        get_frames_instance = GetFrames.get_instance()
        frames = get_frames_instance.get_frames()
        frames["search_result_new"] = self.search_result_frame
        self.pack_forget()
        self.search_result_frame.pack(side='left', fill='both', expand=True)

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

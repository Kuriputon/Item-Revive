import tkinter as tk
from tkinter import ttk
from base_class import ScrollFrame
from utilities import create_item_widgets, check_items, like_search, create_new_item_detail_frame
from controller import GetFrames
from search_result_page import AvailableResultFrame, WantResultFrame


class AvailableFrame(ScrollFrame):   # 求物界面
    def __init__(self, master):
        super().__init__(master)
        self.keyword = tk.StringVar()
        wanting_label = ttk.Label(self.title_frame, text='已发布的闲置信息', style='ThemeFont.TLabel')
        wanting_label.pack(side='left')

        search_entry = ttk.Entry(self.title_frame, width=30, font=('方正小标宋_GBK', 16), textvariable=self.keyword, takefocus=False)
        search_entry.pack(side='left', padx=(20, 10))

        search_button = ttk.Button(self.title_frame, text="搜索", style='ButtonFont.TButton', command=self.main_page_search)
        search_button.pack(side='left', padx=(5, 10), pady=5)

        self.item_list, row_number = check_items("闲置中")
        create_item_widgets(self.items_frame, row_number, "闲置中", self.show_item_detail)

    def main_page_search(self):
        keyword = self.keyword.get()
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

class WantFrame(ScrollFrame):   # 求物界面
    def __init__(self, master):
        super().__init__(master)
        self.keyword = tk.StringVar()
        wanting_label = ttk.Label(self.title_frame, text='已发布的求物信息', style='ThemeFont.TLabel')
        wanting_label.pack(side='left')

        search_entry = ttk.Entry(self.title_frame, width=30, font="Arial 16", textvariable=self.keyword, takefocus=False)
        search_entry.pack(side='left', padx=(20, 10))

        search_button = ttk.Button(self.title_frame, text="搜索", style='ButtonFont.TButton', command=self.main_page_search)
        search_button.pack(side='left', padx=(5, 10), pady=5)
        self.item_list, row_number = check_items("求物中")
        create_item_widgets(self.items_frame, row_number, "求物中", self.show_item_detail)

    def main_page_search(self):
        keyword = self.keyword.get()
        item_list, row_number = like_search(keyword, "求物中")

        self.search_result_frame=WantResultFrame(self.root, keyword, item_list, row_number)
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


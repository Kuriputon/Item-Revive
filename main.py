import tkinter as tk

from utilities import center_window, show_frame, create_item_detail_frames, resource_path
from tkinter import ttk
from plaza import PlazaFrame
from publish import PublishItemFrame, PublishWantingFrame
from mine import MyPublishedFrame
from want_page import WantFrame
from available_page import AvailableFrame



class MainPage:
    def __init__(self, master, username):
        self.root = master
        self.root = tk.Toplevel(master)
        self.page = tk.Frame(self.root)
        self.page.pack()
        # self.root.resizable(width=False, height=False)
        center_window(self.root, 800, 600) # 让窗口出现在屏幕中央
        self.root.title('物品交换平台')
        self.root.iconbitmap(resource_path("images/configs/diamond.ico"))
        self.username = username
        self.setup_menu()

        self.frames = {}
        self.create_frames()
        available_item_frames = create_item_detail_frames(self.root, "闲置中")
        self.frames.update(available_item_frames)
        wanting_item_frames = create_item_detail_frames(self.root, "求物中")
        self.frames.update(wanting_item_frames)

        self.show_plaza(self.frames, self.frames["plaza_frame"])

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)


        menubar.add_command(label='广场', command=lambda: self.show_plaza(self.frames, self.frames["plaza_frame"]))
        menubar.add_command(label='闲置', command=lambda: self.show_available_frame(self.frames, self.frames["available_frame"]))
        menubar.add_command(label='求物', command=lambda: self.show_want_frame(self.frames, self.frames["want_frame"]))

        publish_submenu = tk.Menu(menubar, tearoff=False)
        publish_submenu.add_command(label='发布闲置', command=lambda: show_frame(self.frames, "publish_item_frame"))
        publish_submenu.add_command(label='发布求物', command=lambda: show_frame(self.frames, "publish_wanting_frame"))
        menubar.add_cascade(label='发布', menu=publish_submenu)

        mine_submenu = tk.Menu(menubar, tearoff=False)
        mine_submenu.add_command(label='已发布', command=lambda: self.show_my_items(self.frames, self.frames["my_published_item_frame"]))
        mine_submenu.add_command(label='已收藏')
        mine_submenu.add_command(label='切换账号')
        mine_submenu.add_command(label='退出')
        menubar.add_cascade(label='我的', menu=mine_submenu)



        shadow_frame = ttk.Frame(height=2, style='Shadow.TFrame')
        shadow_frame.pack(fill='x')

        style = ttk.Style()
        style.configure('Shadow.TFrame', background='#B0B0B0')

    def create_frames(self):
        self.plaza_frame = PlazaFrame(self.root, self.frames)
        self.frames["plaza_frame"] = self.plaza_frame

        self.publish_item_frame = PublishItemFrame(self.root, self.username)
        self.frames["publish_item_frame"] = self.publish_item_frame

        self.publish_wanting_frame = PublishWantingFrame(self.root, self.username)
        self.frames["publish_wanting_frame"] = self.publish_wanting_frame

        self.my_published_item_frame = MyPublishedFrame(self.root, self.frames, self.username)
        self.frames["my_published_item_frame"] = self.my_published_item_frame

        self.want_frame = WantFrame(self.root, self.frames)
        self.frames["want_frame"] = self.want_frame

        self.available_frame = AvailableFrame(self.root, self.frames)
        self.frames["available_frame"] = self.available_frame
    def show_plaza(self, frames, plaza):
        for frame in frames.values():
            frame.pack_forget()
        new_plaza = PlazaFrame(plaza.root, frames)
        plaza.destroy()
        frames["plaza_frame"] = new_plaza
        new_plaza.frames = frames
        new_plaza.pack(fill='both', expand=True)

    def show_my_items(self, frames, my_items_frame):
        for frame in frames.values():
            frame.pack_forget()
        new_my_items_frame = MyPublishedFrame(my_items_frame.root, frames, self.username)
        my_items_frame.destroy()
        frames["my_published_item_frame"] = new_my_items_frame
        new_my_items_frame.frames = frames
        new_my_items_frame.pack(fill='both', expand=True)

    def show_want_frame(self, frames, want_frame):
        for frame in frames.values():
            frame.pack_forget()
        new_want_frame = WantFrame(want_frame.root, frames)
        want_frame.destroy()
        frames["want_frame"] = new_want_frame
        new_want_frame.frames = frames
        new_want_frame.pack(fill='both', expand=True)

    def show_available_frame(self, frames, available_frame):
        for frame in frames.values():
            frame.pack_forget()
        new_available_frame = AvailableFrame(available_frame.root, frames)
        available_frame.destroy()
        frames["want_frame"] = new_available_frame
        new_available_frame.frames = frames
        new_available_frame.pack(fill='both', expand=True)

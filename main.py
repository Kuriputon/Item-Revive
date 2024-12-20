import tkinter as tk
import tkinter.messagebox as messagebox

from tkinter import ttk
from manage_item import ManageItemFrame
from manage_user import ManageUserFrame
from my_given_and_got_item import MyGivenFrame, MyGotFrame
from my_received_quests import ManageReceivedQuestsFrame
from my_sent_quests import ManageSentQuestsFrame
from plaza import PlazaFrame
from publish import PublishItemFrame, PublishWantingFrame
from mine import MyPublishedFrame
from search_pages import AvailableFrame, WantFrame
from controller import GetFrames, GetUserInfo
from utilities import resource_path
from utilities_new import center_window



class MainPage:
    def __init__(self, master, username, switch_to_login):
        self.root = master
        self.root = tk.Toplevel(master)
        self.page = tk.Frame(self.root)
        self.page.pack()
        center_window(self.root, 800, 600)
        self.root.title('物品交换平台')
        self.root.iconbitmap(resource_path("images/configs/diamond.ico"))
        self.username = username
        self.switch_to_login = switch_to_login

        self.setup_menu()
        self.frames = {}
        self.create_frames()
        get_frames_instance = GetFrames.get_instance()
        get_frames_instance.frames = self.frames

        self.show_plaza(get_frames_instance.frames, get_frames_instance.frames["plaza_frame"])

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)


        menubar.add_command(label='广场', command=lambda: self.show_plaza(self.frames, self.frames["plaza_frame"]))
        menubar.add_command(label='闲置', command=lambda: self.show_available_frame(self.frames, self.frames["available_frame"]))
        menubar.add_command(label='求物', command=lambda: self.show_want_frame(self.frames, self.frames["want_frame"]))

        publish_submenu = tk.Menu(menubar, tearoff=False)
        publish_submenu.add_command(label='发布闲置', command=lambda: self.show_publish_available_frame(self.frames, self.frames["publish_item_frame"]))
        publish_submenu.add_command(label='发布求物', command=lambda: self.show_publish_want_frame(self.frames, self.frames["publish_wanting_frame"]))
        menubar.add_cascade(label='发布', menu=publish_submenu)

        mine_submenu = tk.Menu(menubar, tearoff=False)
        mine_submenu.add_command(label='已发布', command=lambda: self.show_my_items(self.frames, self.frames["my_published_item_frame"]))
        mine_submenu.add_command(label='已出', command=lambda: self.show_my_given_items(self.frames, self.frames["my_given_item_frame"]))
        mine_submenu.add_command(label='已得', command=lambda: self.show_my_got_items(self.frames, self.frames["my_got_item_frame"]))
        mine_submenu.add_command(label='已发出的交易请求', command=lambda: self.show_my_sent_quests(self.frames, self.frames["my_sent_quests_frame"]))
        mine_submenu.add_command(label='已收到的交易请求', command=lambda: self.show_my_received_quests(self.frames, self.frames["my_received_quests_frame"]))
        mine_submenu.add_command(label='切换账号', command=lambda: self.switch_account())
        mine_submenu.add_command(label='退出', command=lambda: self.quit())
        menubar.add_cascade(label='我的', menu=mine_submenu)

        manage_submenu = tk.Menu(menubar, tearoff=False)
        manage_submenu.add_command(label='管理用户', command=lambda: self.show_manage_user_frame(self.frames, self.frames["manage_user_frame"]))
        manage_submenu.add_command(label='管理物品', command=lambda: self.show_manage_item_frame(self.frames, self.frames["manage_item_frame"]))
        menubar.add_cascade(label='管理', menu=manage_submenu)

        shadow_frame = ttk.Frame(height=2, style='Shadow.TFrame')
        shadow_frame.pack(fill='x')

        style = ttk.Style()
        style.configure('Shadow.TFrame', background='#B0B0B0')

    def create_frames(self):  # 创建菜单栏上对应页面
        self.plaza_frame = PlazaFrame(self.root)
        self.frames["plaza_frame"] = self.plaza_frame

        self.publish_item_frame = PublishItemFrame(self.root, self.username)
        self.frames["publish_item_frame"] = self.publish_item_frame

        self.publish_wanting_frame = PublishWantingFrame(self.root, self.username)
        self.frames["publish_wanting_frame"] = self.publish_wanting_frame

        self.my_published_item_frame = MyPublishedFrame(self.root, self.username)
        self.frames["my_published_item_frame"] = self.my_published_item_frame

        self.my_given_item_frame = MyGivenFrame(self.root, self.username)
        self.frames["my_given_item_frame"] = self.my_given_item_frame

        self.my_got_item_frame = MyGotFrame(self.root, self.username)
        self.frames["my_got_item_frame"] = self.my_got_item_frame

        self.my_sent_quests_frame = ManageSentQuestsFrame(self.root, self.username)
        self.frames["my_sent_quests_frame"] = self.my_sent_quests_frame

        self.my_received_quests_frame = ManageReceivedQuestsFrame(self.root, self.username)
        self.frames["my_received_quests_frame"] = self.my_sent_quests_frame

        self.want_frame = WantFrame(self.root)
        self.frames["want_frame"] = self.want_frame

        self.available_frame = AvailableFrame(self.root)
        self.frames["available_frame"] = self.available_frame

        self.manage_frame = ManageUserFrame(self.root)
        self.frames["manage_user_frame"] = self.manage_frame

        self.manage_frame = ManageItemFrame(self.root)
        self.frames["manage_item_frame"] = self.manage_frame

    def show_plaza(self, frames, plaza):
        for frame in frames.values():
            frame.pack_forget()
        new_plaza = PlazaFrame(plaza.root)
        plaza.destroy()
        frames["plaza_frame"] = new_plaza
        new_plaza.pack(fill='both', expand=True)

    def show_my_items(self, frames, my_items_frame):
        for frame in frames.values():
            frame.pack_forget()
        new_my_items_frame = MyPublishedFrame(my_items_frame.root, self.username)
        my_items_frame.destroy()
        frames["my_published_item_frame"] = new_my_items_frame
        new_my_items_frame.pack(fill='both', expand=True)

    def show_my_given_items(self, frames, my_given_items_frame):
        for frame in frames.values():
            frame.pack_forget()
        new_my_given_items_frame = MyGivenFrame(my_given_items_frame.root, self.username)
        my_given_items_frame.destroy()
        frames["my_given_item_frame"] = new_my_given_items_frame
        new_my_given_items_frame.pack(fill='both', expand=True)

    def show_my_got_items(self, frames, my_got_items_frame):
        for frame in frames.values():
            frame.pack_forget()
        new_my_got_items_frame = MyGotFrame(my_got_items_frame.root, self.username)
        my_got_items_frame.destroy()
        frames["my_got_item_frame"] = new_my_got_items_frame
        new_my_got_items_frame.pack(fill='both', expand=True)

    def show_my_sent_quests(self, frames, my_sent_quests_frame):
        for frame in frames.values():
            frame.pack_forget()
        new_my_sent_quests_frame = ManageSentQuestsFrame(my_sent_quests_frame.root, self.username)
        my_sent_quests_frame.destroy()
        frames["my_sent_quests_frame"] = new_my_sent_quests_frame
        new_my_sent_quests_frame.pack(fill='both', expand=True)

    def show_my_received_quests(self, frames, my_received_quests_frame):
        for frame in frames.values():
            frame.pack_forget()
        new_my_received_quests_frame = ManageReceivedQuestsFrame(my_received_quests_frame.root, self.username)
        my_received_quests_frame.destroy()
        frames["my_received_quests_frame"] = new_my_received_quests_frame
        new_my_received_quests_frame.pack(fill='both', expand=True)

    def show_want_frame(self, frames, want_frame):
        for frame in frames.values():
            frame.pack_forget()
        new_want_frame = WantFrame(want_frame.root)
        want_frame.destroy()
        frames["want_frame"] = new_want_frame
        new_want_frame.pack(fill='both', expand=True)

    def show_available_frame(self, frames, available_frame):
        for frame in frames.values():
            frame.pack_forget()
        new_available_frame = AvailableFrame(available_frame.root)
        available_frame.destroy()
        frames["want_frame"] = new_available_frame
        new_available_frame.pack(fill='both', expand=True)

    def show_publish_available_frame(self, frames, publish_frame):
        for frame in frames.values():
            frame.pack_forget()
        new_available_frame = PublishItemFrame(publish_frame.root, self.username)
        publish_frame.destroy()
        frames["publish_item_frame"] = new_available_frame
        new_available_frame.pack(fill='both', expand=True)

    def show_publish_want_frame(self, frames, publish_frame):
        for frame in frames.values():
            frame.pack_forget()
        new_want_frame = PublishWantingFrame(publish_frame.root, self.username)
        publish_frame.destroy()
        frames["publish_wanting_frame"] = new_want_frame
        new_want_frame.pack(fill='both', expand=True)

    def show_manage_user_frame(self, frames, manage_frame):
        get_user_type_instance = GetUserInfo.get_instance()
        user_type = get_user_type_instance.usertype
        if user_type == "普通用户":
            messagebox.showinfo(title='提示信息', message='管理员才有权限浏览此页面！')
            return
        for frame in frames.values():
            frame.pack_forget()

        new_manage_frame = ManageUserFrame(manage_frame.root)
        manage_frame.destroy()
        frames["manage_frame"] = new_manage_frame
        new_manage_frame.pack(fill='both', expand=True)

    def show_manage_item_frame(self, frames, manage_frame):
        get_user_type_instance = GetUserInfo.get_instance()
        user_type = get_user_type_instance.usertype
        if user_type == "普通用户":
            messagebox.showinfo(title='提示信息', message='管理员才有权限浏览此页面！')
            return
        for frame in frames.values():
            frame.pack_forget()

        new_manage_frame = ManageItemFrame(manage_frame.root)
        manage_frame.destroy()
        frames["manage_item_frame"] = new_manage_frame
        new_manage_frame.pack(fill='both', expand=True)

    def switch_account(self):
        self.switch_to_login()

    def quit(self):
        self.root.destroy()


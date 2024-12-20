import sqlite3
from tkinter import ttk
from base_class import ScrollFrame
from controller import GetFrames
from my_given_got_item_detail import MyGivenGotDetailFrame
from utilities import create_my_given_widgets, create_my_got_widgets
from utilities_new import resource_path


class MyGivenFrame(ScrollFrame):   # 我的已出物品界面
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        tag_label = ttk.Label(self.title_frame, text='已出的物品信息', style='ThemeFont.TLabel')
        tag_label.pack(side='left')
        create_my_given_widgets(self.items_frame, self.username, self.show_item_detail)

    def show_item_detail(self, item_id):
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cursor = connection.cursor()
        query = '''
                                SELECT name, category, description, image_path, upload_time, uploaded_by, price, status
                                FROM items
                                WHERE id = ?
                                ORDER BY upload_time DESC;
                            '''
        cursor.execute(query, (item_id,))
        items = cursor.fetchone()
        name, category, description, image_path, upload_time, uploaded_by, price, status = items
        connection.close()

        get_frames_instance = GetFrames.get_instance()
        frames = get_frames_instance.get_frames()
        frame_name = "user_given_frame_" + str(item_id)
        frames[frame_name] = MyGivenGotDetailFrame(self.root, item_id, name, category, description, image_path,
                                                   upload_time, uploaded_by, price, status)
        for frame in frames.values():
            frame.pack_forget()
        frames[frame_name].pack(fill='both', expand=True)

class MyGotFrame(ScrollFrame):   # 我的已得物品界面
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        tag_label = ttk.Label(self.title_frame, text='已得的物品信息', style='ThemeFont.TLabel')
        tag_label.pack(side='left')
        create_my_got_widgets(self.items_frame, self.username, self.show_item_detail)

    def show_item_detail(self, item_id):
        connection = sqlite3.connect(resource_path('databases/database.db'))
        cursor = connection.cursor()
        query = '''
                                SELECT name, category, description, image_path, upload_time, uploaded_by, price, status
                                FROM items
                                WHERE id = ?
                                ORDER BY upload_time DESC;
                            '''
        cursor.execute(query, (item_id, ))
        items = cursor.fetchone()
        name, category, description, image_path, upload_time, uploaded_by, price, status = items
        connection.close()

        get_frames_instance = GetFrames.get_instance()
        frames = get_frames_instance.get_frames()
        frame_name = "user_given_frame_" + str(item_id)
        frames[frame_name] = MyGivenGotDetailFrame(self.root, item_id, name, category, description, image_path, upload_time, uploaded_by, price, status)
        for frame in frames.values():
            frame.pack_forget()
        frames[frame_name].pack(fill='both', expand=True)


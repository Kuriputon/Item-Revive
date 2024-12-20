import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # 如果在打包后的程序中运行
        return os.path.join(sys._MEIPASS, relative_path)
    # 在开发环境中运行
    return relative_path

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # 如果在打包后的程序中运行
        return os.path.join(sys._MEIPASS, relative_path)
    # 在开发环境中运行
    return os.path.join(os.path.abspath("."), relative_path)


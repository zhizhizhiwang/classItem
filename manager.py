import multiprocessing
import os.path
import sys
import pygame
import pystray
from PIL import Image

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)  

import 置顶课表 as top
import 课表 as background

icon = Image.open("here.ico")
pygame.init()
pygame_flag = 0



def ext():
    global back
    if back.is_alive():
        back.terminate()  # 终止当前进程
    down_icon.stop()  # 退出图标
    background.ext()  # 手动回收
    pygame.quit()  # 退出pygame
    os._exit(0)  # 退出程序


def on_reload():
    global back
    if back.is_alive():
        back.terminate()  # 终止当前进程
    back = multiprocessing.Process(target=background.main)  # 重新创建进程
    back.start()  # 启动新进程

def show_background():
    if not back.is_alive():
        back.start()  # 启动新进程


def on_click():
    global pygame_flag
    if pygame_flag == 0:
        pygame_flag = 1
        top.main()
    elif pygame_flag == 1:
        top.stop()
        pygame_flag = 0


menu = (
    pystray.MenuItem("启动", show_background, default=True),
    pystray.MenuItem("切换顶端显示", on_click),
    pystray.MenuItem("打开配置文件", lambda :os.startfile('note.txt')),
    pystray.MenuItem("重载", on_reload),
    pystray.MenuItem("退出", ext)
)

if __name__ == "__main__":
    down_icon = pystray.Icon("课表", icon, "课表", menu)
    back = multiprocessing.Process(target=background.main)  # 创建进程
    background.reload()
    back.start()  # 启动进程
    down_icon.run()
    



import datetime
import json
import os
import random
import threading
import time
import tkinter
import atexit
import cv2
import numpy as np
import win32con
import win32gui
from PIL import Image, ImageDraw, ImageFont

# 加载配置文件
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 获取当前星期几
today = str(datetime.datetime.now().isoweekday())
current_config = config.get(today, [])

# 获取屏幕尺寸
root = tkinter.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
whole_time = 18
height = 40

# 加载并缩放背景图片
background_path = 'background.jpg'  # 请替换为实际图片路径
if os.path.exists(background_path):
    img = cv2.imread(background_path)
    # img = cv2.resize(img, (screen_width, screen_height))
    # 按照源比例尺缩放
    img_height, img_width = img.shape[:2]
    scale = min(screen_width / img_width, screen_height / img_height)
    img = cv2.resize(img, (int(img_width * scale), int(img_height * scale)))
    img = img[0:screen_height, 0:screen_width]
else:  # 创建白色背景
    img = np.full((screen_height, screen_width, 3), 255, dtype=np.uint8)

color_rgb = (
    random.randint(128, 255),
    random.randint(128, 255),
    random.randint(128, 255)
)

color_rgb = (255, 255, 255) if color_rgb == (240, 240, 200) else color_rgb
running = True
print("background loaded")


def change_rbg():
    global color_rgb
    color_rgb = (
        random.randint(128, 255),
        random.randint(128, 255),
        random.randint(128, 255)
    )
    color_rgb = (255, 255, 255) if color_rgb == (240, 240, 200) else color_rgb


def time_map(time_str):
    """将时间转换为屏幕横坐标"""
    try:
        hours, mins = map(int, time_str.split(':'))
        total_mins = hours * 60 + mins - 5 * 60
        total_mins = max(0, min(total_mins, whole_time * 60))
        return int((total_mins / (whole_time * 60)) * screen_width)
    except:
        return 0


def ext():
    global running
    print("trigger ext")
    running = False
    _output_path = os.path.abspath('background.jpg')
    win32gui.SystemParametersInfo(
        win32con.SPI_SETDESKWALLPAPER,
        _output_path,
        win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
    )


def reload():
    global img, color_rgb, current_config, today, background_path, config, root, screen_width, screen_height, whole_time, height

    root = tkinter.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    whole_time = 18
    height = 40

    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    today = str(datetime.datetime.now().isoweekday())
    current_config = config.get(today, [])

    background_path = 'background.jpg'
    if os.path.exists(background_path):
        img = cv2.imread(background_path)
        img = cv2.resize(img, (screen_width, screen_height))
    else:  # 创建白色背景
        img = np.full((screen_height, screen_width, 3), 255, dtype=np.uint8)

    color_rgb = (
        random.randint(128, 255),
        random.randint(128, 255),
        random.randint(128, 255)
    )

    color_rgb = (255, 255, 255) if color_rgb == (240, 240, 200) else color_rgb


atexit.register(ext)
threading.Timer(60, change_rbg, ()).start()


def draw_rounded_rect(img, pt1, pt2, color, radius=height // 2):
    """
    绘制圆角矩形（支持填充）
    参数：
        img: 目标图像
        pt1: 左上角坐标 (x1, y1)
        pt2: 右下角坐标 (x2, y2)
        color: 颜色 (BGR格式)
        radius: 圆角半径
    """
    x1, y1 = pt1
    x2, y2 = pt2
    h, w = y2 - y1, x2 - x1

    # 自动调整过大半径（不超过短边的1/4）
    # radius = min(radius, abs(h) // 4, abs(w) // 4)

    # 当矩形足够大时绘制圆角
    if radius >= 0 and w >= 2 * radius and h >= 2 * radius:
        # 绘制四个圆角
        cv2.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, -1)  # 左上角
        cv2.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, -1)  # 右上角
        cv2.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, -1)  # 左下角
        cv2.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, -1)  # 右下角

        # 填充四个矩形区域
        cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, -1)  # 上下矩形
        cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, -1)  # 中间矩形
    else:  # 退化为普通矩形
        cv2.rectangle(img, pt1, pt2, color, -1)


def main():
    global img, color_rgb, current_config, today, background_path, config, root, screen_width, screen_height, whole_time, height, running
    running = True
    while running:
        # 获取当前时间并计算进度条位置
        current_time = datetime.datetime.now()
        current_str = f"{current_time.hour}:{current_time.minute}"
        # 12:0 -> 12:00
        if current_time.minute < 10:
            current_str = f"{current_time.hour}:0{current_time.minute}"

        progress_width = time_map(current_str)

        # 背景
        draw_rounded_rect(img, (0, 0), (screen_width, height), (240, 250, 250))

        # 绘制进度条（转换为BGR颜色格式）
        draw_rounded_rect(img, (0, 0), (progress_width, height), color_rgb[::-1])

        # 绘制时间区块边框
        for item in current_config:
            start_x = time_map(item['time'][0])
            end_x = time_map(item['time'][1])
            # cv2.rectangle(img, (start_x, 0), (end_x, height), (0, 0, 0), 1)
            cv2.line(img, (start_x, 5), (start_x, height - 5), (0, 0, 0), 1)
            cv2.line(img, (end_x, 5), (end_x, height - 5), (0, 0, 0), 1)

        # 使用PIL添加文字
        font_path = 'MapleMono-NF-CN.ttf'
        try:
            # font = ImageFont.truetype(font_path, height // 2 - 5)
            font = ImageFont.truetype(font_path, height - 5)
        except:
            font = ImageFont.load_default()

        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        # 当前时间

        # 进度条更明显
        # draw.text((progress_width - 100, -5), "-->", font=font, fill=(0, 0, 0))

        for item in current_config:
            x = time_map(item['time'][0])
            title = item['title']

            # 设置文字颜色
            text_color = (255, 20, 20) if title == "杀！" else (0, 0, 0)

            # 绘制两行文字
            '''
            draw.text((x , 0), title[0], font=font, fill=text_color)
            if len(title) > 1:
                draw.text((x, height // 2), title[1], font=font, fill=text_color)
            '''

            # 单字模式
            draw.text((x, 0), title[0], font=font, fill=text_color)

        draw.text((time_map(current_str) - 120, -3), current_str, font=font, fill=(255, 255, 255, 120))

        # 转换回OpenCV格式
        img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        # 保存并设置壁纸
        output_path = os.path.abspath('desktop_bg.jpg')
        cv2.imwrite('desktop_bg.jpg', img)
        win32gui.SystemParametersInfo(
            win32con.SPI_SETDESKWALLPAPER,
            output_path,
            win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
        )

        time.sleep(10)
    ext()


if __name__ == '__main__':
    reload()
    main()

import datetime
import json
import os
from random import randint

import pygame
import win32con
import win32gui

pygame.init()

screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = 50
startX = 0
running = True
config = json.load(open(r".\config.json", mode="r" , encoding="utf-8"))
today = str(datetime.datetime.now().isoweekday())


def time_map(time: str):
    sec = int(time.split(':')[0]) * 60 + int(time.split(':')[1]) - 5 * 60
    # print((sec / (16 * 60)) * SCREEN_WIDTH)
    return int((sec / (18 * 60)) * SCREEN_WIDTH)


def in_time(inp: str, st: str, ed: str):
    return time_map(st) < time_map(inp) < time_map(ed)


pygame.quit()


def main():
    pygame.init()
    global running
    running = True
    # 获取屏幕尺寸信息

    print(today)
    print(config.get(today, []))
    
    

    font = pygame.font.Font('MapleMono-NF-CN.ttf', SCREEN_HEIGHT - 10)
    # 设置窗口位置到屏幕左上角
    os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

    # 创建无边框、置顶窗口
    window = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.NOFRAME
    )
    hwnd = win32gui.GetForegroundWindow()

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 600, 300, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
    # hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd,
                        win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    # win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(255, 255, 255)), 200, win32con.LWA_ALPHA)
    # 设置窗口标题
    pygame.display.set_caption("Top Bar")

    color = randint(128, 255), randint(128, 255), randint(128, 255)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # 按ESC键退出
                    running = False

        current_time = datetime.datetime.now()
        current_str = f"{current_time.hour}:{current_time.minute}"
        # 12:0 -> 12:00
        if current_time.minute < 10:
            current_str = f"{current_time.hour}:0{current_time.minute}"
        
        now_time = datetime.datetime.now()
        minute = current_str

        if minute in [n['time'][0] for n in config.get(today, [])]:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 600, 300, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
        elif minute in [n['time'][1] for n in config.get(today, [])]:
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 600, 300, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)

        # 填充背景色（这里使用白色）
        pygame.draw.rect(window, (255, 255, 255), ((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)), 0, 25)
        pygame.draw.rect(window, color, ((0, 0), (time_map(minute), SCREEN_HEIGHT)), 0, 25)
        
        time_text = font.render(current_str, True, (255, 255, 255, 100))
        window.blit(time_text, (time_map(current_str) - 140, 0))

        for each in config.get(today, []):
            # print(each['time'])
            # print(each['title'])
            box = (
                (time_map(each['time'][0]),
                0),
                ((time_map(each['time'][1]) - time_map(each['time'][0])),
                SCREEN_HEIGHT))
            pygame.draw.line(window, (0, 0, 0), (time_map(each['time'][0]), 5),
                            (time_map(each['time'][0]), SCREEN_HEIGHT - 5))
            pygame.draw.line(window, (0, 0, 0), (time_map(each['time'][1]), 5),
                            (time_map(each['time'][1]), SCREEN_HEIGHT - 5))
            if each['title'] == "杀！":
                text1 = font.render(each['title'][0], True, (255, 20, 20))
                # text2 = font.render(each['title'][1], True, (255, 20, 20))
            else:
                text1 = font.render(each['title'][0], True, (0, 0, 0))
                # text2 = font.render(each['title'][1], True, (0, 0, 0))

            window.blit(text1, box[0])
            # window.blit(text2, (box[0][0], SCREEN_HEIGHT // 2))
        # 更新显示
        pygame.display.flip()

    # 退出程序
    pygame.quit()


def stop():
    global running
    running = False


if __name__ == '__main__':
    main()

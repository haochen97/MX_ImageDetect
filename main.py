import sys, cv2
import numpy as np
import win32api, win32con, win32gui
import time
import threading

sys.path.append("E:\\AutoMate\\opencv")

from key_mouse import vmouse
from data.lots_name import window_title
from data.common_pos import icon_pos
from opencv import get_img

if __name__ == "__main__":
 
    # 创建windscreenshot的对象
    mx_img = get_img.WindScreenShot(window_title.title['mx'])
    
    #创建线程运行获取实时截图
    mx_img.create_qtapp()   # 创建Qapplication对象，因为必须在main线程中，所以需要单独创建
    #实时获取窗口图像，使用单独线程
    #ori_img = mx_img.real_time()
    thread1 = threading.Thread(target = mx_img.real_time)
    ori_img = thread1.start()   #返回截图
    
    #鼠标操作
    #打开物品栏
    #vmouse.back.drag(mx_img.hwnd, (1379, 505), (1577, 315))

    vmouse.back.click(mx_img.hwnd, icon_pos.base["属性"])
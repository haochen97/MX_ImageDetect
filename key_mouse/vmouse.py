from multiprocessing.connection import wait
import time
from tkinter import Y
from cv2 import waitKey
from matplotlib import ft2font
import win32api, win32con, win32gui


class front():
    #获取父窗口坐标
    def coord_proc(hwnd, x:int, y:int):
        '''
        #对返回的窗口内相对坐标处理为全屏坐标
        '''
        if hwnd != 0:   #判断句柄是否为0,
            (left, top, right, bottom) = win32gui.GetWindowRect(hwnd)
            all_x = left + x
            all_y = top + y
            return all_x, all_y
        else:   #如果为0，则直接为全屏坐标
            all_x = x
            all_y = y
            return all_x, all_y

    def move(hwnd, x:int, y:int):
        #获取转换后的全屏坐标
        (all_x, all_y) = front.coord_proc(hwnd, x, y)
        #移动鼠标
        win32api.SetCursorPos((all_x, all_y))

    def click(hwnd, x:int, y:int, flags1:int = 0, flags2:int = 1):
        '''
        flags1: 0-左键（默认）,1-右键,2-中键
        flags2: 1-单击(默认),2-双击,3-三击,N-N击
        '''
        #获取转换后的全屏坐标
        (all_x, all_y) = front.coord_proc(hwnd, x, y)
        #构建点击次数集
        f2 = range(flags2)
        
        #移动鼠标
        win32api.SetCursorPos((all_x, all_y))
        time.sleep(0.03)   # 30ms
        
        #判断点击次数
        for x in f2: 
            if flags1 == 0:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0)
                time.sleep(0.03)   # 30ms
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0)
            elif flags1 == 1:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0)
                time.sleep(0.03)   # 30ms
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0)
            else:
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0)
                time.sleep(0.03)   # 30ms
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0)
    
    def drag(hwnd, x1, y1, x2, y2, flags1 = 0):
        '''
        按住鼠标移至目标点
        （x1.y1）起始点，（x2,y2）目标点
        flags1: 0-左键（默认）,1-右键,2-中键
        右键和中键一般用不到
        '''
        #获取转换后的全屏坐标
        (all_x1, all_y1) = front.coord_proc(hwnd, x1, y1)
        (all_x2, all_y2) = front.coord_proc(hwnd, x2, y2)

        #计算移动距离和绝对坐标
        x_len = all_x2 - all_x1
        y_len = all_y2 - all_y1
        print(x_len, y_len)

        #移动至起始点
        win32api.SetCursorPos((all_x1, all_y1))
        #设置步长
        x_step = y_step = 1
        #操作
        if flags1 == 0:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0)
                if x_len < 0:
                    x_len = -x_len
                    x_step = -1
                if y_len < 0:
                    y_len = -y_len
                    y_step = -1
                for i in range(x_len):
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_step, 0, 0)
                for j in range(y_len):
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, y_step, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0)
        '''
        elif flags1 == 1:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0)
                time.sleep(0.5)   # 30ms
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_len, y_len, 0)
                time.sleep(0.5)   # 30ms
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0)
        else:
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0)
                time.sleep(0.5)   # 30ms
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_len, y_len, 0)
                time.sleep(0.5)   # 30ms
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0)
        '''
                
                

class back():
    '''
    后端鼠标模拟
    '''
    
    def move(hwnd: int, pos:tuple):
        x = pos[0]
        y = pos[1]
        wparam = 0
        '''
        wparam:
        MK_CONTROL	如果CTRL键关闭，请设置。
        MK_LBUTTON	设置鼠标左键是否关闭。
        MK_MBUTTON	设置中间的鼠标按钮是否关闭。
        MK_RBUTTON	设置鼠标右键是否关闭。
        MK_SHIFT	设置SHIFT键是否关闭。
        '''
        #将输入坐标放到pos的高低位，低位为x，高位为y
        pos = win32api.MAKELONG(x, y)

        win32gui.SendMessage(hwnd, win32con.WM_MOUSEMOVE, wparam, pos)

    def click(hwnd: int, pos:tuple, flags1 = 0, flags2 = 1):
        '''
        flags1: 0-左键（默认）,1-右键,2-中键
        flags2: 1-单击(默认),2-双击,3-三击,N-N击
        '''
        #将输入坐标放到pos的高低位，低位为x，高位为y
        x = pos[0]
        y = pos[1]
        pos = win32api.MAKELONG(x, y)
        #构建点击次数集
        f2 = range(flags2)
        
        #判断点击次数
        for x in f2: 
            if flags1 == 0:
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, pos)
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, pos)
            elif flags1 == 1:
                win32gui.SendMessage(hwnd, win32con.WM_RBUTTONDOWN, 0, pos)
                win32gui.SendMessage(hwnd, win32con.WM_RBUTTONUP, 0, pos)
            else:
                win32gui.SendMessage(hwnd, win32con.WM_MBUTTONDOWN, 0, pos)
                win32gui.SendMessage(hwnd, win32con.WM_MBUTTONUP, 0, pos)

    def drag(hwnd: int, pos1:tuple, pos2:tuple, flags1 = 0):
        '''
        按住鼠标移至目标点
        （x1.y1）起始点，（x2,y2）目标点
        flags1: 0-左键（默认）,1-右键,2-中键
        右键和中键一般用不到
        '''
        #取出输入坐标
        x1 = pos1[0]
        y1 = pos1[1]
        x2 = pos2[0]
        y2 = pos2[1]
        
        #计算移动距离
        x_len = x2 - x1
        if x_len == 0:
            x2 = x2 + 10
        #计算直线方程 
        x = x1 
        y = int((x - x1) / (x2 - x1) * (y2 -y1) + y1)
        pos = win32api.MAKELONG(x , y)
        #设置步长
        x_step  = 1
        
        #操作
        if flags1 == 0:
                win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos)
                
                if x_len < 0:
                    x_len = -x_len
                    x_step = -1
                for i in range(x_len):
                    x = x + x_step
                    y = int((x - x1) / (x2 - x1) * (y2 -y1) + y1) 
                    pos = win32api.MAKELONG(x, y)
                    win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, pos)
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1, 0)
                win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, pos)
                win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, pos)
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos)
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, pos)

class mix:
    def drag(hwnd, pos1:tuple, pos2:tuple, flags1 = 0):
        '''
        按住鼠标移至目标点
        （x1.y1）起始点，（x2,y2）目标点
        flags1: 0-左键（默认）,1-右键,2-中键
        右键和中键一般用不到
        '''
        #设置鼠标捕获
        win32gui.SetCapture(hwnd)
        #取出输入坐标
        x1 = pos1[0]
        y1 = pos1[1]
        x2 = pos2[0]
        y2 = pos2[1]

        #获取转换后的全屏坐标
        (all_x1, all_y1) = front.coord_proc(hwnd, x1, y1)
        (all_x2, all_y2) = front.coord_proc(hwnd, x2, y2)

        #计算移动距离和绝对坐标
        x_len = all_x2 - all_x1
        y_len = all_y2 - all_y1
       

        #移动至起始点
        win32api.SetCursorPos((all_x1, all_y1))
        #设置步长
        x_step = y_step = 1
        #操作
        if flags1 == 0:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0)
                if x_len < 0:
                    x_len = -x_len
                    x_step = -1
                if y_len < 0:
                    y_len = -y_len
                    y_step = -1
                for i in range(x_len):
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_step, 0, 0)
                for j in range(y_len):
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, y_step, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0)
        win32gui.ReleaseCapture
    pass
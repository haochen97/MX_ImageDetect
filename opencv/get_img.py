import cv2
import sys
import win32gui
import win32con
from PyQt5.QtWidgets import QApplication
import numpy as np
from key_mouse import vmouse


class WindScreenShot:
    """
    获取指定窗口图像，实例化时需要传入窗口标题
    """
    
    
    # 类变量
    window_name: str = None     # 窗口名
    hwnd:int = None     # 窗口句柄
    app = None

    def __init__(self, window_name:str) -> None:
        self.window_name = window_name


    def real_time(self):
        """
        实时获取窗口图像
        """
        
        # 获取窗口句柄
        self.hwnd = self.get_hwnd()
        # 鼠标回调函数
        def mouse_callback(event, x, y, flags, userdata):
            event_name = {
                0 : "CV_EVENT_MOUSEMOVE",
                1 : "CV_EVENT_LBUTTONDOWN",
                2 : "CV_EVENT_RBUTTONDOWN",
                3 : "CV_EVENT_MBUTTONDOWN",
                4 : "CV_EVENT_LBUTTONUP",
                5 : "CV_EVENT_RBUTTONUP",
                6 : "CV_EVENT_MBUTTONUP",
                7 : "CV_EVENT_LBUTTONDBLCLK",
                8 : "CV_EVENT_RBUTTONDBLCLK",
                9 : "CV_EVENT_MBUTTONDBLCLK",
                10: "CV_EVENT_WHEEL",
                1 : "CV_EVENT_FLAG_LBUTTON",
                2 : "CV_EVENT_FLAG_RBUTTON",
                4 : "CV_EVENT_FLAG_MBUTTON",
                8 : "CV_EVENT_FLAG_CTRLKEY",
                16 : "CV_EVENT_FLAG_SHIFTKEY",
                32 : "CV_EVENT_FLAG_ALTKEY",        
            } 
            if event == 1:
                pos = (x, y)
                vmouse.back.click(self.hwnd, pos)
            elif event == 7:
                pos = (x, y)
                vmouse.back.click(self.hwnd, pos, 0, 2)
            print(event_name[event], x, y, flags, userdata)
        
        # 创建窗口
        cv2.namedWindow("real_time", cv2.WINDOW_AUTOSIZE) # 跟原窗口同样大小
        cv2.setMouseCallback("real_time", mouse_callback, 0)
        while True:
            # 获取指定窗口截图
            ori_img = self.screen_shot()
            # 显示窗口
            key = cv2.waitKey(30)
            cv2.imshow("real_time", ori_img)
            # 停止显示
            if key & 0xFF == 27:      # 按esc键退出
                print(key)
                break

        cv2.destroyAllWindows()

    
    def convert_format_2mat(self, img):
        """
        Converts a QImage into an opencv MAT format
        """
        # Format_RGB32 = 4,存入格式为B,G,R,A 对应 0,1,2,3
        # RGB32图像每个像素用32比特位表示，占4个字节，
        # R，G，B分量分别用8个bit表示，存储顺序为B，G，R，最后8个字节保留
        img = img.convertToFormat(4)
        width = img.width()
        height = img.height()

        ptr = img.bits()
        ptr.setsize(img.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
        # arr为BGRA，4通道图片
        return arr

    
    def get_hwnd(self):
        """
        获取窗口句柄
        """
        hwnd = win32gui.FindWindow(0, self.window_name)

        if hwnd == 0:
            return None
        else:
            # 还原最小化窗口
            win32gui.SendMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            # 高亮目标窗口
            # win32gui.SetForegroundWindow(handle)
            # return win32gui.GetWindowRect(handle), handle
            return hwnd
    

    def create_qtapp(self):
        app = QApplication(sys.argv)    #由于QApplication实例只能被创建在主线程中
        self.app = app


    def screen_shot(self) -> cv2.Mat:
        
        # 根据句柄截图
        #app =  QApplication(sys.argv)
        screen = QApplication.primaryScreen()
        img = screen.grabWindow(self.hwnd).toImage()
        #img.save("E:\\AutoMate\\img\\实时窗口图.jpg")
        ori_img = self.convert_format_2mat(img) # 将获取的图像从QImage转换为RBG格式
        cv2.imwrite("E:\\AutoMate\\img\\实时窗口图.png", ori_img)
        return ori_img

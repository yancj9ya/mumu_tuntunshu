# This file is used to capture the screenshot of the game window and send mouse events to the game window.
#
#

import win32gui
import win32ui
import win32con
import time
import numpy as np
import cv2
from ctypes import windll
from mytool.datatype import rect,Point

WM_LBUTTONDOWN = 0x0201
WM_SERCURSOR = 0x20
WM_MOUSEACTIVATE = 0x21
WM_MOUSEMOVE = 0x0200
WM_LBUTTONUP = 0x0202
WM_PARENTNOTIFY = 0x210
WM_MOUSEWHEEL = 0x020A

MK_LBUTTON = 0x0001
HTCLIENT = 1

PostMessage = windll.user32.PostMessageW
SendMessage = windll.user32.SendMessageW

FindWindow = win32gui.FindWindow
FindWindowEx = win32gui.FindWindowEx
windll.user32.SetProcessDPIAware()
class handle:
    def __init__(self):
        self.par_handle = self.get_handle("MuMu模拟器12")
        self.child_handle = self.get_handleEx(self.par_handle, "MuMuPlayer")
    @classmethod
    def get_handle(cls, title:str)->int:
        return win32gui.FindWindow(None, title)
    @classmethod
    def get_handleEx(cls, par_handle:int, title:str)->int:
        return win32gui.FindWindowEx(par_handle, None, None, title)
class winmsg:
    def __init__(self):
        self.par_handle = None
        self.child_handle = None
        pass
    #windows message
    #通知父级窗口
    def notifyparent(self, x,y):
        msg=WM_PARENTNOTIFY
        wparam=WM_LBUTTONDOWN
        Lparam=y << 16 | x
        SendMessage(self.par_handle,msg,wparam,Lparam)
    #鼠标移动（按住左键）
    def mouse_move(self,x,y):
        msg=WM_MOUSEMOVE
        wparam=MK_LBUTTON
        Lparam=y << 16 | x
        PostMessage(self.child_handle,msg,wparam,Lparam)
    #激活鼠标   
    def mouseactivate(self):
        msg=WM_MOUSEACTIVATE
        wparam=self.par_handle
        Lparam=WM_LBUTTONDOWN << 16 | HTCLIENT
        SendMessage(self.child_handle,msg,wparam,Lparam)
    #设置鼠标位置
    def setcursor(self):
        msg=WM_SERCURSOR
        wparam=self.child_handle
        Lparam=WM_LBUTTONDOWN << 16 | HTCLIENT
        SendMessage(self.child_handle,msg,wparam,Lparam)
    #鼠标左键按下
    def left_down(self,x,y):
        msg=WM_LBUTTONDOWN
        wparam=MK_LBUTTON
        Lparam=int(y) << 16 | int(x)
        PostMessage(self.child_handle,msg,wparam,Lparam)
    #鼠标左键抬起
    def left_up(self,x,y):
        msg=WM_LBUTTONUP
        wparam=0
        Lparam=int(y) << 16 | int(x)
        PostMessage(self.child_handle,msg,wparam,Lparam)
    # 滚动鼠标滚轮
    def wheel_scroll(self,delta,x,y):
        msg=WM_MOUSEWHEEL
        wparam=delta << 16 
        Lparam=y << 16 | x
        PostMessage(self.child_handle,msg,wparam,Lparam)
        
    def get_window_rect(self)->list:
        return win32gui.GetWindowRect(self.child_handle)
    
    def x_button_down(self,x,y):
        msg=WM_XBUTTONDOWN
        wparam=MK_XBUTTON1
        Lparam=y << 16 | x
        PostMessage(self.child_handle,msg,wparam,Lparam)
    
    def x_button_up(self,x,y):
        msg=WM_XBUTTONDOWN
        wparam=MK_XBUTTON1
        Lparam=y << 16 | x
        PostMessage(self.child_handle,msg,wparam,Lparam)
class screenshot:
    def __init__(self, handle):
        self.handle = handle
    @classmethod
    def get_screenshot(cls, hwnd:int, area:rect)->np.ndarray:
        if type(area) is list:area = rect(*area)
        try:
            # 计算截图区域
            w, h = area.width, area.height
            # 获取窗口设备上下文
            hwindc = win32gui.GetWindowDC(hwnd)
            srcdc = win32ui.CreateDCFromHandle(hwindc)
            memdc = srcdc.CreateCompatibleDC()
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(srcdc, w, h)
            memdc.SelectObject(bmp)
            # 从源设备上下文复制位图到内存设备上下文
            memdc.BitBlt((0, 0), (w, h), srcdc, (area.s_x, area.s_y), win32con.SRCCOPY)
            # 获取位图数据并转换为图像数组
            signedIntsArray = bmp.GetBitmapBits(True)
            img = np.frombuffer(signedIntsArray, dtype='uint8').reshape(h, w, 4)
            # 清理资源
            srcdc.DeleteDC()
            memdc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwindc)
            win32gui.DeleteObject(bmp.GetHandle())
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)         
        except Exception as e:
            print(f"截图失败，错误信息: {e}")
            return None
    def save_screenshot(self, screenshot_img:np.ndarray,save_path:str)->bool:
        #获取当前时间用作保存的文件命名
        timestamp = time.strftime("(%Y-%m-%d)  %H时%M分", time.localtime())
        path = f'{save_path}/{timestamp}.jpg'
        cv2.imencode('.jpg', screenshot_img)[1].tofile(path)
        print(f"截图成功，保存路径为{path}")
        return True
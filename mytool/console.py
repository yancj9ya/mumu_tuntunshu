import ctypes

class Console:
    @staticmethod
    def hide_console():
        # 隐藏控制台窗口
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.user32.ShowWindow(hwnd, 0)  # 0 = SW_HIDE
    @staticmethod
    def show_console():
        # 显示控制台窗口
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.user32.ShowWindow(hwnd, 5)  # 5 = SW_SHOW
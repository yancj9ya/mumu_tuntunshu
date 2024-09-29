# this file is used to simulate mouse click and mouse move and so on

from mytool.winmsg import handle,winmsg,screenshot
from time import sleep
from mytool.datatype import Point,rect,image
from mytool.bezier import BezierTrajectory

class Mouse(handle,winmsg,screenshot):
    def __init__(self):
        super().__init__()
    # mouse click
    def click(self,point:Point|tuple[int,int],click_delay=0.1):
        '''
        point: Point
            the point to click
        click_delay: float
            the time bettween click down and up
        '''
        self.left_down(*point)
        sleep(click_delay)
        self.left_up(*point)
    # random area mouse click
    def random_click(self,area:rect|list[int,int,int,int]|tuple[int,int,int,int]):
        '''
        area: rect
            the area to click
        '''
        if type(area) in (list,tuple):area = rect(*area)
        print(f'click at:{area.random_point}')
        self.click(area.random_point)
    # mouse wheel 
    def mouse_scroll(self, d_t:tuple[str,int], x:int, y:int)->None:
        '''
        d_t: tuple[str,int]
            'up': up scroll
            'down': down scroll
            'int': int value of scroll times
        x: int
            x coordinate of mouse
        y: int
            y coordinate of mouse
        '''
        # print(f'mouse scroll {d_t[0]} {d_t[1]} times at ({x},{y})')
        rect=self.get_window_rect()
        x+=rect[0]
        y+=rect[1]
        self.mouseactivate()
        match d_t[0]:
            case 'up':
                for _ in range(d_t[1]):
                    self.wheel_scroll(120, x, y)
                    sleep(0.1)
            case 'down':
                for _ in range(d_t[1]):
                    self.wheel_scroll(-120, x, y)
                    sleep(0.1)
    # slide screen
    def slide(self,start:rect|Point,end:rect|Point,move_time=0.5)->None:
        #如果输入rect，则随机取一个点作为起始点和结束点
        if type(start)==rect:
            start=start.random_point
        if type(end)==rect:
            end=end.random_point
        #获取贝塞尔曲线
        move_list=BezierTrajectory.move_by_bezier(*start,*end)
        #print(len(move_list),move_list,start,end)
        #计算每一步的时间间隔
        slide_delay=move_time/len(move_list)
        #开始滑动
        self.left_down(*start)
        for point in move_list:
            self.mouse_move(*point)
            sleep(slide_delay)
        self.left_up(*end)   
        pass    
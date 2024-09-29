from collections import namedtuple
from random import randint

Point = namedtuple('Point', ['x', 'y'])
class rect:
    screen_width=1280
    screen_height=720
    def __init__(self,s_x:int,s_y:int,e_x:int,e_y:int):
        self.area=self.format_area(Point(s_x,s_y),Point(e_x,e_y))
        self.s_x,self.s_y,self.e_x,self.e_y=self.area
    def format_area(self,start:Point,end:Point):
        try:
            assert start.x<end.x and start.y<end.y,"area error:s_point over e_point"
            assert start.x>=0 and start.y>=0,"area error:s_point out of screen"
            assert end.x<=self.screen_width and end.y<=self.screen_height,"area error:e_point out of screen"
        except AssertionError as e:
            print(f'area error:{e} rect:{start},{end}')
            start.x=max(start.x,0)
            start.y=max(start.y,0)
            end.x=min(end.x,self.screen_width)
            end.y=min(end.y,self.screen_height)
        return [start.x,start.y,end.x,end.y]
    def expand_area(self,pixel:int)->list:
        return self.format_area(Point(self.s_x-pixel,self.s_y-pixel),Point(self.e_x+pixel,self.e_y+pixel))
    @property
    def random_point(self)->Point:
        return Point(self.s_x+randint(0,self.width),self.s_y+randint(0,self.height))
    @property
    def width(self)->int:
        return self.e_x-self.s_x
    @property    
    def height(self)->int:
        return self.e_y-self.s_y
    @property
    def center(self)->Point:
        return Point((self.s_x+self.e_x)//2,(self.s_y+self.e_y)//2)
    @property
    def top_left(self)->Point:
        return Point(self.s_x,self.s_y)
    @property
    def bottom_right(self)->Point:
        return Point(self.e_x,self.e_y)
    
class image:
    '''
    path:str
    area:list|tuple
    name:str
    '''
    def __init__(self,path:str,area:list,name:str):
        self.path=path
        self.name=name
        self.rect=rect(*area)
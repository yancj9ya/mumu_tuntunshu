# this file is for recognize image
from mytool.winmsg import handle,screenshot
from random import randint
from mytool.datatype import image,rect,Point
from mytool.mylog import MyLog
import cv2
import numpy as np
import pathlib
import  time

log=MyLog()
class ImgRec:
    def __init__(self):
        self.par_handle=handle.get_handle('MuMu模拟器12')
        self.child_handle=handle.get_handleEx(self.par_handle,'MuMuPlayer')
    #循环匹配列表的img，返回第一个匹配成功的img的名称
    def match_ui(self, img_list: list[image],accuracy=0.8)->str:
        try:
            for image in img_list:
                if self.match_img(image,accuracy=accuracy):
                    return image.name
        except Exception as e:
            print(f"match_ui <{image.name}>发生错误: {e}")
            return None
    def match_img(self, img:image, accuracy=0.8)->rect:
        #log.debug(f"match_img<{img.name}>")
        try:
            ShotImage = cv2.cvtColor(screenshot.get_screenshot(self.child_handle, img.rect.expand_area(5)), cv2.COLOR_BGRA2GRAY)
            template = cv2.imread(img.path, cv2.IMREAD_GRAYSCALE)
            Res = cv2.matchTemplate(ShotImage, template, cv2.TM_CCOEFF_NORMED)

            if cv2.minMaxLoc(Res)[1] > accuracy:
                matchCor = cv2.minMaxLoc(Res)[3]
                h, w = template.shape
                s_X = img.rect.s_x + matchCor[0]-5
                s_Y = img.rect.s_y + matchCor[1]-5
                e_X = w + s_X
                e_Y = h + s_Y
                return rect(s_X, s_Y, e_X, e_Y)
            return None
        except Exception as e:
            log.error(f"match_img<{img.name}> 发生错误: {e}")
            return None
    def match_color_img(self, img: image, accuracy=0.8,color_simi_acc=0.9)->rect:
        # 彩色图像模板匹配
        try:
            if matched_img := self.match_img(img, accuracy=accuracy):
                
                shot_color_img = cv2.cvtColor(screenshot.get_screenshot(self.child_handle, img.area), cv2.COLOR_BGRA2BGR)
                template_color_img=cv2.imread(img.path, cv2.IMREAD_COLOR)
                color_simi=np.mean((shot_color_img-template_color_img)**2)
                print(matched_img,color_simi)
                return matched_img if color_simi<color_simi_acc else None
            else:
                return None
        except Exception as e:
            print(f"match_color_img 发生错误: {e}")
            return None

        pass
    def match_duo_img(self, img:image, accuracy=0.8,debug=False)->list[image]:#匹配区域内所有相符合的图像
        rec_img_list=[]
        return_list=[]
        try:
            f_shot_img = screenshot.get_screenshot(self.child_handle, img.rect.area)
            shot_img = cv2.cvtColor(f_shot_img, cv2.COLOR_BGRA2GRAY)
            template = cv2.imread(img.path, cv2.IMREAD_GRAYSCALE)
            Res = cv2.matchTemplate(shot_img, template, cv2.TM_CCOEFF_NORMED)
            h, w = template.shape
            loc = np.where(Res >= accuracy)
            for pt in zip(*loc[::-1]):
                s_X = img.rect.s_x + pt[0]
                s_Y = img.rect.s_y + pt[1]
                rec_img_list.append([s_X, s_Y, w, h])
            temp_list,weight= cv2.groupRectangles(rectList=rec_img_list, groupThreshold=1, eps=0.2)
            if debug:
                for pt in temp_list:
                    start=Point(pt[0]-img.rect.s_x,pt[1]-img.rect.s_y)
                    end=Point(start.x+w,start.y+h)
                    cv2.rectangle(f_shot_img, start, end, (0, 255, 0), 2)
                cv2.imshow("shot_img", f_shot_img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            # 将return_list的w,h转换为e_x,e_y，并且转换为rect对象
            for img_ in temp_list:
                img_[2]+=img_[0]
                img_[3]+=img_[1]
                img_area=[img_[0],img_[1],img_[2],img_[3]]
                return_list.append(image(img.path,img_area,img.name))
            return return_list
        except Exception as e:
            print(f"match_duo_img 发生错误: {e}")
            return None
    def find_duo_img(self, img_dir:str, match_area:list,accuracy=0.8,return_only_one=False)->dict|list:#查找目录下所有图片，返回符合条件的图片坐标
        return_dict={}
        try:
            path = pathlib.Path(img_dir)
            img_list =[img_file for img_file in path.glob('*') if img_file.is_file()]
            ShotImage = cv2.cvtColor(screenshot.get_screenshot(self.child_handle, rect(match_area)), cv2.COLOR_BGRA2GRAY)
            for img in img_list:
                #print(img)
                template = cv2.imread(str(img), cv2.IMREAD_GRAYSCALE)
                Res = cv2.matchTemplate(ShotImage, template, cv2.TM_CCOEFF_NORMED)
                if cv2.minMaxLoc(Res)[1] > accuracy:
                    matchCor = cv2.minMaxLoc(Res)[3]
                    h, w = template.shape
                    s_X = match_area[0] + matchCor[0]
                    s_Y = match_area[1] + matchCor[1]
                    e_X = w + s_X
                    e_Y = h + s_Y
                    if return_only_one:return [img, [s_X, s_Y, e_X, e_Y],img.stem]
                    return_dict[img.stem]=[s_X, s_Y, e_X, e_Y]
            if return_dict:return return_dict
            else:return None
        except Exception as e:
            print(f"find_duo_img 发生错误: {e}")
            return None
    def stat_reward(self, need_stat_dir:str,match_area:list, accuracy=0.9)->dict:
        return self.find_duo_img(need_stat_dir, match_area, accuracy=accuracy, return_only_one=False)
                       
    
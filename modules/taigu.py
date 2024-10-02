# this file is achieve the function of taigu.
# author: yancj
import os
from sys import path

path.append(os.path.dirname(os.path.dirname(__file__)))
from mytool.datatype import Point, rect, image
from mytool.click import Mouse
from mytool.recimg import ImgRec
from mytool.mylog import MyLog
from mytool.client import client
from mytool.Ocr import Ocr
from img.taigu.taigu_img_info import *
from time import sleep
from mytool.SwitchUI import SwitchUI

log = MyLog()


class Taigu(Mouse, ImgRec):
    def __init__(self):
        super().__init__()
        self.page_switch = SwitchUI()
        self.switch = False
        self.ui_list = [jy_ui, jy_out]
        self.is_flashed = False
        self.temp_max = 59
        self.lef_max = None
        self.right_max = None
        self.next_time = None
        self.max = self.temp_max
        Ocr.par_handle = self.par_handle
        Ocr.child_handle = self.child_handle

    def flash_taigu_list(self):
        # 滑动到地步刷新好友的结界列表
        self.slide(Point(190, 191), Point(186, 530), move_time=1)
        self.random_click([350, 105, 434, 151])  # 点击切换到跨区好友
        sleep(1)
        log.info(f"开始刷新跨区列表")
        self.slide(Point(190, 191), Point(186, 530), move_time=1)  # 刷新跨区好友列表
        self.random_click([243, 109, 307, 141])  # 点击切换到同区好友
        # 刷新完成
        self.is_flashed = True
        log.info("flash completed")
        pass

    def get_num(self, result: list[image], mode: str):
        log.info(f"mode:{mode}\nresult:{result}")
        for img in result:
            self.random_click(img.rect)
            sleep(1.5)
            if res := Ocr().ocr([832, 423, 946, 446]):
                if "勾玉" in res[0]:
                    num = (
                        int("".join(char for char in res[0] if char.isdigit()))
                        if res[1] > 0.7
                        else 0
                    )
                    log.info(f"get_num:{num}")
                else:
                    num = 0
                match mode:
                    case "find":
                        self.temp_max = max(self.temp_max, num)
                        if self.temp_max == 76:
                            self.shoot_target()
                    case "shot":
                        if num >= self.max:
                            self.shoot_target()
                            return
        return True

    def refind_max(self):
        log.info(f"refind_max:{self.lef_max},{self.right_max}")
        self.max = max(self.lef_max, self.right_max)
        result = []
        if not self.is_flashed:
            self.flash_taigu_list()
        for _ in range(2):
            for i in range(4):
                sleep(1)
                if self.switch:
                    return
                if res := self.match_duo_img(
                    tg_6x,
                ):
                    result = res
                if res := self.match_duo_img(
                    tg_5x,
                ):
                    result += res
                self.get_num(result, "shot")
                self.random_click([428, 192, 461, 249])  # 428,192,461,249
                sleep(0.5)
                self.mouse_scroll(
                    ("down", 5 + i % 2), *rect(283, 177, 578, 584).random_point
                )
                sleep(0.5)
                result = []
            self.random_click([350, 105, 434, 151])  # 切换到跨区寻找
            sleep(1)
        log.info(f"not found max:{self.temp_max}")
        self.switch = True
        self.next_time = 3  # 3分钟后再次寻找
        self.page_switch.switch_to("in_jj")
        pass

    def find_max(self):
        result = []
        if not self.is_flashed:
            self.flash_taigu_list()
        for i in range(4):
            sleep(1.5)
            if self.switch:
                return
            if res := self.match_duo_img(tg_6x, debug=False):
                result = res
            if res := self.match_duo_img(tg_5x, debug=False):
                result += res
            log.info(f"find_max:{result}")
            self.get_num(result, "find")
            self.random_click([428, 192, 461, 249])  # 428,192,461,249
            sleep(0.5)
            self.mouse_scroll(
                ("down", 5 + i % 2), *rect(370, 268, 473, 491).random_point
            )
            sleep(0.5)
            result = []
        if self.lef_max is None:
            self.lef_max = self.temp_max
            self.random_click([350, 105, 434, 151])  # 切换到跨区好友寻找

        elif self.right_max is None:
            self.right_max = self.temp_max
            self.random_click([243, 109, 307, 141])  # 切换到同区好友寻找
            self.refind_max()
        pass

    def shoot_target(self):
        self.max = self.temp_max
        log.info(f"shoot_target:{self.max}")
        self.random_click([830, 550, 928, 585])
        sleep(2)
        self.random_click([469, 539, 500, 607])
        sleep(1)
        self.random_click([692, 528, 780, 555])
        self.next_time = 360
        self.switch = True
        pass

    def jy_match(self):
        res = self.match_img(kjy_ui)
        match res:
            case None:
                # log.error("No match jy_ui")

                if time := Ocr().ocr([1145, 123, 1236, 144])[0]:
                    log.info(f"get_next_time:{time}")
                    self.next_time = (
                        int(time.split(":")[0]) * 60 + int(time.split(":")[1]) + 1
                    )
                    self.switch = True
            case x if x is not None:
                self.random_click(x)

    def run(self):
        curr_ui = self.match_ui(self.ui_list)
        match curr_ui:
            case "jy_out":
                self.jy_match()
            case "jy_ui":
                self.find_max()
            case _:
                log.error("No match ui")

        pass


def taigu_run():
    if client.get_handle("MuMu模拟器12"):  # 已经启动
        log.info("MuMu模拟器12 is running")
    else:
        log.error("MuMu模拟器12 is starting")
        client.start()
        client.kill_app = True
        sleep(10)
    taigu = Taigu()
    while not taigu.page_switch.switch_to("jy_out"):
        sleep(1)
    while not taigu.switch:
        sleep(1)
        taigu.run()
    log.info(f"next_time:{taigu.next_time}")
    if hasattr(client, "kill_app"):
        log.info(f"attr(client,kill_app):{client.kill_app}")
        if client.kill_app:
            client.stop()
            log.info("MuMu模拟器12 is stoped")
    return taigu.next_time


if __name__ == "__main__":
    # from time import sleep
    # taigu=Taigu()
    # # taigu.page_switch.switch_to('jy_out')
    # # while True:
    # #     sleep(1)
    # #     taigu.run()
    # while True:
    #     taigu.get_next_time()
    #     sleep(1)
    taigu_run()

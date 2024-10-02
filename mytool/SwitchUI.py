import networkx as nx
from time import sleep
import os
from sys import path

path.append(r"E:\python\mumu_tuntunshu")
from img.switch_ui.switch_img_info import *
from mytool.click import Mouse
from mytool.recimg import ImgRec
from mytool.mylog import MyLog

log = MyLog()

# import matplotlib.pyplot as plt
# 根据最短路径具体需要实施的每一步切换的点击操作的坐标
ui_map = {
    "jy_ui": {
        "jy_out": (24, 24, 56, 61),
    },
    "in_jj": {
        "jy_out": (615, 339, 626, 407),
    },
    "jy_out": {
        "in_jj": (24, 24, 56, 61),
        "jy_ui": (1159, 61, 1204, 118),
    },
    "yyl": {"in_jj": (1079, 633, 1113, 675)},
    "home_top": {
        "yyl": (563, 609, 598, 659),
    },
    "home": {
        "home_top": (1188, 626, 1208, 679),
    },
    "server_ui": {"home_top": (573, 576, 713, 618)},
}
# 构建切换ui的路径图，主要是为了寻找最短路径
G = nx.Graph()
for start_ui, target_ui_dict in ui_map.items():
    G.add_node(start_ui)
    for target_ui, pos in target_ui_dict.items():
        G.add_edge(start_ui, target_ui, weight=len(pos) if type(pos) == list else 1)


class SwitchUI:
    _instance = None

    def __new__(cls, *arg, **kw):  # 确保只有一个实例
        if not cls._instance:
            cls._instance = super(SwitchUI, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.click = Mouse()
        self.imageRec = ImgRec()

    def find_current_ui(self):  # 寻找当前的ui
        for key in ui_map:
            if self.imageRec.match_img(ui_list[key]):
                return key
            sleep(0.1)

    def switch_to(self, target_ui):
        # 判断当前ui是否位于uimap，能够切换ui
        if start_ui := self.find_current_ui():
            log.info(f"@SwitchUI: Current ui is {start_ui},switch to {target_ui}")
        else:
            log.info(
                f"@SwitchUI: Can't find current ui, handle:{self.click.child_handle}"
            )
            # 如果当前ui未找到，则大概率是因为handle获取不正确，尝试重新初始化获取
            self.click.__init__()
            self.imageRec.__init__()
            return False
        # 如果当前ui即是目标ui，则直接返回
        if start_ui == target_ui:
            return True
        # 寻找最短路径并执行切换操作
        while self.find_current_ui() != target_ui:
            start_ui = self.find_current_ui()  # 获取当前的ui位置
            if not start_ui:
                sleep(1)
                continue  # 如果当前ui未找到，则等待1秒再次尝试
            path = nx.shortest_path(
                G, start_ui, target_ui
            )  # 获得当前ui到目标ui的最短路径
            log.info(f"[{start_ui}]->[{target_ui}] \nby path:{path}")
            # 根据最短路径和uimap循环执行操作直到到达最终的目标ui
            for page, next_page in zip(path, path[1:]):
                if page in ui_map:
                    for ui, pos in ui_map[page].items():
                        if ui == next_page:
                            # logger.info(f"[{page}]->[{next_page}]")
                            # 如果切换ui需要多次点击，则为tuple构成的 list
                            # 如果只需要单击一次，则为单个tuple
                            if type(pos[0]) == tuple:
                                for p in pos:
                                    self.click.random_click(p)
                                    sleep(0.8)
                            else:
                                self.click.random_click(pos)
                                sleep(1)
                else:
                    log.info(f"{page} not in ui_map")
        return True  # 切换成功，返回True

    # def draw_map(self):
    #    nx.draw(G, with_labels=True, node_color="lightblue", node_size=700, font_weight="bold")
    #    plt.show()


if __name__ == "__main__":
    switch = SwitchUI()
    switch.switch_to("jy_out")
    pass
    # nx.draw(G, with_labels=True, node_color="lightblue", node_size=700, font_weight="bold")
    # plt.show()

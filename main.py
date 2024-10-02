import PySimpleGUI as sg
from gui.psgrewrite import sw_Button
from gui.home_page import layout
from mytool.taskmgr import TaskManager


class myapp:
    def __init__(self):
        # super().__init__('Mumu Tuntunshu', self.layout, finalize=True)
        self.layout = layout
        self.window = sg.Window("Mumu Tuntunshu", self.layout, finalize=True)
        self.taskmgr = TaskManager(self.window)
        self.run()

    def run(self):
        while True:
            event, values = self.window.read()
            match event:
                case sg.WIN_CLOSED:
                    break
                case "main_sw":
                    self.taskmgr.excute_task("test")
                case "task_end":
                    self.taskmgr.task_end()
        self.window.close()


if __name__ == "__main__":
    myapp()

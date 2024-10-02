from threading import Timer, Thread
from typing import Any
from modules.taigu import taigu_run, log
from time import sleep, strftime, time, localtime
from pystray import Icon, Menu, MenuItem
from PIL import Image

# from mytool.console import Console


class Tuntunshu:
    def __init__(self):
        # Console().hide_console()
        self.next_time = 0
        self.next_t_point = 0
        self.task_state = None
        self.exit_flag = False

        menu = Menu(
            MenuItem("log", self.openlog),
            MenuItem("Next time", self.show_next_time),
            MenuItem("Exit", self.exit),
        )
        self.icon = Icon("Tuntunshu", icon=Image.open("001.ico"), menu=menu)
        self.stray = Thread(target=lambda: self.icon.run, name="stray")
        self.stray.daemon = True
        log.info("Tuntunshu is ready")

    def left_click(self):
        time_str = strftime("%Y-%m-%d %H:%M:%S", localtime(self.next_t_point))
        self.icon.notify("下次蹲点时间", f"{time_str} ")
        self.icon.title = f"{time_str}"
        pass

    def show_next_time(self):
        time_str = strftime("%Y-%m-%d %H:%M:%S", localtime(self.next_t_point))
        self.icon.notify("下次蹲点时间", f"{time_str} ")
        self.icon.title = f"{time_str}"
        pass

    def openlog(self):
        self.show_console()
        pass

    def exit(self):
        self.exit_flag = True
        pass

    def taigu_timer(self):
        self.next_time = taigu_run()
        self.task_state = "finished"
        self.next_t_point = time() + self.next_time * 60
        self.show_next_time()

    def time_to_run(self):
        if self.next_time is not None:
            log.info(f"Creat timer for {self.next_time} minutes")
            timer = Timer(self.next_time * 60, self.taigu_timer)
            timer.daemon = True
            timer.start()
            self.task_state = "not_started"

    def run(self):
        log.info("Tuntunshu is running")
        self.stray.start()
        while not self.exit_flag:
            match self.task_state:
                case "finished" | None:
                    self.time_to_run()
                case "not_started":
                    # log.info('last task is not finished yet')
                    pass
            sleep(1)


if __name__ == "__main__":
    tuntunshu = Tuntunshu()
    log.info("Tuntunshu is running")
    tuntunshu.run()

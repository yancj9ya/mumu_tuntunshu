# 实现自己的log工具
# 1、可以分级为info、debug、error
# 2、如果没有gui对象，输出到console
# 3、可以自定义输出格式
from datetime import datetime


class MyLog:
    log_out_list = []

    def __init__(self):
        pass

    def add_log_out(self, out):
        self.log_out_list.append(out)

    def fmt_msg(self, msg, level):
        with open("log.txt", "r", encoding="utf-8") as f:
            exists_content = f.read()
        new_content = (
            f"[{level}]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {msg}\n"
            + exists_content
        )
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write(new_content)

        match level:
            case "info":
                return f"[INFO] {msg}"
            case "debug":
                return f"[DEBUG] {msg}"
            case "error":
                return f"[ERROR] {msg}"
            case _:
                return f"[OTHER] {msg}"
        pass

    def info(self, msg, *args, **kwargs):
        if self.log_out_list:
            for out in self.log_out_list:
                out.print(self.fmt_msg(msg, "info"), **kwargs)
        else:
            print(self.fmt_msg(msg, "info"), **kwargs)

        pass

    def debug(self, msg, *args, **kwargs):
        if self.log_out_list:
            for out in self.log_out_list:
                out.print(self.fmt_msg(msg, "debug"), **kwargs)
        else:
            print(self.fmt_msg(msg, "debug"), **kwargs)

        pass

    def error(self, msg, *args, **kwargs):
        if self.log_out_list:
            for out in self.log_out_list:
                out.print(self.fmt_msg(msg, "error"), **kwargs)
        else:
            print(self.fmt_msg(msg, "error"), **kwargs)
        pass

    def print(self, msg):
        pass

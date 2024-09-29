# 这个地方用来处理gui发出的各种任务
# todo list：
#     1. 实现任务的立马执行
#     2. 实现任务的定时执行
#     3. 实现任务的停止的时间判定和次数条件判定
#     4. 实现任务的优先级判定
from modules import test
from mytool.mylog import MyLog
log=MyLog()
class TaskManager:
    def __init__(self,window):
        self.window = window
        self.task_list = []
        self.current_task = None
        self.task_map = {'test':test.test}

    def excute_task(self, task):
        self.window.perform_long_operation(lambda: self.task_map[task](),'task_end')
        self.current_task = task
        pass
    
    def task_end(self):
        log.info(f'task end: {self.current_task}')
        self.current_task = None
        pass
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import PySimpleGUI as sg
from psgrewrite import sw_Button
from mytool import mylog,taskmgr

log=mylog.MyLog()
test_button=sw_Button(button_text="Test Button",button_key="test_button",button_color="blue")
output=sg.Multiline(s=(50,20))
log.add_log_out(output)
layout=[[test_button],[output]]
window=sg.Window("Test Window",layout)
taskmgr=taskmgr.TaskManager(window=window)
while True:
    event,values=window.read()
    match event:
        case sg.WIN_CLOSED:
            break
        case "test_button":
            log.info("Test Button Pressed")
            log.info(f'log_id:{id(log)}')

            taskmgr.excute_task('test')
        case 'task_end':
            taskmgr.task_end()
window.close()
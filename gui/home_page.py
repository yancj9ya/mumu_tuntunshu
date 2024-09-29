import PySimpleGUI as sg
from gui.psgrewrite import sw_Button
from mytool.mylog import MyLog
log=MyLog()



sw_button=sw_Button(button_text="start",button_key="main_sw")
out_log=sg.Multiline(s=(50,20))

layout = [
    [sw_button],
    [out_log]
]

log.add_log_out(out_log)
# This file is used to store the image information of the switch UI.
from sys import path
path.append(r'E:\python\mumu_tuntunshu')
from mytool.datatype import image
jy_ui=image('img/taigu/jy_ui.bmp',[843,172,921,214],'jy_ui')
in_jj=image('img/switch_ui/in_jj.bmp',[115,353,251,495],'in_jj')
jy_out=image('img/switch_ui/jy_out.bmp',[23,625,65,684],'jy_out')
yyl=image('img/switch_ui/yyl.bmp',[1079,633,1113,675],'yyl')
home=image('img/switch_ui/home.bmp',[369,34,391,77],'home')
home_top=image('img/switch_ui/home_top.bmp',[494,16,521,49],'home_top')
server_ui=image('img/switch_ui/server_ui.bmp',[20,569,59,617],'server_ui')

ui_list={key:value for key,value in locals().items() if isinstance(value,image)}
if __name__=='__main__':
    print(ui_list)
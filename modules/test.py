import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mytool import mylog
from mytool.recimg import ImgRec
from img.test.test_img_info import *
log=mylog.MyLog()   

def test():
    eye=ImgRec()

    if res:=eye.match_img(coin):
        log.info(f"识别结果:{res.area}\n")
        print(*res.area,sep='\n')
    else:
        log.info("未识别到")
        
    
if __name__=="__main__":
    test()
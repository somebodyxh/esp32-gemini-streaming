from CODE_Python.config import SCNEIDER
from CODE_Python.Api import Run_Api
#指定esp32串口

#主要功能一：发送与回传消息                  
def Massger(msg):
#其他ai和功能我会慢慢更新
    if SCNEIDER == "api":
            Run_Api()                  

if __name__ == "__main__":
    Massger(None)
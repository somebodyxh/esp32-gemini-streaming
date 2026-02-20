from CODE_Python.config import SCNEIDER
from CODE_Python.Selenium import Run_Selenium
#指定esp32串口

#主要功能1 发送与回传消息                  
def Massger(msg):
    if SCNEIDER == "selenium":
        Run_Selenium()
#目前只针对chrome和gemini作了实现 其他浏览器和ai我会慢慢更新 以下是api部分                         



if __name__ == "__main__":
    Massger(None)
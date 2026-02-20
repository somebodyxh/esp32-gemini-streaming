#config.py
#通过这个文件修改实现方案
SCNEIDER = None
def USER_Scneider():
    return  input("输入你想使用的实现方案 \n selenium:启动浏览器 通过浏览器css类进行操作 配置麻烦但功能多\n api:自己导入api使用 功能较少（还没有开发目前）\n >>")
SCNEIDER = USER_Scneider()#selenium借助浏览器css类 可以做到切换话题等 api就是简单的api调用
print("您选择的是"+SCNEIDER)
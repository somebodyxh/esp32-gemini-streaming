#config.py
#通过这个文件修改全局函数
SCNEIDER = None
def USER_Scneider():
    return  input("输入你想使用的实现方案 \n  api:自己导入api使用 /\n 后续方案请等待正在开发中\n >>")
SCNEIDER = USER_Scneider()
print("您选择的是"+SCNEIDER)

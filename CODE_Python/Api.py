import serial
from CODE_Python.Port import Port_Open
from CODE_Python.Loop import Loop
from CODE_Api.Gemini_Api import Gemini_Api, Gemini_Api_APIKEY,Gemini_Api_AIlist
from CODE_Api.Deepseek_Api import DeepSeek_Api,DeepSeek_Api_AIlist,DeepSeek_Api_APIKEY


def Run_Api():
    # 1. 选择后端
    backends = {
        "1": ("Gemini  API", "Gemini"),
        "2": ("Deepseek Api", "Deepseek")
    }#在这里添加想要的AI
    print("请选择要使用的 AI 后端：")
    for key, (name, _) in backends.items():
        print(f"  {key}. {name}")
    USER_Api_choice = input("输入编号: ").strip()
    if USER_Api_choice not in backends:#USER_Api_choise就是用户选择的api实现
        print("无效选择，退出")
        return
    if USER_Api_choice == "1":  # Gemini
            # 初始化 AI 客户端
            client = Gemini_Api_APIKEY()
            models = Gemini_Api_AIlist(client)
            
            # 打印列表让用户选
            print("请选择要使用的模型：")
            for i, m in enumerate(models):
                print(f"  {i}: {m}")
            models = models[int(input("选择模型编号: "))]

            # 包装 AI 调用函数
            ai_func = lambda msg: Gemini_Api(client, msg,models)

            # 选择并打开串口
            Port_Open()
    elif USER_Api_choice == "2":  # DeepSeek
            client = DeepSeek_Api_APIKEY()
            models = DeepSeek_Api_AIlist(client)

            # 打印列表让用户选
            print("请选择要使用的模型：")
            models = client.models.list()
            for i, m in enumerate(models.data):
                print(f"  {i}: {m.id}")
            models = models.data[int(input("选择模型编号: "))].id
            
            # 3. 包装 AI 调用函数
            ai_func = lambda msg: DeepSeek_Api(client, msg,models)

            # 4. 选择并打开串口
            Port_Open()



    # 5. 启动主循环
    ser = Port_Open()
    if ser is None:
        return
    Loop(ser, ai_func)

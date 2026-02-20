       
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from serial.tools import list_ports
from CODE_Python.Port import select_serial_port
from CODE_Python.Send import throttled_serial_send
import time
import os
import platform
import serial
def Run_Selenium():
    SYSTEM = platform.system()
    NAME_AI = input("在这里选择你想使用的ai ").strip().lower()
    if NAME_AI == "gemini":
        def user_chrome():
        #这是获取你上chrome用户配置的功能阿 临时目录也行 就是要重新登录。。。。。。。。我这一段写的和shit一样 轻喷
            print("输入你浏览器用户配置 ")
            if SYSTEM == "Windows":
                USER_Input_Windows = input("输入你的用户配置地址 可以拖拽文件夹 或输入 'skip' 使用临时目录（不推荐，可能导致登录信息丢失）")
                if USER_Input_Windows.strip().lower() == "skip":  
                    if USER_Input_Windows == "skip":
                        # 创建一个临时目录
                        import tempfile
                        temp_dir = tempfile.mkdtemp(prefix="chrome_profile_")
                        print(f"使用临时目录: {temp_dir}")
                        return temp_dir
                else:
                    # 移除引号
                    dir = USER_Input_Windows.strip('"').strip("'")
                    return os.path.abspath(dir)
            else:  # Linux
                    print("请输入用户数据目录路径（留空则使用 ~/.config/google-chrome/Gemini_Pro)")
                    USER_Input_Linux = input("路径: ").strip()
                    if USER_Input_Linux:
                        return os.path.abspath(USER_Input_Linux)
                    else:
                        USER_Input_Linux= os.path.expanduser("~/.config/google-chrome/Gemini_Pro")
                        os.makedirs(USER_Input_Linux, exist_ok=True)
                        return USER_Input_Linux
        def SYSTEM_Config():
            if SYSTEM == "Windows":
                # Windows 串口号 (根据实际情况修改)
                COM_PORT = select_serial_port()
                # Chrome 用户数据目录 
                USER_DIR = user_chrome()
            else:
                # Linux 串口号 
                COM_PORT = select_serial_port()
                # Chrome 用户数据目录 Linux 
                USER_DIR = user_chrome()

            BAUD_RATE = 115200

                 
            def init_driver():
                options = Options()
                # 确保目录存在（可选）
                os.makedirs(USER_DIR, exist_ok=True)
                options.add_argument(f"--user-data-dir={USER_DIR}")
                
                # Linux 下可能需要添加以下参数以避免沙盒权限问题
                # if SYSTEM != "Windows":
                #     options.add_argument("--no-sandbox")
                #     options.add_argument("--disable-dev-shm-usage")

                d = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=options
                )
                d.get("https://gemini.google.com/gems/create?hl=en-US&pli=1")
                return d

            print(f"[*] 系统识别: {SYSTEM}")
            print(f"[*] 串口: {COM_PORT}")
            print(f"[*] 用户数据目录: {USER_DIR}")

            # ========== 全局变量 ==========
            driver = init_driver()
            ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.01)


            last_reply = ""
            current_topics = []
            waiting_for_reply = False
            is_transmitting = False

            # ========== 辅助函数 ==========

            def sync_topics():
                nonlocal current_topics
                try:
                    items = driver.find_elements(By.CSS_SELECTOR, "a[data-test-id='conversation']")
                    current_topics = []
                    for item in items[:10]:
                        try:
                            title = item.find_element(By.CSS_SELECTOR, ".conversation-title").text.strip()
                            if title:
                                current_topics.append(title)
                        except:
                            continue
                    if current_topics:
                        menu = "【对话列表】\n" + "\n".join([f"{i}.{t[:10]}" for i, t in enumerate(current_topics, 1)])
                        throttled_serial_send(ser, menu)
                except Exception as e:
                    print(f"[X] sync_topics 异常: {e}")

            # ========== 主循环 ==========
            print("[*] 就绪")

            while True:
                try:
                    # 检查浏览器是否还活着
                    _ = driver.window_handles

                    # 1. 监控 Gemini 回复
                    if waiting_for_reply and not is_transmitting:
                        stop_btn_selector = "button:has(.mat-mdc-button-touch-target)[aria-label*='Stop'], button:has(.mat-mdc-button-touch-target)[aria-label*='停止']"
                        if len(driver.find_elements(By.CSS_SELECTOR, stop_btn_selector)) == 0:
                            full_text = driver.execute_script("return document.body.innerText;")
                            if "【START】" in full_text and "【END】" in full_text:
                                s_idx = full_text.rfind("【START】") + 7
                                e_idx = full_text.rfind("【END】")
                                content = full_text[s_idx:e_idx].strip()
                                if content and content != last_reply:
                                    throttled_serial_send(ser, content)
                                    last_reply = content
                                    waiting_for_reply = False

                    # 2. 处理串口指令
                    if ser.in_waiting:
                        line = ser.readline().decode('utf-8', errors='ignore').strip()
                        if "[SENSOR]" in line:
                            print(f"[*] 硬件状态 -> {line}")
                        elif "[CMD]" in line:
                            msg = line.split("[CMD]")[-1].strip()
                            print(f"[CMD] 收到指令: {msg}")

                            if msg == "刷新":
                                sync_topics()
                            elif msg == "新建":
                                new_btn = driver.find_elements(By.CSS_SELECTOR, "a[data-test-id='expanded-button']")
                                if new_btn:
                                    driver.execute_script("arguments[0].click();", new_btn[0])
                                    print("已点击：发起新对话")
                                    throttled_serial_send(ser, "NEW_CHAT_OK")
                                else:
                                    driver.get("https://gemini.google.com/app")
                                    print("[!] 警告 请检查你是否打开了侧边栏 已通过 URL 跳转新建")
                                waiting_for_reply = False
                            elif msg.isdigit():
                                idx = int(msg) - 1
                                if 0 <= idx < len(current_topics):
                                    els = driver.find_elements(By.CSS_SELECTOR, "a[data-test-id='conversation']")
                                    driver.execute_script("arguments[0].click();", els[idx])
                                    waiting_for_reply = False
                            elif msg:
                                # 发送消息给 Gemini
                                box = driver.find_element(By.CSS_SELECTOR, "div.ql-editor.textarea")
                                box.send_keys(msg + Keys.ENTER)
                                waiting_for_reply = True
                                last_reply = ""

                except (InvalidSessionIdException, WebDriverException):
                    print("[!] 浏览器会话中断，正在重启...")
                    try:
                        driver.quit()
                    except:
                        pass
                    time.sleep(2)
                    driver = init_driver()
                except Exception as e:
                    print(f"运行时异常: {e}")
        SYSTEM_Config()

import time
from CODE_Python.Send import throttled_serial_send


def Loop(ser, AI_Func):
    print("\n就绪")
    while True:
        try:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if not line:
                    continue
                # 识别 [CMD] 指令
                if "[SENSOR]" in line:
                    print(f"[*] 硬件状态 -> {line}")
                elif "[CMD]" in line:
                    msg = line.split("[CMD]")[-1].strip()
                    print(f"[CMD] 收到指令: {msg}")
                    try:
                        reply = AI_Func(msg)#AI回答
                        if reply:
                            throttled_serial_send(ser, reply)#调用回传函数回传
                        else:
                            throttled_serial_send(ser, "[返回空]")
                    except Exception as e:
                        error_msg = f"[AI 调用失败] {e}"
                        print(error_msg)
                        throttled_serial_send(ser, error_msg)
            time.sleep(0.05)
        except KeyboardInterrupt:
            print("\n用户中断,退出")
            break
        except Exception as e:
            print(f"运行时异常: {e}")
            time.sleep(1)

    ser.close()
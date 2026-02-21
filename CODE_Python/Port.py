#Port.py
#通过这个文件修改串口
import serial
import serial.tools.list_ports

#指定esp32串口

def select_serial_port():
                    
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("没有检测到任何串口设备")
        exit(1)
    
    print("检测到以下串口：")
    for i, port in enumerate(ports):
        print(f"   {i}: {port.device} - {port.description}")
    
    while True:
        try:
            choice = input("请选择串口编号 (0~{}): ".format(len(ports)-1)).strip()
            if not choice:
                print("输入不能为空，请重新输入。")
                continue
            idx = int(choice)
            if 0 <= idx < len(ports):
                selected = ports[idx].device
                print(f"选择: {selected}")
                return selected
            else:
                print(f"编号超出范围，请输入 0~{len(ports)-1} 之间的数字。".format(len(ports)-1))
        except ValueError:
            print("请输入有效的数字。")
        except KeyboardInterrupt:
            print("\n用户取消 退出。")
            exit(0)

def Port_Open():
    port = select_serial_port()
    try:
        ser = serial.Serial(port, 115200, timeout=0.01)
        print(f"串口 {port} 打开成功")
    except Exception as e:
        print(f"打开串口失败: {e}")
        return None
    return ser
if __name__ == "__main__":
    port = select_serial_port()
    print(f"串口是：{port}")
#Send.py
#通过这个回传
import time
is_transmitting = False

def throttled_serial_send(ser, text):
                            global is_transmitting
                            is_transmitting = True
                            try:
                                full_msg = f"\r\n[AI]: {text}\r\n"
                                data = full_msg.encode('utf-8', errors='ignore')
                                print(f"[回传 (共 {len(data)} 字节)...")

                                chunk_size = 6
                                for i in range(0, len(data), chunk_size):
                                    # 检查是否有新指令打断
                                    if ser.in_waiting > 0:
                                        incoming = ser.read(ser.in_waiting)
                                        if b'[' in incoming:
                                            print("\n 检测到新指令，回传中断")
                                            break
                                    chunk = data[i:i+chunk_size]
                                    ser.write(chunk)
                                    ser.flush()
                                    time.sleep(0.05)
                                    print(chunk.decode('utf-8', errors='ignore'), end='', flush=True)
                                print("\n回传完毕")
                            except Exception as e:
                                print(f"\n回传出错: {e}")
                            finally:
                                is_transmitting = False
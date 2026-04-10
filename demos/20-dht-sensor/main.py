import adafruit_dht
import board
import time

dht_device = adafruit_dht.DHT11(board.D4)

print("DHT11 温湿度传感器已启动，按 Ctrl+C 退出")
try:
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            if temperature is not None and humidity is not None:
                print(f"温度: {temperature:.1f}°C, 湿度: {humidity:.1f}%")
            else:
                print("读取失败，重试...")
        except RuntimeError as e:
            print(f"读取错误: {e}")
        time.sleep(2)
except KeyboardInterrupt:
    print("退出")
finally:
    dht_device.exit()

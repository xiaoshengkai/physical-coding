from picamera2 import Picamera2
import time

picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()
time.sleep(2)

picam2.capture_file("test.jpg")
print("照片已保存为 test.jpg")
picam2.stop()

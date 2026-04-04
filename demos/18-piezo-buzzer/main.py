import RPi.GPIO as GPIO
import time

buzzer_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

# 音符频率映射（单位：Hz）
tones = {
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349, 'G4': 392, 'A4': 440, 'B4': 494,
    'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784, 'A5': 880, 'B5': 988,
    'C6': 1047, 'D6': 1175, 'E6': 1319, 'F6': 1397, 'G6': 1568, 'A6': 1760, 'B6': 1976,
    'R': 0  # 休止符
}

# 《小星星》完整旋律（两段主题 + 重复一次）
# 每个音符的时长（秒），通过 base_duration 统一控制
base_duration = 0.6   # 一拍的长度（秒），可调整以改变总时长
melody = [
    # 第一段：1 1 5 5 | 6 6 5 - | 4 4 3 3 | 2 2 1 - |
    ('C4', 1), ('C4', 1), ('G4', 1), ('G4', 1), ('A4', 1), ('A4', 1), ('G4', 2),
    ('F4', 1), ('F4', 1), ('E4', 1), ('E4', 1), ('D4', 1), ('D4', 1), ('C4', 2),
    # 第二段：5 5 4 4 | 3 3 2 - | 5 5 4 4 | 3 3 2 - |
    ('G4', 1), ('G4', 1), ('F4', 1), ('F4', 1), ('E4', 1), ('E4', 1), ('D4', 2),
    ('G4', 1), ('G4', 1), ('F4', 1), ('F4', 1), ('E4', 1), ('E4', 1), ('D4', 2),
    # 重复第一段
    ('C4', 1), ('C4', 1), ('G4', 1), ('G4', 1), ('A4', 1), ('A4', 1), ('G4', 2),
    ('F4', 1), ('F4', 1), ('E4', 1), ('E4', 1), ('D4', 1), ('D4', 1), ('C4', 2),
    # 重复第二段
    ('G4', 1), ('G4', 1), ('F4', 1), ('F4', 1), ('E4', 1), ('E4', 1), ('D4', 2),
    ('G4', 1), ('G4', 1), ('F4', 1), ('F4', 1), ('E4', 1), ('E4', 1), ('D4', 2),
]

def play_tone(pin, frequency, duration):
    if frequency == 0:
        time.sleep(duration)
        return
    p = GPIO.PWM(pin, frequency)
    p.start(50)
    time.sleep(duration)
    p.stop()

try:
    print("开始播放《小星星》完整旋律（约1分钟）...")
    total_time = 0
    for note, beats in melody:
        duration = beats * base_duration
        frequency = tones.get(note, 0)
        print(f"播放 {note} ({frequency}Hz) 持续 {duration:.2f}秒")
        play_tone(buzzer_pin, frequency, duration)
        time.sleep(0.05)   # 音符间短停顿
        total_time += duration + 0.05
    print(f"播放完成，总时长约 {total_time:.1f} 秒")
except KeyboardInterrupt:
    print("播放中断")
finally:
    GPIO.cleanup()
    print("GPIO已清理")
import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

print("按 q 退出")

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法获取画面")
        break

    cv2.imshow("Camera Preview", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("退出")

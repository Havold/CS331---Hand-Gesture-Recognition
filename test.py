import cv2
import time
import os
import mediapipe as mp
import hand as htm

cap = cv2.VideoCapture('http://192.168.137.106:8080/video')

# Model load
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands (
#     static_image_mode = use_static_image_mode,
#     max_num_hands = 2,
#     min_detection_confidence = min_detection_confidence,
#     min_tracking_confidence = min_tracking_confidence,
# )

DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 3
dataset_size = 100


folderPath = 'images'
lst = os.listdir(folderPath)
lst_2 = []
for i in lst:
    image = cv2.imread(f"{folderPath}/{i}")
    lst_2.append(image)

pTime = 0
# detector = htm.handDetector(detectionCon=0.55) # phát hiện ra bàn tay với độ chính xác 0.55

# while True:
#     ret, frame = cap.read()

#     frame = detector.findHands(frame) 
#     lmList = detector.findPosition(frame,draw=False) # Phát hiện vị trí và gán 20 điểm đó vào list
#     print(lmList)

#     h,w,c = lst_2[0].shape
#     frame[0:h,0:w] = lst_2[0]

#     # Viết ra FPS
#     cTime = time.time() # trả về số giây, tính từ 0:0:00 ngày 1/1/1970 theo giờ UTc, gọi là giời điểm bắt đầu thời gian)
#     fps = 1/(cTime-pTime) # Tính fps (frame per second - chỉ số khung hình trên mỗi giây)
#     pTime = cTime
    
#     # show fps lên màn hình
#     cv2.putText(frame,f"FPS: {int(fps)}",(w+10,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

#     cv2.imshow("Test",frame)
#     if cv2.waitKey(1) == ord("q"): # Độ trễ 1/1000s, nếu bấm q sẽ thoát
#         break

for j in range(0,number_of_classes):
    if not os.path.exists(os.path.join(DATA_DIR,str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

        print(f'Collecting data for class {j}')

        done=False
        while True:
            ret, frame = cap.read()
            cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                cv2.LINE_AA)
            h,w,c = lst_2[0].shape
            frame[0:h,0:w] = lst_2[0]

            # Viết ra FPS
            cTime = time.time() # trả về số giây, tính từ 0:0:00 ngày 1/1/1970 theo giờ UTc, gọi là giời điểm bắt đầu thời gian)
            fps = 1/(cTime-pTime) # Tính fps (frame per second - chỉ số khung hình trên mỗi giây)
            pTime = cTime
            
            # show fps lên màn hình
            cv2.putText(frame,f"FPS: {int(fps)}",(w+10,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

            cv2.imshow("Test",frame)
            if cv2.waitKey(1) == ord("q"): # Độ trễ 1/1000s, nếu bấm q sẽ thoát
                break
            
        counter = 0
        while counter < dataset_size:
            ret, frame = cap.read()
            cv2.imshow('Test',frame)
            cv2.waitKey(25)
            cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)

            counter +=1
            print(counter)
            print(j)
cap.release() # Giải phóng camera
cv2.destroyAllWindows() # thóa tất cả các cửa sổ
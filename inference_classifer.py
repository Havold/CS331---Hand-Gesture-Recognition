import cv2
import mediapipe as mp
import numpy as np
import pickle

model_dict = pickle.load(open('./model.p','rb'))
model = model_dict['model']

cap = cv2.VideoCapture('http://192.168.137.153:8080/video')

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)
# x1,y1,x2,y2 = [0,0,0,0]
labels_dict = {0: 'Bye', 1: 'Like', 2: 'Peace'}
while True:
    data_aux = []
    ret, frame = cap.read()
    x_ = []
    y_ = []

    H,W,_ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks( # Vẽ các hand_landmarks thu được từ model lên img
                frame, # image to draw
                hand_landmarks, # model output, kết quả thu được từ mô hình
                mp_hands.HAND_CONNECTIONS, # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x=hand_landmarks.landmark[i].x
                y=hand_landmarks.landmark[i].y
                data_aux.append(x)
                data_aux.append(y)
                x_.append(x)
                y_.append(y)
        x1 = int(min(x_) * W)
        y1 = int(min(y_) * H)
        x2 = int(max(x_) * W)
        y2 = int(max(y_) * H)

        prediction = model.predict([np.asarray(data_aux)])
        predicted_sign = labels_dict[int(prediction[0])]
        # print(predicted_sign)
    
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,0), 4)
        cv2.putText(frame, predicted_sign, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
            cv2.LINE_AA)
    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) == ord("q"): # Độ trễ 1/1000s, nếu bấm q sẽ thoát
        break

cap.release() # Giải phóng camera
cv2.destroyAllWindows() # thóa tất cả các cửa sổ
import cv2
import mediapipe as mp
import numpy as np
# import pyautogui
# pyautogui.FAILSAFE = False
import ctypes
# import utils
import time

# Định nghia các hằng số cho chiều rộng và chiều cao màn hình
SM_CXSCREEN = 0
SM_CYSCREEN = 1

# Định nghĩa các hằng số và hàm từ user32.dll
SetCursorPos = ctypes.windll.user32.SetCursorPos
mouse_event = ctypes.windll.user32.mouse_event

# Mã cho các sự kiện chuột
MOUSEEVENTF_MOVE = 0x0001 # di chuyển chuột
MOUSEEVENTF_LEFTDOWN = 0x0002 # nhấn chuột trái
MOUSEEVENTF_LEFTUP = 0x0004 # thả chuột trái
MOUSEEVENTF_RIGHTDOWN = 0x0008 # nhấn chuột phải
MOUSEEVENTF_RIGHTUP = 0x0010 # thả chuột phải
MOUSEEVENTF_WHEEL = 0x0800 # cuộn chuột



# Hàm di chuyển chuột
def move_mouse(x, y):
    SetCursorPos(x, y)

# Hàm nhấn chuột trái
def click_mouse():
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# Hàm nhấn chuột phải
def click_mouse_right():
    mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


# Hàm double click
def double_click():
    mouse_event(MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)
    mouse_event(MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# Hàm scroll chuột
def scroll_mouse(x):
    mouse_event(MOUSEEVENTF_WHEEL, 0, 0, 60 * x, 0)

# Lấy hàm GetSystemMetrics từ user32.dll
user32 = ctypes.windll.user32

# Lấy chiều rộng và chiều cao màn hình
screen_width = user32.GetSystemMetrics(SM_CXSCREEN)
screen_height = user32.GetSystemMetrics(SM_CYSCREEN)


# screen_width, screen_height = pyautogui.size()
cap = cv2.VideoCapture(0)
index_y=0
wrest_y=0
wrest_x=0
middle_MCP_x=0
middle_MCP_y=0

is_Moving=False

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.4, max_num_hands=1)


receive = 1
while True:
    data_aux = []
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
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

        landmarks_list = []

        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                landmarks_list.append([landmark.x,landmark.y]) #Nhận vào các điểm landmark
            index_x_frame = int(landmarks_list[8][0]*W)
            index_y_frame = int(landmarks_list[8][1]*H)

            if index_x_frame < 48:
                index_x = 48
            elif index_x_frame > 592:
                index_x = 592
            if index_y_frame < 87:
                index_y = 87
            elif index_y_frame > 393:
                index_y = 393
            index_x = screen_width/544 * (index_x_frame-48)
            index_y = screen_height/306 * (index_y_frame-87)
            # pyautogui.moveTo(index_x,index_y)
            move_mouse(int(index_x),int(index_y)) #Di chuyển chuột

            #Thực hiện các xử lí
            # if landmarks_list[4] and landmarks_list[3]:
            #     print(landmarks_list[4][0] - landmarks_list[3][0])
            cv2.circle(img=frame, center=(index_x_frame,index_y_frame), radius=20, color=(0,255,255))

            if (landmarks_list[4][0] - landmarks_list[3][0]) < -0.01 and landmarks_list[4][0] < landmarks_list[5][0] and receive == 1:
                # pyautogui.click()
                click_mouse()
                receive = 0
            elif landmarks_list[4][0] > landmarks_list[5][0] and receive == 1:
                # pyautogui.click(button='right')
                click_mouse_right()
                receive = 0
            elif (landmarks_list[12][1] < landmarks_list[10][1]) and receive == 1:
                # pyautogui.doubleClick()
                double_click()
                receive = 0
            elif (landmarks_list[16][1] < landmarks_list[14][1]) and (landmarks_list[20][1] < landmarks_list[18][1]):
            #     # pyautogui.scroll(40)
                scroll_mouse(1)
            elif (landmarks_list[16][1] > landmarks_list[14][1]) and (landmarks_list[20][1] < landmarks_list[18][1]):
            #     pyautogui.scroll(-40)
                scroll_mouse(-1)
            elif landmarks_list[4][0] > landmarks_list[3][0] and landmarks_list[4][0] < landmarks_list[5][0] and (landmarks_list[12][1] > landmarks_list[10][1]):
                receive = 1
            else:
                pass
    # print(receive)

    cv2.rectangle(frame, (48,87), (592, 393), (0,255,0), 2)
    cv2.imshow('Camera', frame)
    cv2.moveWindow('Camera', 0, 0)
    #cv2.setWindowProperty('Camera', cv2.WND_PROP_TOPMOST, 1)
    if cv2.waitKey(1) == ord("q"): # Độ trễ 1/1000s, nếu bấm q sẽ thoát
        break

cap.release() # Giải phóng camera
cv2.destroyAllWindows() # thóa tất cả các cửa sổ
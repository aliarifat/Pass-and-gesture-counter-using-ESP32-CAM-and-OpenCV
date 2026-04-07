import cv2
import mediapipe as mp
import numpy as np
import urllib.request

# ------------------- ESP32 CAMERA URL -------------------
ESP32_URL = "http://192.168.1.104/cam-hi.jpg"  # << CHANGE THIS

# Initialize mediapipe hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Background subtractor for motion/object detection
fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

# Define line position and counters
line_y = 250
pass_counter = 0
gesture_counter = 0
prev_gesture_state = False

# Read frame from ESP32
def get_esp32_frame():
    try:
        img_resp = urllib.request.urlopen(ESP32_URL, timeout=2)
        img_np = np.asarray(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        return frame
    except:
        return None


while True:
    frame = get_esp32_frame()
    if frame is None:
        print("Failed to retrieve frame from ESP32")
        continue

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))

    # ----------------- Object/Pass Counter -----------------
    fgmask = fgbg.apply(frame)
    _, thresh = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame, (0, line_y), (640, line_y), (0, 255, 255), 2)

    for cnt in contours:
        if cv2.contourArea(cnt) > 1500:
            x, y, w, h = cv2.boundingRect(cnt)
            cx = int(x + w / 2)
            cy = int(y + h / 2)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            if abs(cy - line_y) < 6:
                pass_counter += 1
                cv2.line(frame, (0, line_y), (640, line_y), (0, 0, 255), 3)

    # ----------------- Hand Gesture Counter -----------------
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    current_gesture_state = False

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frame.shape
                lmList.append((int(lm.x * w), int(lm.y * h)))

            if lmList:
                # Count raised fingers
                tipIds = [4, 8, 12, 16, 20]
                fingers = []

                # Thumb
                if lmList[tipIds[0]][0] > lmList[tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Other 4 fingers
                for id in range(1, 5):
                    if lmList[tipIds[id]][1] < lmList[tipIds[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                totalFingers = fingers.count(1)
                cv2.putText(frame, f'Fingers: {totalFingers}', (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Consider "open palm" (5 fingers up) as gesture
                if totalFingers == 5:
                    current_gesture_state = True

    # Gesture counts on state change
    if current_gesture_state and not prev_gesture_state:
        gesture_counter += 1
    prev_gesture_state = current_gesture_state

    # ----------------- Display Counters -----------------
    cv2.putText(frame, f'Pass Count: {pass_counter}', (10, 420),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, f'Gesture Count: {gesture_counter}', (10, 460),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show window
    cv2.imshow('ESP32-CAM Combined Counter', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()

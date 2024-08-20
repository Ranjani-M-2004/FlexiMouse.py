import cv2
import mediapipe as mp
import pyautogui
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

while True:
    ret, frame = cap.read()

    if not ret:
        break
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            for landmark in landmarks.landmark:
                
                print(f"Landmark: X: {x}, Y: {y}, Z: {z}")

            index_finger_tip = landmarks.landmark[8]
            index_finger_x = int(index_finger_tip.x * screen_width)
            index_finger_y = int(index_finger_tip.y * screen_height)

            
            pyautogui.moveTo(index_finger_x, index_finger_y)

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

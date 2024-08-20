import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Set up screen size for scrolling
screen_width, screen_height = pyautogui.size()
scroll_speed = 10

# Function to perform scrolling based on hand gestures
def perform_scroll(hand_landmarks):
    # Get landmarks of index and middle fingers
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    # Calculate vertical distance between fingers
    finger_distance = index_tip.y - middle_tip.y

    # Scroll up if fingers are moved upwards
    if finger_distance < -0.1:
        pyautogui.scroll(scroll_speed)
    # Scroll down if fingers are moved downwards
    elif finger_distance > 0.1:
        pyautogui.scroll(-scroll_speed)

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process image with MediaPipe
    results = hands.process(frame_rgb)

    # If hand(s) detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Perform scrolling based on hand gesture
            perform_scroll(hand_landmarks)

            # Visualize hand landmarks (optional)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display output
    cv2.imshow('Hand Gesture Scroll', frame)

    # Check for keypress
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

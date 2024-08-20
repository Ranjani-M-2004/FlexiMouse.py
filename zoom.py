import cv2
import numpy as np
import pyautogui

# Constants for hand detection
HAND_AREA_THRESHOLD = 10000

# Capture webcam feed
cap = cv2.VideoCapture(0)

# Set up mouse control parameters
screen_width, screen_height = pyautogui.size()
mouse_speed = 10

# Function to perform zoom-in action
def perform_zoom_in():
    pyautogui.hotkey('ctrl', '+')  # You can adjust the key combination for zoom-in as needed

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a natural mirror effect
    frame = cv2.flip(frame, 1)

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges using Canny
    edges = cv2.Canny(blur, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours to find hand
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > HAND_AREA_THRESHOLD:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Calculate hand centroid
            cx = x + w // 2
            cy = y + h // 2
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

            # Perform zoom-in action if hand is in specific region
            if screen_width // 4 < cx < 3 * screen_width // 4 and screen_height // 4 < cy < 3 * screen_height // 4:
                perform_zoom_in()

    # Display the frame
    cv2.imshow('Frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import time
import numpy as np
import pyautogui # Import the pyautogui library
# Removed: from controlkeys import ...

# Optional: Add a brief pause to allow you to switch to the game window
time.sleep(2.0)

# Removed: current_key_pressed logic as pyautogui.press() handles press and release

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]

video = cv2.VideoCapture(0)

# The get_label function is not essential for key control, but kept for completeness
def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            # Process results
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score, 2))

            # Extract Coordinates
            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hand.HandLandmark.WRIST].x, hand.landmark[mp_hand.HandLandmark.WRIST].y)),
                [640, 480]).astype(int))

            output = text, coords

    return output

with mp_hand.Hands(min_detection_confidence=0.5,
                   min_tracking_confidence=0.5) as hands:
    while True:
        # Removed all key state variables (keyPressed, key_count, etc.)
        
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList = []
        text = ''
        
        if results.multi_hand_landmarks:
            # Handedness label extraction
            for idx, classification in enumerate(results.multi_handedness):
                if classification.classification[0].index == idx:
                    label = classification.classification[0].label
                    text = '{}'.format(label)
                else:
                    label = classification.classification[0].label
                    text = '{}'.format(label)
            
            # Extract landmarks and draw connections
            for hand_landmark in results.multi_hand_landmarks:
                # Note: This assumes only one hand is detected, using the first one [0]
                myHands = results.multi_hand_landmarks[0] 
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        
        fingers = []

        if len(lmList) != 0:
            # Thumb check (X-axis comparison)
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            
            # Other 4 fingers check (Y-axis comparison)
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1) # Finger is up
                else:
                    fingers.append(0) # Finger is down
            
            total = fingers.count(1)
            
            # --- Gesture to Key Mapping using pyautogui.press() ---
            
            if total == 4 and text == "Right": # Right hand, 4 fingers up (Index, Middle, Ring, Pinky)
                cv2.rectangle(image, (400, 300), (600, 425), (255, 255, 255), cv2.FILLED)
                cv2.putText(image, "LEFT", (400, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (0, 0, 255), 5)
                pyautogui.press('left') # Simulate a quick key press
                
            elif total == 5 and text == "Left": # Left hand, all 5 fingers up
                cv2.rectangle(image, (400, 300), (600, 425), (255, 255, 255), cv2.FILLED)
                cv2.putText(image, " RIGHT", (400, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (0, 255, 0), 5)
                pyautogui.press('right') # Simulate a quick key press

            elif total == 1: # Only Index finger up (assuming any hand)
                cv2.rectangle(image, (400, 300), (600, 425), (255, 255, 255), cv2.FILLED)
                cv2.putText(image, "UP", (400, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (0, 255, 0), 5)
                pyautogui.press('up') # Simulate a quick key press

            elif total == 0: # All fingers down (Fist)
                cv2.rectangle(image, (400, 300), (600, 425), (255, 255, 255), cv2.FILLED)
                cv2.putText(image, "Down", (400, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (0, 255, 0), 5)
                pyautogui.press('down') # Simulate a quick key press
                
        # Removed the entire logic block for KeyOff and current_key_pressed management
        
        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
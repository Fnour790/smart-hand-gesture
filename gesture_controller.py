import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time  # pour le delai anti-spam

# Disable pyautogui fail-safe
pyautogui.FAILSAFE = False

# Initialize mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

# Get screen size
screen_width, screen_height = pyautogui.size()
print(f"Screen size: {screen_width}x{screen_height}")

# Smoothing variables
prev_x, prev_y = 0, 0
smoothing = 5

# Click control - anti-spam
last_click_time = 0
click_cooldown = 0.6  # secondes entre chaque clic
was_clicking = False  # detecte pinch ON/OFF

print("\n=== HAND GESTURE CONTROLLER ===")
print("Move your index finger to control the mouse")
print("PINCH thumb + index finger to click")
print("Press 'q' to quit")
print("===============================\n")

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to capture frame")
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # INDEX FINGER TIP (landmark 8) -> deplace la souris
            index_tip = hand_landmarks.landmark[8]
            x = int(index_tip.x * frame_width)
            y = int(index_tip.y * frame_height)

            # Conversion coordonnees camera -> ecran
            screen_x = np.interp(x, [0, frame_width], [0, screen_width])
            screen_y = np.interp(y, [0, frame_height], [0, screen_height])

            # Lissage du mouvement
            curr_x = prev_x + (screen_x - prev_x) / smoothing
            curr_y = prev_y + (screen_y - prev_y) / smoothing

            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # THUMB TIP (landmark 4) -> detection du clic
            thumb_tip = hand_landmarks.landmark[4]
            distance = np.sqrt(
                (index_tip.x - thumb_tip.x)**2 +
                (index_tip.y - thumb_tip.y)**2
            )

            # Affiche la distance en temps reel (debug)
            cv2.putText(frame, f"Dist: {distance:.3f}", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

            # Logique clic: pinch detecte + cooldown respecte
            current_time = time.time()
            is_pinching = distance < 0.08  # seuil augmente de 0.05 a 0.08

            if is_pinching and not was_clicking:
                if current_time - last_click_time > click_cooldown:
                    pyautogui.click()
                    last_click_time = current_time
                    print(f"CLICK! distance={distance:.3f}")
                    cv2.putText(frame, "CLICK!", (x - 30, y - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

            was_clicking = is_pinching

            # Affiche le statut du pinch
            status = "PINCHING" if is_pinching else "open"
            color = (0, 255, 0) if is_pinching else (200, 200, 200)
            cv2.putText(frame, status, (10, 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # Dessine les landmarks
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Cercles sur les bouts des doigts
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
            thumb_x = int(thumb_tip.x * frame_width)
            thumb_y = int(thumb_tip.y * frame_height)
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 100, 255), -1)

            # Ligne entre pouce et index (verte si pinch, orange sinon)
            line_color = (0, 255, 0) if is_pinching else (0, 100, 255)
            cv2.line(frame, (x, y), (thumb_x, thumb_y), line_color, 2)

    # Instructions a l'ecran
    cv2.putText(frame, "Press 'q' to quit", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, "Index: move | Pinch: click", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"Cooldown: {click_cooldown}s", (10, 85),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    cv2.imshow('Hand Gesture Controller', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("\nApplication closed successfully!")
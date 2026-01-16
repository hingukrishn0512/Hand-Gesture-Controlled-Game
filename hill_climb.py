import cv2
import numpy as np
import math
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ---------------- HAND LANDMARKER ----------------
base_options = python.BaseOptions(
    model_asset_path="media\hand_landmarker.task"
)

hand_options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

hand_detector = vision.HandLandmarker.create_from_options(hand_options)

# ---------------- GAME VARIABLES ----------------
WIDTH, HEIGHT = 900, 500
car_x = 100
car_y = 380
speed = 0
ground_y = 420

# ---------------- HELPER FUNCTIONS ----------------
def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)
# 👉 Calculates distance between:
# wrist
# fingertip
# Used to check:
# finger open or closed? 
def get_gesture(hand):
    wrist = hand[0]
    tips = [hand[8], hand[12], hand[16], hand[20]]

    open_fingers = sum(dist(tip, wrist) > 0.22 for tip in tips)

    if open_fingers >= 4:
        return "ACCELERATE"
    elif open_fingers == 0:
        return "BRAKE"
    elif open_fingers == 2:
        return "NORMAL"
    else:
        return "STOP"

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = hand_detector.detect(mp_image)
    gesture = "STOP"

    if result.hand_landmarks:
        hand = result.hand_landmarks[0]
        gesture = get_gesture(hand)

        h, w, _ = frame.shape
        for lm in hand:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

    # ---------------- GAME LOGIC ----------------
    if gesture == "ACCELERATE":
        speed += 0.4
    elif gesture == "BRAKE":
        speed -= 0.6
    elif gesture == "NORMAL":
        speed += 0.1
    else:
        speed = 0

    speed = max(0, min(speed, 12))
    car_x += speed

    if car_x > WIDTH:
        car_x = 0

    # ---------------- DRAW GAME ----------------
    game = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    cv2.line(game, (0, ground_y), (WIDTH, ground_y), (255, 255, 255), 3)
    cv2.rectangle(game, (int(car_x), car_y),
                  (int(car_x + 50), car_y + 30),
                  (0, 0, 255), -1)

    cv2.putText(game, f"Gesture: {gesture}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(game, f"Speed: {speed:.1f}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Hill Climb Game", game)
    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

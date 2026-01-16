import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ---------------- HAND LANDMARKER ----------------
base_options = python.BaseOptions(
    model_asset_path="media/hand_landmarker.task"
)

hand_options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

hand_detector = vision.HandLandmarker.create_from_options(hand_options)

# ---------------- GAME SETTINGS ----------------
height, width = 480, 640

car_x = 280
car_y = 400

ob_x = 300
ob_y = 0
speed = 5

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# ---------------- GAME LOOP ----------------
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

    # ---------- HAND CONTROL ----------
    if result.hand_landmarks:
        hand = result.hand_landmarks[0]

        index_tip = hand[8]   # Index finger tip
        thumb_tip = hand[4]   # Thumb tip

        # Distance between fingers
        dist = abs(index_tip.y - thumb_tip.y)

        # Open hand → move
        if dist > 0.05:
            car_x = int(index_tip.x * width)

    # ---------- OBSTACLE ----------
    ob_y += speed
    if ob_y > height:
        ob_y = 0

    # ---------- DRAW GAME ----------
    game = np.zeros((height, width, 3), dtype=np.uint8)

    # Car
    cv2.rectangle(game,
                  (car_x - 30, car_y),
                  (car_x + 30, car_y + 20),
                  (0, 255, 0), -1)

    # Obstacle
    cv2.rectangle(game,
                  (ob_x, ob_y),
                  (ob_x + 40, ob_y + 40),
                  (0, 0, 255), -1)

    cv2.imshow("Hand Control Game", game)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

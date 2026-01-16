import cv2
import numpy as np

# while game_is_running:
#     read_input()
#     update_game_state()
#     draw_everything()

# Camera → Detection → Drawing → Movement → Game logic → Controls


# screen size 
Height = 1000
width = 800

#  car position

car_x = 50
car_y = 350
speed = 0

#  in the loop there is the screen with the help of the zeros matrix 
# and game condition if these word press then do this 
#  then draw a rectangle(a car) also the condition car_x +=speed , also 
# initialize the speed maxmimum 
while True:
    screen = np.zeros((Height , width , 3) , dtype=np.uint8)

    key = cv2.waitKey(1)

    if key ==ord('w'):
        speed +=0.2
    
    elif key == ord('s'):
        speed -=0.4
        
# In Python, you use a zero-initialized array for the screen (or framebuffer) 
# because it provides a pre-allocated memory block that serves as a placeholder
#  for pixel data, where zero typically represents black or an "off" state
    
    speed = max(0 , min(speed , 10))
    car_x += speed

    cv2.rectangle(screen, (int(car_x), car_y),
                  (int(car_x + 60), car_y + 30),
                  (0, 0, 255), -1)

    cv2.imshow("Game Logic Demo", screen)

    if key == ord('q'):
        break
        


# (0,0) --------------------> X (right)
#   |
#   |
#   |
#   v
#  Y (down)

# So:

# Increasing x → moves right

# Increasing y → moves down
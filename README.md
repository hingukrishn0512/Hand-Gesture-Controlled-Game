# 🎮 Hand Gesture Controlled Game using OpenCV & MediaPipe

This project is a real-time hand gesture controlled game built using **OpenCV** and **MediaPipe Tasks API**.  
The game uses webcam-based hand tracking to control the movement of a car using finger gestures.

---

## 🚀 Features
- Real-time hand detection using MediaPipe Hand Landmarker
- Gesture-based control (open hand to move, closed hand to stop)
- Index finger position controls horizontal movement
- Basic obstacle animation
- Clean and beginner-friendly game logic
- Uses **latest MediaPipe Tasks API** (not deprecated `mp.solutions`)

---

## 🛠️ Technologies Used
- Python
- OpenCV
- MediaPipe Tasks API
- NumPy

---

## 🎯 How It Works
- The webcam captures live video
- MediaPipe detects hand landmarks
- Distance between thumb and index finger determines movement
- Index finger X-coordinate controls the car position
- Obstacles move continuously to simulate gameplay

📈 Learning Outcomes

Practical use of computer vision
Understanding real-time hand tracking
Mapping gestures to game mechanics
Working with MediaPipe Tasks API
Building interactive Python projects

🔮 Future Improvements

Collision detection and game over logic
Score counter
Speed control using gestures
Two-hand control (accelerator + brake)

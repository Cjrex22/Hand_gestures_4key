# Gesture Keyboard Controller
This is a robust Computer Vision program built in Python that allows users to control all four directional arrow keys (Up, Down, Left, and Right) using specific real-time hand gestures. This system is designed to provide a comprehensive, non-contact input method for PC applications and games requiring four-way directional control. It leverages OpenCV and MediaPipe for accurate, real-time hand tracking.

⚙️ Core Technology Stack
Language: Python (Tested with 3.8.3, but generally compatible with Python 3)

Computer Vision: OpenCV (cv2)

Hand Tracking: Google MediaPipe (Used for highly accurate hand landmark detection)

✨ Key Functionality
Four-Way Gesture Mapping: Implements distinct gesture-to-key mappings for Up (↑), Down (↓), Left (←), and Right (→) arrow keys.

Real-time Control: Provides reliable, low-latency control for games and applications that accept standard keyboard arrow inputs.

Hand Tracking: Continuously tracks hand position and gestures via the webcam input.
Usage:

Up-1 finger

Down-0 fingers/closed wrist

Left- only left palm open

Right- only right palm open

Upcoming feature: 360 degree cursor movement using eye tracking - useful to play games like Call of Duty, GTA etc.

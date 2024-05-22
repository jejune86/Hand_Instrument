import mediapipe as mp

FINGER_INDICES = {'thumb': 3, 'index': 7, 'middle': 11, 'ring': 15, 'pinky': 19}
 
hands = None
mp_hands = None
 
def init_mediapipe():
    global mp_hands
    global hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                          max_num_hands=2,
                          min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)

def calculate_angles(hand_landmarks):
    import numpy as np
    angles = {}
    for finger, idx in FINGER_INDICES.items():
        x1, y1 = hand_landmarks.landmark[idx].x, hand_landmarks.landmark[idx].y
        x2, y2 = hand_landmarks.landmark[idx - 1].x, hand_landmarks.landmark[idx - 1].y
        angle = np.arctan2(y2 - y1, x2 - x1)
        angles[finger] = angle
    return angles

mp_drawing = mp.solutions.drawing_utils
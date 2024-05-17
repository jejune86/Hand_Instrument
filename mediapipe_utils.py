import mediapipe as mp

def init_mediapipe():
    mp_hands = mp.solutions.hands
    return mp_hands.Hands(static_image_mode=False,
                          max_num_hands=2,
                          min_detection_confidence=0.5,
                          min_tracking_confidence=0.5), mp_hands

def calculate_angles(hand_landmarks, finger_indices):
    import numpy as np
    angles = {}
    for finger, idx in finger_indices.items():
        x1, y1 = hand_landmarks.landmark[idx].x, hand_landmarks.landmark[idx].y
        x2, y2 = hand_landmarks.landmark[idx - 1].x, hand_landmarks.landmark[idx - 1].y
        angle = np.arctan2(y2 - y1, x2 - x1)
        angles[finger] = angle
    return angles

mp_drawing = mp.solutions.drawing_utils
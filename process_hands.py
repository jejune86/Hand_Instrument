import mediapipe_utils as mp_u

def process_hands(image, results, sound_manager):
    angles = {}
    if results.multi_hand_landmarks:
        for hand_landmarks, hand_label in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_u.mp_drawing.draw_landmarks(image, hand_landmarks, mp_u.mp_hands.HAND_CONNECTIONS)
            
            
            
            x_coords = [landmark.x for landmark in hand_landmarks.landmark]
            center_x = sum(x_coords) / len(x_coords)
            hand_label = 'left' if center_x < 0.5 else 'right'

            angles = mp_u.calculate_angles(hand_landmarks)
            sound_manager.play_sounds(angles, hand_label)
        sound_manager.right_fist_to_change()
        sound_manager.left_fist_for_metronome()
    return angles, image

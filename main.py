import cv2
import numpy as np
import mediapipe_utils
import pygame_utils

def get_next_instrument(current_instrument):
    return 'piano' if current_instrument == 'drum' else 'drum'

def main():
    hands, mp_hands = mediapipe_utils.init_mediapipe()
    left_sounds, right_sounds = pygame_utils.init_pygame_sounds()
    
    cap = cv2.VideoCapture(0)
    
    finger_indices = {'thumb': 3, 'index': 7, 'middle': 11, 'ring': 15, 'pinky': 19}
    sound_played = { 'left': {k: False for k in finger_indices.keys()}, 'right': {k: False for k in finger_indices.keys()} }
    threshold_angles = { 'thumb': 1.6, 'index': 1.0, 'middle': 1.0, 'ring': 0.9, 'pinky': 1.0 }
    
    current_instrument = 'piano'
    instrument_changed = False

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.putText(image, current_instrument, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mediapipe_utils.mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                x_coords = [landmark.x for landmark in hand_landmarks.landmark]
                center_x = sum(x_coords) / len(x_coords)

                if center_x < 0.5:
                    hand_label = 'left'
                    sounds = left_sounds[current_instrument]
                else:
                    hand_label = 'right'
                    sounds = right_sounds[current_instrument]

                angles = mediapipe_utils.calculate_angles(hand_landmarks, finger_indices)
                pygame_utils.play_sounds(sounds, angles, threshold_angles, sound_played, hand_label)

            if all(sound_played['left'].values()) and all(sound_played['right'].values()) and not instrument_changed:
                current_instrument = 'piano' if current_instrument == 'drum' else 'drum'
                instrument_changed = True

            if not any(sound_played['left'].values()) and not any(sound_played['right'].values()):
                instrument_changed = False

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

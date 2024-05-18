import cv2
import numpy as np
import mediapipe_utils
import pygame_utils


def main():
    hands, mp_hands = mediapipe_utils.init_mediapipe()
    left_sounds, right_sounds = pygame_utils.init_pygame_sounds()
    
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FPS, 60)    
    finger_indices = {'thumb': 3, 'index': 7, 'middle': 11, 'ring': 15, 'pinky': 19}
    sound_played = { 'left': {k: False for k in finger_indices.keys()}, 'right': {k: False for k in finger_indices.keys()} }
    threshold_angles = { 'thumb': 1.6, 'index': 1.0, 'middle': 1.0, 'ring': 0.9, 'pinky': 1.0 }
    
    current_instrument = 'piano'
    instrument_changed = False

    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
        
        image_height, image_width = image.shape[:2]
        aspect_ratio = image_width / image_height
        new_width = 1280
        new_height = int(new_width / aspect_ratio)
        if new_height > 720:
            new_height = 720
            new_width = int(new_height * aspect_ratio)
            
        image = cv2.resize(image, (new_width, new_height))    

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
                print(angles['thumb'])
            if all(sound_played['right'].values()) and not instrument_changed:
                current_instrument = pygame_utils.get_next_instrument(current_instrument)
                instrument_changed = True

            if not any(sound_played['right'].values()):
                instrument_changed = False

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

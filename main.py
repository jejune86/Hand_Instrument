import cv2
import numpy as np
import mediapipe_utils
import sound

def draw_text(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.6, color=(255, 255, 255), thickness=1.3):
    cv2.putText(image, text, position, font, font_scale, color, thickness)

def display_help_window(current_instrument):
    help_image = np.full((360, 540, 3), (168, 168, 168), dtype=np.uint8)
    draw_text(help_image, 'Hand Instrument Help', (60, 30), font_scale=1.2, color=(0, 0, 0))
    draw_text(help_image, '1. Make a fist with your right hand to change Instrument', (10, 85), color=(0, 0, 255) )
    draw_text(help_image, '            or Press \'Space\'', (10, 110), color=(0, 0, 255))
    draw_text(help_image, '2. Press \'q\' or \'ESC\' to quit', (10, 135), color=(0, 165, 255))
    draw_text(help_image, '3. It recognize Left/Right hand based on location', (10, 160), color=(0, 255, 255))
    draw_text(help_image, '4. Play sound by bending fingers', (10, 185), color=(0, 255, 0))
    draw_text(help_image, 'Press \'I\' to turn off Information', (10, 330), color=(0, 0, 0))
    return help_image

def main():
    hands, mp_hands = mediapipe_utils.init_mediapipe()
    left_sounds, right_sounds = sound.init_pygame_sounds()
    
    cap = cv2.VideoCapture(0)

    finger_indices = {'thumb': 3, 'index': 7, 'middle': 11, 'ring': 15, 'pinky': 19}
    sound_played = { 'left': {k: False for k in finger_indices.keys()}, 'right': {k: False for k in finger_indices.keys()} }
    threshold_angles = { 'thumb': 1.6, 'index': 1.0, 'middle': 1.0, 'ring': 0.9, 'pinky': 1.0 }
    
    current_instrument = 'piano'
    instrument_changed = False
    help_window_visible = False


    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
        
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        image_width = image.shape[1]
        image = cv2.flip(image, 1)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        
        cv2.putText(image, current_instrument, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

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
                sound.play_sounds(sounds, angles, threshold_angles, sound_played, hand_label)
                #print(angles['thumb'])
            if all(sound_played['right'].values()) and not instrument_changed:
                current_instrument = sound.get_next_instrument(current_instrument)
                instrument_changed = True

            if not any(sound_played['right'].values()):
                instrument_changed = False

        cv2.imshow('Hand Instrument', image)
        
        
        input_key = cv2.waitKey(1) & 0xFF
        if input_key == 27 or input_key == ord('q'): # esc or q 누를 시 종료
            break
        elif input_key == 32: # space key 누를 시 악기 전환
            current_instrument = sound.get_next_instrument(current_instrument)
            instrument_changed = True
        elif input_key == ord('i'): # i 누를 시 도움말 창 표시/숨김
            if help_window_visible:
                cv2.destroyWindow('Help')
            help_window_visible = not help_window_visible
            
        if help_window_visible:
            help_image = display_help_window(current_instrument)
            cv2.imshow('Help', help_image)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

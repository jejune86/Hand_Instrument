import cv2 as cv
import numpy as np
import mediapipe_utils
import sound
import visual


def main():
    hands, mp_hands = mediapipe_utils.init_mediapipe()
    sound.init_pygame_sounds() 
    
    cap = cv.VideoCapture(0)

    finger_indices = {'thumb': 3, 'index': 7, 'middle': 11, 'ring': 15, 'pinky': 19}
    sound_played = { 'left': {k: False for k in finger_indices.keys()}, 'right': {k: False for k in finger_indices.keys()} }
    
    
    #current_instrument = 'piano'
    instrument_changed = False
    help_window_visible = False


    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
        
        
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        
        image_width = image.shape[1]
        image = cv.flip(image, 1)
        results = hands.process(image)
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        
        
        cv.putText(image, sound.instrument, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mediapipe_utils.mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                x_coords = [landmark.x for landmark in hand_landmarks.landmark]
                center_x = sum(x_coords) / len(x_coords)

                if center_x < 0.5:
                    hand_label = 'left'
                else:
                    hand_label = 'right'

                angles = mediapipe_utils.calculate_angles(hand_landmarks, finger_indices)
                sound.play_sounds(angles, hand_label)
            sound.fist_to_change()
            
        cv.imshow('Hand Instrument', image)
        
        
        input_key = cv.waitKey(1) & 0xFF
        if input_key == 27 or input_key == ord('q'): # esc or q 누를 시 종료
            break
        elif input_key == 32: # space key 누를 시 악기 전환
            sound.change_instrument()
            instrument_changed = True
        elif input_key == ord('i'): # i 누를 시 도움말 창 표시/숨김
            if help_window_visible:
                cv.destroyWindow('Help')
            help_window_visible = not help_window_visible
            
        if help_window_visible:
            help_image = visual.display_help_window()
            cv.imshow('Help', help_image)

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()

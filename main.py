import cv2
import mediapipe_utils as mp_u
from sound import SoundManager
import visual
import key_handle

def main():
    mp_u.init_mediapipe()
    sound_manager = SoundManager()  # SoundManager 인스턴스 생성
    
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
        
        results, image = visual.process_image(image, sound_manager.instrument)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_u.mp_drawing.draw_landmarks(image, hand_landmarks, mp_u.mp_hands.HAND_CONNECTIONS)
                
                x_coords = [landmark.x for landmark in hand_landmarks.landmark]
                center_x = sum(x_coords) / len(x_coords)

                hand_label = 'left' if center_x < 0.5 else 'right'
                angles = mp_u.calculate_angles(hand_landmarks)
                sound_manager.play_sounds(angles, hand_label)
            sound_manager.right_fist_to_change()
            sound_manager.left_fist_for_metronome()
        
        cv2.imshow('Hand Instrument', image)
        
        input_key = cv2.waitKey(1) & 0xFF
        if input_key == 27 or input_key == ord('q'):  # esc or q 누를 시 종료
            break
        
        key_handle.key_handle(input_key, sound_manager)
        
        if visual.threshold_window_visible:
            threshold_image = visual.display_threshold_window(sound_manager)
            cv2.imshow('Thresholds', threshold_image)
        
        if visual.help_window_visible:
            help_image = visual.display_help_window()
            cv2.imshow('Help', help_image)

    cap.release()
    cv2.destroyAllWindows()
    sound_manager.stop_metronome()

if __name__ == "__main__":
    main()

import cv2 as cv
import mediapipe_utils as mp_u
from sound import SoundManager
import visual
import key_handle
from process_hands import process_hands

def main():
    mp_u.init_mediapipe()
    sound_manager = SoundManager()  # SoundManager for sound control
    
    cap = cv.VideoCapture(0)   # get camera input from webcam
    while cap.isOpened():
        success, image = cap.read()
        
        if not success:
            print("Error: Failed to read frame from webcam.")
            break
        
        results, image = visual.process_image(image) # process image for hands and get hand results
        
        angles, image = process_hands(image, results, sound_manager) # handle hand results and play sounds
            
        image = visual.draw_output_image(image, results, sound_manager) # create output image
        cv.imshow('Hand Instrument', image)
        
        input_key = cv.waitKey(1) & 0xFF
        if input_key == 27 or input_key == ord('q'):  # esc or q 누를 시 종료
            break
        
        key_handle.key_handle(input_key, sound_manager)
        
        visual.window_controller(sound_manager, angles)
        
    cap.release()
    cv.destroyAllWindows()
    sound_manager.stop_metronome()

if __name__ == "__main__":
    main()

import cv2 as cv
import numpy as np
import mediapipe_utils as mp_u

help_window_visible = False
threshold_window_visible = False
remote_control_visible = True
finger_info_visible = False

current_selection = 0
window_options = ["Help", "Sensitive Thresholds", "Finger Info"]

finger_info_image = {
    'Drum' : cv.imread('resource/image/drum.png'),
    'Piano' : cv.imread('resource/image/DoReMi.png'),
    'Xylophone' : cv.imread('resource/image/DoReMi.png'),
}

        
def draw_text(image, text, position, font=cv.FONT_HERSHEY_DUPLEX, font_scale=0.6, color=(255, 255, 255), thickness=1, shadow_color=(100, 100, 100), shadow_offset=(2, 2)):
    shadow_position = (position[0] + shadow_offset[0], position[1] + shadow_offset[1])
    cv.putText(image, text, shadow_position, font, font_scale, shadow_color, thickness+1, lineType=cv.LINE_AA)
    cv.putText(image, text, position, font, font_scale, color, thickness, lineType=cv.LINE_AA)


def process_image(image):
    img_ratio = image.shape[1] / image.shape[0]
    image = cv.resize(image, (960, int(960 / img_ratio)))
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image = cv.flip(image, 1)
    results = mp_u.hands.process(image)
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    
    return results, image

def draw_finger_blink(image, finger, hand_landmarks, color=(0, 255, 255)):
    index = mp_u.FINGER_INDICES[finger]
    landmark = hand_landmarks.landmark[index]
    x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
    cv.circle(image, (x, y), 10, color, cv.FILLED)
    

def draw_output_image(image, results, sound_manager):
    draw_text(image, sound_manager.instrument, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    if results.multi_hand_landmarks:
        for hand_landmarks, hand_label in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = hand_label.classification[0].label.lower()
            for finger in mp_u.FINGER_INDICES.keys():
                if sound_manager.sound_played[label][finger]:
                    draw_finger_blink(image, finger, hand_landmarks)
    if remote_control_visible:
        remote_control_image = draw_remote_control(image.shape[0])
        image = np.hstack((image, remote_control_image))
    return image

def draw_remote_control(height):
    remote_image = np.full((height, 300, 3), (0, 0, 0), dtype=np.uint8)
    y_pos = 30
    for i, option in enumerate(window_options):
        color = (0, 255, 0) if i == current_selection else (255, 255, 255)
        draw_text(remote_image, option, (10, y_pos), font_scale=0.8, color=color, shadow_color=(0, 0, 0))
        y_pos += 40
    draw_text(remote_image, 'Press Enter to toggle', (10, height-60), font_scale=0.6, color=(255, 255, 255), shadow_color=(0, 0, 0))
    draw_text(remote_image, 'Press \'Z/X\' to select', (10, height-40), font_scale=0.6, color=(255, 255, 255), shadow_color=(0, 0, 0)) 
    draw_text(remote_image, 'Press \'C\' to turn off', (10, height-20), font_scale=0.6, color=(255, 255, 255), shadow_color=(0, 0, 0))
    return remote_image



def display_finger_info(instrument):
    return finger_info_image[instrument]
    
def display_help_window():
    help_image = np.full((360, 640, 3), (184, 242, 255), dtype=np.uint8)
    draw_text(help_image, 'Hand Instrument Help', (60, 30), font_scale=1.2, color=(0, 0, 0))
    draw_text(help_image, '1. Bend your finger to play!!', (10, 85), color=(0, 0, 255) )
    draw_text(help_image, '2. Press \'Q\' or \'ESC\' to quit', (10, 110), color=(0, 165, 255))
    draw_text(help_image, '3. Make a fist with your right hand to change Instrument', (10, 135), color=(0, 255, 255))
    draw_text(help_image, '            or Press \'Space\'', (10, 160), color=(0, 255, 255))
    draw_text(help_image, '4. Make a fist with your lefts hand to start/stop Metronome', (10, 185), color=(0, 255, 0))
    draw_text(help_image, '            or Press \'M\'', (10, 210), color=(0, 255, 0))
    draw_text(help_image, '5. Press \'[\' or \']\' to adjust Metronome interval', (10, 235), color=(255, 0, 0))
    draw_text(help_image, '6. Press \'C\' to turn on window controller', (10, 260), color=(130, 0, 75))
    draw_text(help_image, '7. It recognize Left/Right hand based on location', (10, 285), color=(238, 130, 238))
    draw_text(help_image, 'Press \'I\' to turn off Information', (10, 345), color=(0, 0, 0))
    return help_image

def display_threshold_window(sound_manager, angles):
    threshold_image = np.full((330, 310, 3), (255, 255, 255), dtype=np.uint8)
    thresholds = sound_manager.get_thresholds()
    draw_text(threshold_image, 'Adjust Thresholds', (40, 30), font_scale=0.8, color=(0, 0, 0))
    y_pos = 70
    for finger, value in thresholds.items():
        color = (0, 0, 255) if finger == sound_manager.selected_finger else (0, 0, 0)
        draw_text(threshold_image, f'{finger}: {value:.2f}', (10, y_pos), color=color)
        y_pos += 40
    draw_text(threshold_image, 'Use 1-5 to select finger', (10, 280), color=(0, 0, 0))
    draw_text(threshold_image, 'Use +/- Key to adjust', (10, 310), color=(0, 0, 0))
    
    y_pos = 70
    for finger, angle in angles.items():
        draw_text(threshold_image, f'{angle:.2f}', (150, y_pos),  color=(0, 0, 0), )
        y_pos += 40
        
    return threshold_image


def window_controller(sound_manager, angles):
    if help_window_visible:
        help_image = display_help_window()
        cv.imshow('Help', help_image)
    if threshold_window_visible:
        threshold_image = display_threshold_window(sound_manager, angles)
        cv.imshow('Sensitive Thresholds', threshold_image)
    if finger_info_visible:
        finger_info_image = display_finger_info(sound_manager.instrument)
        cv.imshow('Finger Info', finger_info_image)
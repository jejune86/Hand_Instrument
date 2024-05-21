import cv2 as cv
import numpy as np
import mediapipe_utils as mp_u

help_window_visible = False
threshold_window_visible = False

def draw_finger_blink(image, landmarks, finger_indices, color=(0, 255, 255)):
    for finger, index in finger_indices.items():
        landmark = landmarks[index]
        x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
        cv.circle(image, (x, y), 10, color, cv.FILLED)
        
def draw_text(image, text, position, font=cv.FONT_HERSHEY_DUPLEX, font_scale=0.6, color=(255, 255, 255), thickness=1):
    cv.putText(image, text, position, font, font_scale, color, thickness)

def display_help_window():
    help_image = np.full((360, 540, 3), (168, 168, 168), dtype=np.uint8)
    draw_text(help_image, 'Hand Instrument Help', (60, 30), font_scale=1.2, color=(0, 0, 0))
    draw_text(help_image, '1. Make a fist with your right hand to change Instrument', (10, 85), color=(0, 0, 255) )
    draw_text(help_image, '            or Press \'Space\'', (10, 110), color=(0, 0, 255))
    draw_text(help_image, '2. Press \'q\' or \'ESC\' to quit', (10, 135), color=(0, 165, 255))
    draw_text(help_image, '3. It recognize Left/Right hand based on location', (10, 160), color=(0, 255, 255))
    draw_text(help_image, '4. Play sound by bending fingers', (10, 185), color=(0, 255, 0))
    draw_text(help_image, 'Press \'I\' to turn off Information', (10, 345), color=(0, 0, 0))
    return help_image

def display_threshold_window(sound_manager):
    threshold_image = np.full((300, 330, 3), (255, 255, 255), dtype=np.uint8)
    thresholds = sound_manager.get_thresholds()
    draw_text(threshold_image, 'Adjust Thresholds', (30, 30), font_scale=0.8, color=(0, 0, 0))
    y_pos = 70
    for finger, value in thresholds.items():
        color = (0, 0, 255) if finger == sound_manager.selected_finger else (0, 0, 0)
        draw_text(threshold_image, f'{finger}: {value:.2f}', (10, y_pos), color=color)
        y_pos += 40
    draw_text(threshold_image, 'Use 1-5 to select finger', (10, 280), color=(0, 0, 0))
    draw_text(threshold_image, 'Use LEFT RIGHT Key to adjust', (10, 310), color=(0, 0, 0))
    return threshold_image

def process_image(image, instrument):
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image = cv.flip(image, 1)
    results = mp_u.hands.process(image)
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    cv.putText(image, instrument, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return results, image

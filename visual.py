import cv2 as cv
import numpy as np
import mediapipe_utils as mp_u

help_window_visible = True
threshold_window_visible = False

def draw_finger_blink(image, landmarks, finger_indices, color=(0, 255, 255)):
    for finger, index in finger_indices.items():
        landmark = landmarks[index]
        x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
        cv.circle(image, (x, y), 10, color, cv.FILLED)
        
def draw_text(image, text, position, font=cv.FONT_HERSHEY_DUPLEX, font_scale=0.6, color=(255, 255, 255), thickness=1, shadow_color=(100, 100, 100), shadow_offset=(2, 2)):
    shadow_position = (position[0] + shadow_offset[0], position[1] + shadow_offset[1])
    cv.putText(image, text, shadow_position, font, font_scale, shadow_color, thickness+1, lineType=cv.LINE_AA)
    cv.putText(image, text, position, font, font_scale, color, thickness, lineType=cv.LINE_AA)

def display_help_window():
    help_image = np.full((360, 640, 3), (184, 242, 255), dtype=np.uint8)
    draw_text(help_image, 'Hand Instrument Help', (60, 30), font_scale=1.2, color=(0, 0, 0))
    draw_text(help_image, '1. Bend your finger to play!!', (10, 85), color=(0, 0, 255) )
    draw_text(help_image, '2. Press \'Q\' or \'ESC\' to quit', (10, 110), color=(0, 165, 255))
    draw_text(help_image, '3. Make a fist with your right hand to change Instrument', (10, 135), color=(0, 255, 255))
    draw_text(help_image, '            or Press \'Space\'', (10, 160), color=(0, 255, 255))
    draw_text(help_image, '4. Press \'T\' to adjust sensitive thresholds', (10, 185), color=(0, 255, 0))
    draw_text(help_image, '5. It recognize Left/Right hand based on location', (10, 210), color=(255, 0, 0))
    draw_text(help_image, '6. Make a fist with your lefts hand to start/stop Metronome', (10, 235), color=(130, 0, 75))
    draw_text(help_image, '            or Press \'M\'', (10, 260), color=(238, 130, 238))
    draw_text(help_image, '7. Press \'[\' or \']\' to adjust Metronome interval', (10, 285), color=(238, 130, 238))
    draw_text(help_image, 'Press \'I\' to turn off Information', (10, 345), color=(0, 0, 0))
    return help_image

def display_threshold_window(sound_manager):
    threshold_image = np.full((330, 310, 3), (255, 255, 255), dtype=np.uint8)
    thresholds = sound_manager.get_thresholds()
    draw_text(threshold_image, 'Adjust Thresholds', (40, 30), font_scale=0.8, color=(0, 0, 0))
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
    draw_text(image, instrument, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return results, image

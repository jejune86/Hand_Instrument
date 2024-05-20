import cv2

def draw_finger_blink(image, landmarks, finger_indices, color=(0, 255, 255)):
    for finger, index in finger_indices.items():
        landmark = landmarks[index]
        x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
        cv2.circle(image, (x, y), 10, color, cv2.FILLED)
        
def draw_text(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.6, color=(255, 255, 255), thickness=1):
    cv2.putText(image, text, position, font, font_scale, color, thickness)

def display_help_window():
    help_image = np.full((360, 540, 3), (168, 168, 168), dtype=np.uint8)
    draw_text(help_image, 'Hand Instrument Help', (60, 30), font_scale=1.2, color=(0, 0, 0))
    draw_text(help_image, '1. Make a fist with your right hand to change Instrument', (10, 85), color=(0, 0, 255) )
    draw_text(help_image, '            or Press \'Space\'', (10, 110), color=(0, 0, 255))
    draw_text(help_image, '2. Press \'q\' or \'ESC\' to quit', (10, 135), color=(0, 165, 255))
    draw_text(help_image, '3. It recognize Left/Right hand based on location', (10, 160), color=(0, 255, 255))
    draw_text(help_image, '4. Play sound by bending fingers', (10, 185), color=(0, 255, 0))
    draw_text(help_image, 'Press \'I\' to turn off Information', (10, 330), color=(0, 0, 0))
    return help_image

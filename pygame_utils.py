import pygame

def init_pygame_sounds():
    pygame.mixer.init()
    left_sounds = {
        'drum': {
            'thumb': pygame.mixer.Sound('resource/sound/drum/RD_C_HH_1.wav'),
            'index': pygame.mixer.Sound('resource/sound/drum/RD_S_1.wav'),
            'middle': pygame.mixer.Sound('resource/sound/drum/RD_C_C_1.wav'),
            'ring': pygame.mixer.Sound('resource/sound/drum/RD_K_1.wav'),
            'pinky': pygame.mixer.Sound('resource/sound/drum/RD_T_MT_1.wav')
        },
        'piano': {
            'thumb': pygame.mixer.Sound('resource/sound/piano/F4.mp3'),
            'index': pygame.mixer.Sound('resource/sound/piano/E4.mp3'),
            'middle': pygame.mixer.Sound('resource/sound/piano/D#4.mp3'),
            'ring': pygame.mixer.Sound('resource/sound/piano/D4.mp3'),
            'pinky': pygame.mixer.Sound('resource/sound/piano/C4.mp3')
        }
    }
    right_sounds = {
        'drum': {
            'thumb': pygame.mixer.Sound('resource/sound/drum/RD_C_HH_1.wav'),
            'index': pygame.mixer.Sound('resource/sound/drum/RD_S_1.wav'),
            'middle': pygame.mixer.Sound('resource/sound/drum/RD_C_C_1.wav'),
            'ring': pygame.mixer.Sound('resource/sound/drum/RD_K_1.wav'),
            'pinky': pygame.mixer.Sound('resource/sound/drum/RD_T_MT_1.wav')
        },
        'piano': {
            'thumb': pygame.mixer.Sound('resource/sound/piano/G4.mp3'),
            'index': pygame.mixer.Sound('resource/sound/piano/G#4.mp3'),
            'middle': pygame.mixer.Sound('resource/sound/piano/A4.mp3'),
            'ring': pygame.mixer.Sound('resource/sound/piano/B4.mp3'),
            'pinky': pygame.mixer.Sound('resource/sound/piano/C5.mp3')
        }
    }
    return left_sounds, right_sounds

def play_sounds(sounds, angles, thresholds, sound_played, hand_label):
    for finger, angle in angles.items():
        if (finger == 'thumb' and angle > thresholds[finger] and not sound_played[hand_label][finger]) or \
           (finger != 'thumb' and angle < thresholds[finger] and not sound_played[hand_label][finger]):
            sounds[finger].play()
            sound_played[hand_label][finger] = True

        if (finger == 'thumb' and angle <= thresholds[finger]) or \
           (finger != 'thumb' and angle >= thresholds[finger]):
            sound_played[hand_label][finger] = False

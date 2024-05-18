import pygame

def init_pygame_sounds():
    pygame.mixer.init()
    left_sounds = {
        'drum': {
            'thumb': pygame.mixer.Sound('resource/sound/drum/CrashCymbal.wav'),
            'index': pygame.mixer.Sound('resource/sound/drum/Kick.wav'),
            'middle': pygame.mixer.Sound('resource/sound/drum/Snare.wav'),
            'ring': pygame.mixer.Sound('resource/sound/drum/Hi-hat.wav'),
            'pinky': pygame.mixer.Sound('resource/sound/drum/MediumTom.wav')
        },
        'piano': {
            'thumb': pygame.mixer.Sound('resource/sound/piano/G4.mp3'),
            'index': pygame.mixer.Sound('resource/sound/piano/F4.mp3'),
            'middle': pygame.mixer.Sound('resource/sound/piano/E4.mp3'),
            'ring': pygame.mixer.Sound('resource/sound/piano/D4.mp3'),
            'pinky': pygame.mixer.Sound('resource/sound/piano/C4.mp3')
        },
        'xylophone': {
            'thumb': pygame.mixer.Sound('resource/sound/xylophone/G.wav'),
            'index': pygame.mixer.Sound('resource/sound/xylophone/F.wav'),
            'middle': pygame.mixer.Sound('resource/sound/xylophone/E.mp3'),
            'ring': pygame.mixer.Sound('resource/sound/xylophone/D.mp3'),
            'pinky': pygame.mixer.Sound('resource/sound/xylophone/C.mp3')
        }
    }
    right_sounds = {
        'drum': {
            'thumb': pygame.mixer.Sound('resource/sound/drum/CrashCymbal.wav'),
            'index': pygame.mixer.Sound('resource/sound/drum/Kick.wav'),
            'middle': pygame.mixer.Sound('resource/sound/drum/Snare.wav'),
            'ring': pygame.mixer.Sound('resource/sound/drum/Hi-hat.wav'),
            'pinky': pygame.mixer.Sound('resource/sound/drum/MediumTom.wav')
        },
        'piano': {
            'thumb': pygame.mixer.Sound('resource/sound/piano/A4.mp3'),
            'index': pygame.mixer.Sound('resource/sound/piano/B4.mp3'),
            'middle': pygame.mixer.Sound('resource/sound/piano/C5.mp3'),
            'ring': pygame.mixer.Sound('resource/sound/piano/D5.mp3'),
            'pinky': pygame.mixer.Sound('resource/sound/piano/E5.mp3')
        },
        'xylophone': {
            'thumb': pygame.mixer.Sound('resource/sound/xylophone/A.wav'),
            'index': pygame.mixer.Sound('resource/sound/xylophone/B.mp3'),
            'middle': pygame.mixer.Sound('resource/sound/xylophone/C+.wav'),
            'ring': pygame.mixer.Sound('resource/sound/xylophone/D+.wav'),
            'pinky': pygame.mixer.Sound('resource/sound/xylophone/E+.wav')
        }
    }
    return left_sounds, right_sounds

def get_next_instrument(current_instrument):
    instruments = ['piano', 'drum', 'xylophone']
    next_index = (instruments.index(current_instrument) + 1) % len(instruments)
    return instruments[next_index]


def play_sounds(sounds, angles, thresholds, sound_played, hand_label):
    for finger, angle in angles.items():
        if finger == 'thumb' :
            if hand_label == 'left':
                if angle < thresholds[finger] and not sound_played[hand_label][finger]:
                    sounds[finger].play()
                    sound_played[hand_label][finger] = True
                if angle >= thresholds[finger]:
                    sound_played[hand_label][finger] = False
            else: # right thumb
                if angle > thresholds[finger] and not sound_played[hand_label][finger]:
                    sounds[finger].play()
                    sound_played[hand_label][finger] = True
                if angle <= thresholds[finger]:
                    sound_played[hand_label][finger] = False
        
        else : # other fingers
            if angle < thresholds[finger] and not sound_played[hand_label][finger]:
                sounds[finger].play()
                sound_played[hand_label][finger] = True

            if angle >= thresholds[finger]:
                sound_played[hand_label][finger] = False

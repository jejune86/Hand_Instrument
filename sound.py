import pygame
import visual

finger_indices = {'thumb': 3, 'index': 7, 'middle': 11, 'ring': 15, 'pinky': 19}
sound_played = { 'left': {k: False for k in finger_indices.keys()}, 'right': {k: False for k in finger_indices.keys()} }
instrument_changed = False

thresholds = { 'thumb': 1.6, 'index': 1.0, 'middle': 1.0, 'ring': 0.9, 'pinky': 1.0 }

sounds = {}
instrument = 'piano'

def init_pygame_sounds():
    pygame.mixer.init()
    
    global left_sounds, right_sounds, sounds
    sounds = {
        'left' : {
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
        },
        'right' : {
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
    }

def fist_to_change() : 
    global instrument_changed
    if all(sound_played['right'].values()) and not instrument_changed:
                change_instrument()
                instrument_changed = True
    if not any(sound_played['right'].values()):
        instrument_changed = False

def change_instrument():
    global instrument
    instruments = ['piano', 'drum', 'xylophone']
    next_index = (instruments.index(instrument) + 1) % len(instruments)
    instrument = instruments[next_index]


def play_sounds(angles, hand_label):
    global sounds, instrument, sound_played
    
    for finger, angle in angles.items():
        if finger == 'thumb' :
            if hand_label == 'left':
                if angle < thresholds[finger] and not sound_played[hand_label][finger]:
                    sounds[hand_label][instrument][finger].play()
                    sound_played[hand_label][finger] = True
                if angle >= thresholds[finger]:
                    sound_played[hand_label][finger] = False
            else: # right thumb
                if angle > thresholds[finger] and not sound_played[hand_label][finger]:
                    sounds[hand_label][instrument][finger].play()
                    sound_played[hand_label][finger] = True
                if angle <= thresholds[finger]:
                    sound_played[hand_label][finger] = False
        
        else : # other fingers
            if angle < thresholds[finger] and not sound_played[hand_label][finger]:
                sounds[hand_label][instrument][finger].play()
                sound_played[hand_label][finger] = True
                #visual.draw_finger_blink(image, hand_landmarks, {finger: finger_indices[finger]})

            if angle >= thresholds[finger]:
                sound_played[hand_label][finger] = False
                

import pygame

# 손가락 인덱스와 초기 임계값 설정
FINGER_INDICES = {'thumb': 3, 'index': 7, 'middle': 11, 'ring': 15, 'pinky': 19}
INITIAL_THRESHOLDS = {'thumb': 1.6, 'index': 1.0, 'middle': 1.0, 'ring': 0.9, 'pinky': 1.0}

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.sound_played = {'left': {k: False for k in FINGER_INDICES.keys()}, 'right': {k: False for k in FINGER_INDICES.keys()}}
        self.instrument = 'Piano'
        self.instrument_changed = False
        self.selected_finger = 'thumb'
        self.thresholds = INITIAL_THRESHOLDS.copy()
        pygame.mixer.init()
        self.init_sounds()

    def init_sounds(self):
        self.sounds = {
            'left': {
                'Drum': {
                    'thumb': pygame.mixer.Sound('resource/sound/drum/Kick.wav'),
                    'index': pygame.mixer.Sound('resource/sound/drum/FloorTom.wav'),
                    'middle': pygame.mixer.Sound('resource/sound/drum/HighTom.wav'),
                    'ring': pygame.mixer.Sound('resource/sound/drum/MediumTom.wav'),
                    'pinky': pygame.mixer.Sound('resource/sound/drum/Clap.wav')
                },
                'Piano': {
                    'thumb': pygame.mixer.Sound('resource/sound/piano/G4.mp3'),
                    'index': pygame.mixer.Sound('resource/sound/piano/F4.mp3'),
                    'middle': pygame.mixer.Sound('resource/sound/piano/E4.mp3'),
                    'ring': pygame.mixer.Sound('resource/sound/piano/D4.mp3'),
                    'pinky': pygame.mixer.Sound('resource/sound/piano/C4.mp3')
                },
                'Xylophone': {
                    'thumb': pygame.mixer.Sound('resource/sound/xylophone/G.wav'),
                    'index': pygame.mixer.Sound('resource/sound/xylophone/F.wav'),
                    'middle': pygame.mixer.Sound('resource/sound/xylophone/E.mp3'),
                    'ring': pygame.mixer.Sound('resource/sound/xylophone/D.mp3'),
                    'pinky': pygame.mixer.Sound('resource/sound/xylophone/C.mp3')
                }
            },
            'right': {
                'Drum': {
                    'thumb': pygame.mixer.Sound('resource/sound/drum/CrashCymbal.wav'),
                    'index': pygame.mixer.Sound('resource/sound/drum/RideCymbal.wav'),
                    'middle': pygame.mixer.Sound('resource/sound/drum/Snare.wav'),
                    'ring': pygame.mixer.Sound('resource/sound/drum/Hi-hat.wav'),
                    'pinky': pygame.mixer.Sound('resource/sound/drum/StickHits.wav')
                },
                'Piano': {
                    'thumb': pygame.mixer.Sound('resource/sound/piano/A4.mp3'),
                    'index': pygame.mixer.Sound('resource/sound/piano/B4.mp3'),
                    'middle': pygame.mixer.Sound('resource/sound/piano/C5.mp3'),
                    'ring': pygame.mixer.Sound('resource/sound/piano/D5.mp3'),
                    'pinky': pygame.mixer.Sound('resource/sound/piano/E5.mp3')
                },
                'Xylophone': {
                    'thumb': pygame.mixer.Sound('resource/sound/xylophone/A.wav'),
                    'index': pygame.mixer.Sound('resource/sound/xylophone/B.mp3'),
                    'middle': pygame.mixer.Sound('resource/sound/xylophone/C+.wav'),
                    'ring': pygame.mixer.Sound('resource/sound/xylophone/D+.wav'),
                    'pinky': pygame.mixer.Sound('resource/sound/xylophone/E+.wav')
                }
            }
        }

    def fist_to_change(self):
        if all(self.sound_played['right'].values()) and not self.instrument_changed:
            self.change_instrument()
            self.instrument_changed = True
        if not any(self.sound_played['right'].values()):
            self.instrument_changed = False

    def change_instrument(self):
        instruments = ['Piano', 'Drum', 'Xylophone']
        next_index = (instruments.index(self.instrument) + 1) % len(instruments)
        self.instrument = instruments[next_index]

    def play_sounds(self, angles, hand_label):
        for finger, angle in angles.items():
            if finger == 'thumb':
                if hand_label == 'left':
                    if angle < self.thresholds[finger] and not self.sound_played[hand_label][finger]:
                        self.sounds[hand_label][self.instrument][finger].play()
                        self.sound_played[hand_label][finger] = True
                    if angle >= self.thresholds[finger]:
                        self.sound_played[hand_label][finger] = False
                else:  # right thumb
                    if angle > self.thresholds[finger] and not self.sound_played[hand_label][finger]:
                        self.sounds[hand_label][self.instrument][finger].play()
                        self.sound_played[hand_label][finger] = True
                    if angle <= self.thresholds[finger]:
                        self.sound_played[hand_label][finger] = False
            else:  # other fingers
                if angle < self.thresholds[finger] and not self.sound_played[hand_label][finger]:
                    self.sounds[hand_label][self.instrument][finger].play()
                    self.sound_played[hand_label][finger] = True
                if angle >= self.thresholds[finger]:
                    self.sound_played[hand_label][finger] = False

    def adjust_thresholds(self, adjustment):
        self.thresholds[self.selected_finger] += adjustment
        if self.thresholds[self.selected_finger] < 0:  # 임계값이 음수가 되지 않도록
            self.thresholds[self.selected_finger] = 0

    def get_thresholds(self):
        return self.thresholds

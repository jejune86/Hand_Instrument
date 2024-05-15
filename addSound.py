import cv2
import mediapipe as mp
import numpy as np
import pygame

# MediaPipe 손 인식기 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 웹캠에서 영상 캡처 시작
cap = cv2.VideoCapture(0)

# Pygame 믹서 초기화 및 소리 로드
pygame.mixer.init()
sounds = {
    'drum':{
            'thumb': pygame.mixer.Sound('resource/sound/RD_C_C_1.wav'),
            'index': pygame.mixer.Sound('resource/sound/RD_S_1.wav'),
            'middle': pygame.mixer.Sound('resource/sound/RD_K_1.wav'),
            'ring': pygame.mixer.Sound('resource/sound/RD_C_HH_1.wav'),
            'pinky': pygame.mixer.Sound('resource/sound/RD_T_MT_1.wav')
    },
    'piano':{
            'thumb': pygame.mixer.Sound('resource/sound/RD_C_C_1.wav'),
            'index': pygame.mixer.Sound('resource/sound/RD_S_1.wav'),
            'middle': pygame.mixer.Sound('resource/sound/RD_K_1.wav'),
            'ring': pygame.mixer.Sound('resource/sound/RD_C_HH_1.wav'),
            'pinky': pygame.mixer.Sound('resource/sound/RD_T_MT_1.wav')
    },
}

prev_landmarks = None
prev_angles = [None] * 21  # 각 마디의 이전 각도 저장

sound_played = {
    'thumb': False,
    'index': False,
    'middle': False,
    'ring': False,
    'pinky': False
}

threshold_angles = {
    'thumb': 1.6,  # 엄지의 임계 각도
    'index': 1.2,  # 검지의 임계 각도
    'middle': 1.2,  # 중지의 임계 각도
    'ring': 0.9,  # 약지의 임계 각도
    'pinky': 1.2   # 소지의 임계 각도
}


while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    cv2.putText(image, 'DRUM', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    

 
    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            current_angles = [None] * 21
            if idx == 0 :
                for finger in ['thumb', 'index', 'middle', 'ring', 'pinky']:
                    idx = {'thumb': 3, 'index': 7, 'middle': 11, 'ring': 15, 'pinky': 19}[finger]
                    x1, y1 = hand_landmarks.landmark[idx].x, hand_landmarks.landmark[idx].y
                    x2, y2 = hand_landmarks.landmark[idx - 1].x, hand_landmarks.landmark[idx - 1].y
                    current_angle = np.arctan2(y2 - y1, x2 - x1)
                    current_angles[idx] = current_angle        
                              
                    print(f"index, {current_angles[3]}")              
                    if finger == 'thumb':
                        # 엄지는 각도가 임계값보다 높아질 때 소리 재생
                        if prev_angles[idx] is not None and current_angle > threshold_angles[finger] and not sound_played[finger]:
                            sounds['drum'][finger].play()
                            sound_played[finger] = True
                            
                    else:
                        # 다른 손가락은 각도가 임계값보다 낮아질 때 소리 재생
                        if prev_angles[idx] is not None and current_angle < threshold_angles[finger] and not sound_played[finger]:
                            sounds['drum'][finger].play()
                            sound_played[finger] = True
                            
                    # 각도가 다시 임계값을 넘으면 상태 초기화
                    if finger == 'thumb':
                        if current_angle <= threshold_angles[finger]:
                            sound_played[finger] = False
                    else:
                        if current_angle >= threshold_angles[finger]:
                            sound_played[finger] = False
                
                            
                prev_landmarks = [hand_landmarks.landmark[i] for i in range(21)]
                prev_angles = current_angles
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()



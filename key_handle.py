import cv2 as cv
import sound 
import visual
import cv2 as cv

def key_handle(input_key, sound_manager):
    if input_key == 32:  # space key 누를 시 악기 전환
        sound_manager.change_instrument()
    elif input_key == ord('i'):  # i 누를 시 도움말 창 표시/숨김
        if visual.help_window_visible:
            cv.destroyWindow('Help')
        visual.help_window_visible = not visual.help_window_visible
    elif input_key == ord('t'):  # t 누를 시 임계값 창 표시/숨김
        if visual.threshold_window_visible:
            cv.destroyWindow('Thresholds')
        visual.threshold_window_visible = not visual.threshold_window_visible
    elif input_key == ord('1'):
        sound_manager.selected_finger = 'thumb'
    elif input_key == ord('2'):
        sound_manager.selected_finger = 'index'
    elif input_key == ord('3'):
        sound_manager.selected_finger = 'middle'
    elif input_key == ord('4'):
        sound_manager.selected_finger = 'ring'
    elif input_key == ord('5'):
        sound_manager.selected_finger = 'pinky'
    elif input_key == ord('='):  # + 키 누를 시 임계값 증가
        sound_manager.adjust_thresholds(0.1)
    elif input_key == ord('-'):  # - 키 누를 시 임계값 감소
        sound_manager.adjust_thresholds(-0.1)

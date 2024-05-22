import cv2 as cv
import visual

def key_handle(input_key, sound_manager):
    if input_key == 32:  # space key 누를 시 악기 전환
        sound_manager.change_instrument()
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
        sound_manager.adjust_thresholds(0.05)
    elif input_key == ord('-'):  # - 키 누를 시 임계값 감소
        sound_manager.adjust_thresholds(-0.05)
    elif input_key == ord('m'): 
        if not sound_manager.metronome_running:
            sound_manager.start_metronome()
        else:
            sound_manager.stop_metronome()
    elif input_key == ord('['):  # [ 키 누를 시 메트로놈 간격 감소
        sound_manager.adjust_metronome_interval(-0.1)
    elif input_key == ord(']'):  # ] 키 누를 시 메트로놈 간격 증가
        sound_manager.adjust_metronome_interval(0.1)
    elif input_key == ord('c') :
        if visual.remote_control_visible:
            cv.destroyWindow('Remote Control')
        visual.remote_control_visible = not visual.remote_control_visible   
    elif input_key == 13 and visual.remote_control_visible:  # Enter 키 누를 시 선택한 윈도우 표시/숨김
        selected_option = visual.window_options[visual.current_selection]
        if selected_option == "Help":
            if visual.help_window_visible:
                cv.destroyWindow('Help')
            visual.help_window_visible = not visual.help_window_visible
        elif selected_option == "Thresholds":
            if visual.threshold_window_visible:
                cv.destroyWindow('Thresholds')
            visual.threshold_window_visible = not visual.threshold_window_visible
        elif selected_option == "Finger Info":
            if visual.finger_info_visible:
                cv.destroyWindow('Finger Info')
            visual.finger_info_visible = not visual.finger_info_visible
    elif input_key == ord('z'):  
        visual.current_selection = (visual.current_selection - 1) % len(visual.window_options)
    elif input_key == ord('x'):  
        visual.current_selection = (visual.current_selection + 1) % len(visual.window_options)
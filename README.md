# Hand Instrument Project

This project uses computer vision to create a virtual instrument that can be played using hand gestures detected by a webcam. You can play Piano, Drum and Xylophone

<img src="resource/image/play.gif">

## Features

- **Hand Tracking**: Uses Mediapipe to detect and track hands in real-time.
- **Instrument Sounds**: Plays different instrument sounds (Piano, Drum, Xylophone) using finger
- **Sensitivity Threshold Adjustment**: Allows users to adjust the sensitivity of finger
- **Metronome**: Includes a metronome feature with adjustable intervals.
- **Help**: Provides a help window explaining how to use 
- **Finger Info**: Shows sound of each fingers
- **Control Box**: Allows users to control different windows (Help, sensitivity Thresholds, Finger Info) using a remote control box.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/hand-instrument.git
    cd hand-instrument
    ```

2. **Install required packages**:
    ```sh
    pip install -r requirements.txt
    ```
    
    The `requirements.txt` file should contain the following dependencies:
    ```plaintext
    mediapipe
    pygame
    opencv-python
    numpy
    ```

## Usage

1. **Run the main script**:
    ```sh
    python main.py
    ```

2. **Controls**:
    1. KeyBoard
    - `i`: Toggle the help window.
    - `Space`: Change the instrument.
    - `q` or `ESC`: Quit the application.
    - `1` to `5`: Select thumb, index, middle, ring, or pinky finger respectively for threshold adjustment.
    - `=` and `-`: Increase or decrease the threshold for the selected finger.
    - `m`: Start/Stop the metronome.
    - `[` and `]`: Decrease or increase the metronome interval.
    - `c`: Toggle window control box.
    - `z` and `x`: Navigate through the control box options.
    - `Enter`: Toggle the selected window in the control box.
    <br>
    1. Hand
    - `Bend your finger` to play sound
    - `Make fist with Right hand` to change instrument
    - `Make fist with Left hand` to start Metronome

(You can check this on Help window too)

## Window Information

   1. **Main**
    <img src="resource/image/main_window.png">
   - Points of hand appears on the screen
   - Yellow is displayed on the fingers that make a sound.
   - On the right side of screen, you can control other window

   2. **Help**
    <img src="resource/image/help.png">
    <br>
   3. **Sensitivity Thresholds**
    <img src="resource/image/sensitivity_threshold.png" width=300>
    - On the right side, it shows finger's current angle value
    - It makes sound, when the angle value is lower than threshold

   4. Finger Info
    <img src="resource/image/finger_info.png">
    - It shows fingers current sound

## Program Usage Video
   1. **Piano** 
   
   [![Watch the video](https://img.youtube.com/vi/13rA8FfwtO4/0.jpg)](https://youtu.be/13rA8FfwtO4)
    <br>
   2. **Xylophone** 

   [![Watch the video](https://img.youtube.com/vi/0ibOeEEJzJs/0.jpg)](https://youtu.be/0ibOeEEJzJs)
    <br>
   3. **Drum** 

   [![Watch the video](https://img.youtube.com/vi/iskAuhqkUgg/0.jpg)](https://youtu.be/iskAuhqkUgg)
    <br>
   4. **Change Instrument and Metronome** 

   [![Watch the video](https://img.youtube.com/vi/0K80JKxfJ8Q/0.jpg)](https://youtu.be/0K80JKxfJ8Q)
    

## License

This project is licensed under the MIT License. See the LICENSE file for details.


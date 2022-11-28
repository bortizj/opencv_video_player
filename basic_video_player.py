"""
Copyleft 2022
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

author: Benhur Ortiz-Jaramillo
"""

from datetime import datetime
from tkinter import filedialog
from pathlib import Path
from time import sleep
import numpy as np
import cv2
import sys


# Reading settings, now it is just folder for screenshots
with open(Path(__file__).parent.joinpath("settings")) as file:
    OUT_FOLDER = Path(file.readline().rstrip())
    SAMPLING = file.readline().rstrip()
    if SAMPLING in ("1", "2", "3", "4", "5"):
        SAMPLING = int(SAMPLING)
    else:
        SAMPLING = 1


# Valid keys for controls
LIST_VALID_KEYS = [
    ord("a"), ord("d"), ord("w"), ord("s"),
    ord("A"), ord("D"), ord("W"), ord("S"),
    ord("p"), ord("f"), ord("r"), ord("q"),
    ord("P"), ord("F"), ord("R"), ord("Q"),
]
# Control labels for the control panel
CONTROLS = {
    "A/a": "Prev. frame",
    "D/d": "Next frame",
    "W/w": "Speed up [max 30 fps]",
    "S/s": "Speed down [min 1 fps]",
    "P/p": "Play / Pause",
    "F/f": "Store the current frame",
    "R/r": "Reset the player",
    "Q/q": "Close the player",
}
# You want low frame rates for researching
MIN_FPS, MAX_FPS = 1, 30


class SimpleVideoReader:
    """
    Convenient class for reading frames from a video stream
    """

    def __init__(self, device_name=0):
        # Next time that frame is read the right index is set
        self.frame_id = -1
        self.cap = cv2.VideoCapture(device_name)
        self.n_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if self.cap.isOpened():
            print("Bitstream opened")
        else:
            print("Cannot open bitstream")
            exit()

    def __del__(self):
        self.cap.release()
        print("Bitstream closed")

    def read_frame(self):
        ret, self.frame = self.cap.read()
        if ret:
            self.frame_id += 1

    def go_to_frame(self, frame_id=0):
        if frame_id < 0:
            # For negative ids means back a number of frames
            frame_id = np.clip(self.frame_id + frame_id, 0, self.n_frames)

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        self.frame_id = frame_id - 1  # Next time that frame is read the right index is set


class BasicPlayer:
    """
    Convenient class to play any video file frame by frame or at very slow frame rate
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.vr = SimpleVideoReader(device_name=str(file_path))
        self.frame_rate = 10
        self.is_playing = False
        self.name_window = file_path.name
        cv2.namedWindow(self.name_window, cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow(self.name_window, 0, 0)
        cv2.imshow(
            self.name_window, 
            np.zeros((self.vr.height, self.vr.width), dtype="uint8")[::SAMPLING, ::SAMPLING]
            )
        cv2.createTrackbar('Frame id', self.name_window, 0, self.vr.n_frames - 1, self.frame_id_changed)

        # Reading the first frame
        self.vr.read_frame()

        # Building the window control
        name_window = "Controls"
        cv2.namedWindow(name_window)
        cv2.moveWindow(name_window, 0, 0)
        self.build_controls_window()

    def __del__(self):
        cv2.destroyAllWindows()
        print("Player closed")

    def frame_id_changed(self, event):
        # For convenience, this is handled by other functions
        pass

    def build_controls_window(self):
        # Shows the controls in a different window for reference
        name_window = "Controls"

        controls_img = np.zeros((384, 512), dtype=np.uint8)
        for index, (key, value) in enumerate(CONTROLS.items()):
            cv2.putText(
                controls_img, f"{key}: {value}", (20, 40 + index * 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255)
            )

        cv2.putText(
                controls_img, f"fps: {self.frame_rate}", (20, 40 + (index + 1) * 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255)
            )
        cv2.imshow(name_window, controls_img)

    def key_pressed(self, key_pressed):
        # Returns true except for next, previous or restart keys
        flag = True
        if self.is_playing:
            if key_pressed == ord("p") or key_pressed == ord("P"):
                # Pause
                self.is_playing = False
            elif key_pressed == ord("w") or key_pressed == ord("W"):
                # Speed up frame rate
                self.frame_rate = np.clip(self.frame_rate + 1, MIN_FPS, MAX_FPS)
                self.build_controls_window()
            elif key_pressed == ord("s") or key_pressed == ord("S"):
                # Speed down frame rate
                self.frame_rate = np.clip(self.frame_rate - 1, MIN_FPS, MAX_FPS)
                self.build_controls_window()
        else:
            if key_pressed == ord("a") or key_pressed == ord("A"):
                # Previous frame
                self.vr.go_to_frame(-1)
                self.vr.read_frame()
                flag = False
            elif key_pressed == ord("d") or key_pressed == ord("D"):
                # Next frame
                self.vr.read_frame()
                flag = False
            elif key_pressed == ord("w") or key_pressed == ord("W"):
                # Speed up frame rate
                self.frame_rate = np.clip(self.frame_rate + 1, MIN_FPS, MAX_FPS)
                self.build_controls_window()
            elif key_pressed == ord("s") or key_pressed == ord("S"):
                # Speed down frame rate
                self.frame_rate = np.clip(self.frame_rate - 1, MIN_FPS, MAX_FPS)
                self.build_controls_window()
            elif key_pressed == ord("p") or key_pressed == ord("P"):
                # Play
                self.is_playing = True
            elif key_pressed == ord("f") or key_pressed == ord("F"):
                # Store frame
                frame = self.vr.frame.copy()
                cv2.imwrite(
                    str(OUT_FOLDER.joinpath(datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png")), 
                    frame
                    )
            elif key_pressed == ord("r") or key_pressed == ord("R"):
                # Restart to initial frame
                self.vr.go_to_frame(0)
                self.vr.read_frame()
                flag = False

        return flag

    def update_screen(self, flag):
        if self.is_playing:
            # Keep reading frames while playing
            self.vr.read_frame()
        else:
            # Check if user did not change the frames using next, previous or restart keys
            # flag is false when user pressed next, previous or restart keys
            if flag:
                frame_id = cv2.getTrackbarPos('Frame id', self.name_window)
                # If there is a change between the trackbar and the frame id, it was because user change
                # Difference is not zero if the user changed the trackbar
                if self.vr.frame_id - frame_id != 0:
                    self.vr.go_to_frame(frame_id)
                    self.vr.read_frame()

        cv2.imshow(self.name_window, self.vr.frame[::SAMPLING, ::SAMPLING])
        cv2.setTrackbarPos('Frame id', self.name_window, self.vr.frame_id)

    def run_player(self):
        # Runs the main loop of the video player
        print("Player opened")
        wait_time = 5
        # Shows the first image before the loop
        flag = True
        self.update_screen(flag)
        while True:
            # Main loop changes the frame rate and reads key presses
            key_pressed = cv2.waitKey(wait_time)
            if key_pressed in LIST_VALID_KEYS:
                # If key is q/Q then exit
                if key_pressed == ord("q") or key_pressed == ord("Q"):
                    break

                # Other keys are checked in the key pressed function
                flag = self.key_pressed(key_pressed)

            # Waits the frame rate before going to the next loop
            try:
                self.update_screen(flag)
            except:
                break
            flag = True
            sleep((1 / self.frame_rate) - (wait_time / 1000.0))


if __name__ == "__main__":
    # Getting the list of arguments if any
    # pyinstaller basic_video_player.py --add-data settings;.
    path_source = None
    list_args = sys.argv
    print(*list_args, sep="\n")
    if len(list_args) > 1:
        path_source = Path(list_args[1])

    if path_source is None:
        path_source = Path(
            filedialog.askopenfilename(title="Select video", filetypes=[("Video", ".mp4 .avi")])
            )
        if path_source.suffix not in (".mp4", ".avi"):
            exit()

    bs = BasicPlayer(path_source)
    bs.run_player()

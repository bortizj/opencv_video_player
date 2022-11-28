# Video player using opencv
Basic video player for research purposes able to display frame by frame or at very low frame rates.
# Controls
- *left / a*: previous frame
- *right / d*: next frame
- *up / w*: speed up [max 30 fps]
- *down / s*: speed down [min 1 fps]
- *space*: Play / Pause
- *f*: stores the current frame
- *r*: resets the player to the first frame
- *q*: closes the player
# Usage
Right click on the video file and select the executable as player. 
Use the command line as 'basic_video_player.exe vid_file.mp4'
Open the application and select the video file from a folder
# Settings file
There is a settings file along with the executable where you can set the path for storing the 
screenshots taken with the software. The first line of the settings file is the path to the 
folder to store the images and the second line is the sampling factor in case that the image 
does not fit your screen (int 1, 2, 3, 4 or 5). By default is 1 and the executable path.
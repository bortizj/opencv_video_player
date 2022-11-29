# Video player using opencv
Nice research video player for frame by frame analysis with screenshot saving functionality.
- Trackbar for frame selection
- Next and previous frame selection
- Screenshot of current frame
- Playing functionality with variable frame rate 1 to 30 fps
- Screenshot stores the actual video frame using opencv
- Easy to use with the executable allowing Windows open with feature (`Right click -> open with -> basic_video_player.exe`)
- Or use the convenient file-chooser
- ... of course it also works with command line `basic_video_player.exe vid_file.mp4`

# Controls
- *a*: previous frame
- *d*: next frame
- *w*: speed up [max 30 fps]
- *s*: speed down [min 1 fps]
- *p*: Play / Pause
- *f*: stores the current frame
- *r*: resets the player to the first frame
- *q*: closes the player
# Usage
Right click on the video file and select the executable as player. 
Use the command line as `basic_video_player.exe vid_file.mp4`
Open the application and select the video file from a folder
# Settings file
There is a settings file along with the executable where you can set the path for storing the 
screenshots taken with the software. The first line of the settings file is the path to the 
folder to store the images and the second line is the sampling factor in case that the image 
does not fit your screen (`int` 1, 2, 3, 4 or 5). By default is 1 and the executable path.
# Synch.Live: Aesthetics Flask application

Lightweight webserver for data collection. Grabs participant data, then displays
videos in a random order, for the participant to rate them.

The videos are obtained by cutting off the first seconds and the last, based on
the parameters used, then trimmed in 10s blocks. For each 10s block, we extract
trajectories with the same [Kalman filter based tracker](https://github.com/Synch-Live/Synch.Live1.0/blob/main/python/camera/tools/trajectories.py) as Synch.Live, then use the [`pyflocks`
library](https://github.com/mearlboro/flocks) to plot into simple animations.

See the bottom section of this readme, for more details on how these videos
were produced.

## Setup
To run the application you need Python 3.8+ and Flask. You can install it in an
IDE or do on each machine that will be running the application.

```
pip install flask
```

Clone the repository,
```
git clone git@github.com:Synch-Live/AestheticsFlask.git
```
run the application
```
python3 server.py
```
then go to a browser at `localhost:5000` and follow the steps.

## Experimental videos and data
The videos are in `web/static/videos`. The list of videos, with associated mean
realtime filtered Psi, is in `web/static/videos.csv`.

## Data collection
The data collected from participants is in `web/static/data`. For each participant
`PID`, participant data is in a file `p_{PID}.csv`, while each video rating, side
by side to the video's name/ID and Psi, is in a file `v_{PID}.csv`.

The participant's responses can be recovered from the `web/static/data` folder,
each participant has 2 CSV files.

Since the files are indexed by the participant ID, the data from multiple computers
can be merged easily without overlap as long as the participant IDs are **unique**.

| :exclamation: This is a local application. The data is saved on the computer the application is being run on. There is no cloud storage or server. Make sure you copy the relevant files and store them securely.
|-----------------------------------------|


## Media

The folder `media` contains relevant files for generating the videos and CSV
file used in this platform.

### Psi data
The folder `media/0-psi` contains CSV files with the Psi emergence calculation
for each frame. The script `to-10s-mean.py` reads the files and generates a
new file with means for each 10 second segment corresponding to a video.

### Animating the experimental videos
The folder `media/1-txt` contains the text trajectories files, as exported from
the experimental videos, on which the animation videos used in this repository are
based. The videos have been animated using the [`pyflocks` library](https://github.com/mearlboro/flocks) and `ffmpeg`.

For details on how the trajectory files are obtained, see the [`DataAnalysis2022` repository](https://github.com/Synch-Live/DataAnalysis2022).

The script `media/anim.py` makes use of the experimental data in `media/group_data.csv`
to produce the relevant `pyflock` commands to animate the trajectories.
The script produces 10 second videos of gameplay with simple white dots on a
black background.

The script outputs the relevant commands to a shell script file, `to-anim.sh`.

The result should be individual subdirectories in `2-img` with the names of the
form `B_1-7`, where `B_1` indicates the day and the group, and `-7` indicates
it is the 7th 10-second block in the video. These subdirectories include PNG
images numbered by the frame number.

`ffmpeg` can be used to combine the images in each folder into 12 fps videos.
The script `mp4.sh` contains the `ffmpeg` commands to animate the videos.

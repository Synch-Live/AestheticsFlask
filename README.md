### Synch.Live Aesthetics Flask application

Lightweight webserver for data collection. Grabs participant data, then displays
videos in a random order, for the participant to rate them.

The videos are obtained by cutting off the first seconds and the last, based on
the parameters used, then trimmed in 10s blocks. For each 10s block, we extract
trajectories with the same [Kalman filter based tracker](https://github.com/Synch-Live/Synch.Live1.0/blob/main/python/camera/tools/trajectories.py) as Synch.Live, then use a [flocking
library]() to plot into simple animations.

The videos are in `web/static/videos`. The list of videos, with associated mean
realtime filtered Psi, is in `web/static/videos.csv`.

The data collected from participants is in `web/static/data`. For each participant
`PID`, Participant data is in a file `p_{PID}.csv`, while each video rating, side
by side to the video's name/ID and Psi, is in a file `v_{PID}.csv`.

To run the application you need Python 3.8+ and Flask. You can install it in an
IDE or do

```
pip install flask
```

# Synch.Live
## Aesthetics Flask application

Lightweight webserver for data collection. Grabs participant data, then displays
videos in a random order, for the participant to rate them.

The videos are obtained by cutting off the first seconds and the last, based on
the parameters used, then trimmed in 10s blocks. For each 10s block, we extract
trajectories with the same [Kalman filter based tracker](https://github.com/Synch-Live/Synch.Live1.0/blob/main/python/camera/tools/trajectories.py) as Synch.Live, then use a [flocking
library]() to plot into simple animations.


### Setup
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

### Data collection
The data collected from participants is in `web/static/data`. For each participant
`PID`, participant data is in a file `p_{PID}.csv`, while each video rating, side
by side to the video's name/ID and Psi, is in a file `v_{PID}.csv`.

The participant's responses can be recovered from the `web/static/data` folder,
each participant has 2 CSV files.

Since the files are indexed by the participant ID, the data from multiple computers
can be merged easily without overlap as long as the participant IDs are **unique**.

| :exclamation: This is a local application. The data is saved on the computer the application is being run on. There is no cloud storage or server. Make sure you copy the relevant files and store them securely.
|-----------------------------------------|

### Media
The videos are in `web/static/videos`. The list of videos, with associated mean
realtime filtered Psi, is in `web/static/videos.csv`.



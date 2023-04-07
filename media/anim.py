import os
import csv
import pandas as pd
import subprocess

FRAMERATE = 12
START_THRESHOLD = FRAMERATE * 15
BLOCK_LEN_SEC = 10
BLOCK_LEN_FRAMES = FRAMERATE * BLOCK_LEN_SEC

groups = pd.read_csv('groups_data.csv')
groups = groups[groups.Notes != 'Pointwise MI'][groups.Notes != 'ERROR']

with open('to-anim.sh', 'a') as comm:

    for g in groups.Group:
        if os.path.exists(f"1-txt/{g}"):
            start  = int(groups[groups.Group==g]['Filter buffer (frames)'] / 3 * 2 + START_THRESHOLD)
            gameplay_length = int(groups[groups.Group==g]['Duration (frames)'])
            length = gameplay_length - start + 1
            blocks, rem = divmod(length, BLOCK_LEN_FRAMES)
            if rem <= 20:
                blocks -= 1

            path = f"1-txt/{g}"
            command = f"python -m pyflocks.util.animate --path {path} --style DOT -s 0 -e 1; sleep 2\n"
            comm.write(command)
            for b in range(blocks):
                s = b * BLOCK_LEN_FRAMES
                e = (b+1) * BLOCK_LEN_FRAMES
                command = f"python -m pyflocks.util.animate --path {path} --out 2-img --style DOT -s {s} -e {e} --simple; sleep 2\n"
                comm.write(command)
            comm.write("\n")


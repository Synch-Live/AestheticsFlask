import os
import csv
import pandas as pd
import numpy as np

FRAMERATE = 12
START_THRESHOLD = FRAMERATE * 15
BLOCK_LEN_SEC = 10
BLOCK_LEN_FRAMES = FRAMERATE * BLOCK_LEN_SEC

groups = pd.read_csv('groups_data.csv')
groups = groups[groups.Notes != 'Pointwise MI'][groups.Notes != 'ERROR']

with open('videos.csv', 'w') as csvf:

    for g in groups.Group:
        if os.path.exists(f"0-psi/{g}-psi.csv"):

            start  = int(groups[groups.Group==g]['Filter buffer (frames)'] / 3 * 2 + START_THRESHOLD)
            gameplay_length = int(groups[groups.Group==g]['Duration (frames)'])
            length = gameplay_length - start + 1
            blocks, rem = divmod(length, BLOCK_LEN_FRAMES)
            if rem <= 20:
                blocks -= 1

            psis = pd.read_csv(f"0-psi/{g}-psi.csv", sep=',')
            psis = psis[psis['type']=='Filtered']

            for b in range(blocks):
                s = start + b * BLOCK_LEN_FRAMES
                e = s + BLOCK_LEN_FRAMES
                block_psi = psis['psi'][s: e]
                mean_block_psi = np.mean(block_psi)

                csvf.write(f"{g}-{b + 1},{mean_block_psi}\n")
            print(f"{b+1} blocks for group {g}")

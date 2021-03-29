#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

import gb
from utils import build_replay, get_score
import asyncio
import time
import sys
import os

def main():
    f = []
    if not gb.cfg.replay_path.exists():
        raise RuntimeError(f'Directory \'{gb.cfg.replay_path}\' is invalid!')

    for (_, _, filenames) in os.walk(gb.cfg.replay_path):
        f.extend(filenames)
        break

    loop = asyncio.get_event_loop()

    for file in f:
        sid = file[:len(file) - 4]

        score = loop.run_until_complete(get_score(sid))

        if score is None:
            continue

        build_replay(score)

    loop.close()

    print("Done!")

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

from cmyui import AsyncSQLPool
import struct
import hashlib
from writer import write_uleb128, write_string
from objects.score import Score
from typing import Optional
import gb
import os

DATETIME_OFFSET = 0x89F7FF5F7B58000
db = AsyncSQLPool()

def build_replay(s: Score) -> Optional[None]:
    # get the md5 hash of replay
    replay_md5 = hashlib.md5(
        '{}p{}o{}o{}t{}a{}r{}e{}y{}o{}u{}{}{}'.format(
            s.n100 + s.n300,
            s.n50, s.ngeki,
            s.nkatu, s.nmiss,
            s.map_md5, s.max_combo,
            str(s.perfect == 1),
            s.player_name, s.score, 0, # Lfie graph?
            s.mods, 'True'
        ).encode()
    ).hexdigest()

    # bufffer for replay output
    buff = bytearray()

    # pack first headers
    buff += struct.pack('<Bi', s.mode, gb.cfg.osu_ver)
    buff += write_string(s.map_md5)
    buff += write_string(s.player_name)
    buff += write_string(replay_md5)
    buff += struct.pack(
        '<hhhhhhihBi',
        s.n300, s.n100, s.n50,
        s.ngeki, s.nkatu, s.nmiss,
        s.score, s.max_combo, s.perfect,
        s.mods
    )
    buff += b'\x00' # Life graph?

    timestamp = int(s.play_time.timestamp() * 1e7)
    buff += struct.pack('<q', timestamp + DATETIME_OFFSET)

    raw_replay = get_raw_replay(s.id)

    if raw_replay is None:
        return print(f'Skipping...')

    # pack the raw replay data into the buffer
    try:
        buff += struct.pack('<i', len(raw_replay))
    except:
        return print(f'Bad replay, skip. ({s.id})')

    buff += raw_replay

    # pack additional info info buffer.
    buff += struct.pack('<q', s.id)

    save_replay(bytes(buff), s.id)

def get_raw_replay(sid: int) -> Optional[bytes]:
    replay = gb.cfg.replay_path / f'{sid}.osr'

    if not replay.exists():
        return print(f'There are no .osr for replay: {sid}')

    r = replay.read_bytes()

    # Try to unpack osuver to check if replay is broken
    try:
       struct.unpack('<i', r[1:5])
       return print(f'Replay {sid} isn\'t broken.')
    except:
        pass

    return bytes(r)

def save_replay(replay: bytes, sid: int) -> Optional[None]:
    # Save a temp file for a while due the checks
    tempfile = gb.cfg.replay_path / f'temp-{sid}.osr'

    try:
        tempfile.write_bytes(replay)
    except Exception as e:
        print(f'Error while saving replay {sid}\n{e}')

    # Now we can delete temp file & original file safely
    file = gb.cfg.replay_path / f'{sid}.osr'

    if file.exists():
        os.remove(file)

    file.write_bytes(tempfile.read_bytes())

async def get_score(sid: int) -> Optional[Score]:
    await db.connect(gb.cfg.mysql)

    # Bruh... 🤠
    if (score := await db.fetch('SELECT scores_vn.*, users.name FROM scores_vn LEFT JOIN users ON scores_vn.userid = users.id WHERE scores_vn.id = %s',
    [sid], _dict=False)) is not None:
        score = Score.from_sql(score)
    elif (score := await db.fetch('SELECT scores_rx.*, users.name FROM scores_rx LEFT JOIN users ON scores_rx.userid = users.id WHERE scores_rx.id = %s',
    [sid], _dict=False)) is not None:
        score = Score.from_sql(score)
    elif (score := await db.fetch('SELECT scores_ap.*, users.name FROM scores_ap LEFT JOIN users ON scores_ap.userid = users.id WHERE scores_ap.id = %s',
    [sid], _dict=False)) is not None:
        score = Score.from_sql(score)
    else:
        await db.close()
        return print("Error when trying to get score from database: " + sid)

    await db.close()
    return score
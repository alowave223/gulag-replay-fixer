from pathlib import Path

# Path to .osr files
replay_path = Path('/root/coding/test')

# Mysql configuration
mysql = {
    'db': 'osu',
    'host': 'localhost',
    'password': 'password',
    'user': 'root'
}

# Osu version with which replays will be saved
osu_ver: int = 20200207
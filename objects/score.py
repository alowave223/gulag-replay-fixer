from datetime import datetime
from typing import Optional

__all__ = 'Score',

class Score:

    __slots__ = (
        'id', 'map_md5', 'mods', 'score',
        'n300', 'n100', 'n50', 'nmiss', 'ngeki',
        'nkatu', 'mode', 'perfect', 'max_combo',
        'play_time', 'player_name'
    )

    def __init__(self):
        self.id: Optional[int] = None

        self.map_md5: Optional[str] = None
        self.score: Optional[int] = None
        self.mods: Optional[int] = None

        self.n300: Optional[int] = None
        self.n100: Optional[int] = None
        self.n50: Optional[int] = None
        self.nmiss: Optional[int] = None
        self.ngeki: Optional[int] = None
        self.nkatu: Optional[int] = None

        self.mode: Optional[int] = None
        self.max_combo: Optional[int] = None
        self.perfect: Optional[int] = None

        self.player_name: [str] = None
        self.play_time: [datetime] = None

    @classmethod
    def from_sql(cls, score):

        ret = cls()

        ret.id = score[0]
        ret.map_md5 = score[1]
        ret.score = score[2]

        ret.max_combo = score[5]
        ret.mods = score[6]

        ret.mode = score[15]
        ret.play_time = score[16]
        ret.perfect = score[20]
        ret.player_name = score[21]

        (ret.n300, ret.n100, ret.n50,
        ret.nmiss, ret.ngeki, ret.nkatu) = score[7:13]

        return ret

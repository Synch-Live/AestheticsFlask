from enum import Enum
from typing import List, Optional
import csv
import os
import random

class EnumStr(Enum):
    @classmethod
    def from_str(e, s: str):
        return e[s.upper()]

    def __str__(e):
        names = e.name.split('_')
        name = names[0].capitalize()
        if len(names) > 1:
            name += " " + " ".join(n.lower() for n in names[1:])
        return name

    @classmethod
    def names(e) -> List[str]:
        return list(e.__members__.keys())

    @classmethod
    def members(e) -> List['EnumStr']:
        return list(e.__members__.values())


class Gender(EnumStr):
    NONE = 0
    MALE = 1
    FEMALE = 2
    NON_BINARY = 3

    def prt(e):
        if e.name == 'NONE':
            return "Prefer not to say"
        else:
            return super().__str__()

class Ethnicity(EnumStr):
    OTHER = 0
    WHITE = 1
    ASIAN = 2
    BLACK = 3
    MIXED = 4

    def prt(e):
        if e.name == 'ASIAN':
            return "Asian or British Asian"
        elif e.name == 'BLACK':
            return "Black, Black British, Carribean, or African"
        else:
            return super().__str__()



class Video():
    def __init__(self, fname: str, psi: float) -> None:
        if not fname.endswith('.mp4'):
            fname = f"{fname}.mp4"

        self.fname  = os.path.join(os.path.join("static", "videos"), fname)
        self.vid    = fname.split('.')[0]
        self.psi    = psi
        self.rating = 5 # set to the midde of scale, to avoid skewed stats

    @classmethod
    def random(self, vids: List['Video'], seen: List['Video'] = []) -> Optional['Video']:
        v = None
        if len(seen) < len(vids):
            i = random.randint(0, len(vids) - 1)
            while vids[i].vid in set([ v.vid for v in seen ]):
                i = random.randint(0, len(vids) - 1)
            v = vids[i]
        return v

    def rate(self, rating: int) -> None:
        assert(type(rating) is int and 0 < rating <= 10)
        self.rating = rating


class Library():
    @staticmethod
    def all() -> List['Video']:
        videos = []
        path = os.path.abspath(os.path.join('static', 'videos.csv'))
        with open(path, 'r') as csvf:
            csvr = csv.reader(csvf, delimiter = ',')
            for row in csvr:
                # A01_07.mp4, -2.3849239
                videos.append(Video(row[0], float(row[1])))
        return videos


class Participant():
    def __init__(self,
        pid: str = '', age: int = -1,
        gender: 'Gender' = Gender.NONE, ethnicity: 'Ethnicity' = Ethnicity.OTHER
    ) -> None:
        self.pid = pid
        self.age = age
        self.gender = gender
        self.ethnicity = ethnicity
        self.videos : List['Video'] = []

    def update(self,
        pid: str, age: int, gender: 'Gender', ethnicity: 'Ethnicity'
    ) -> None:
        self.pid = pid
        self.age = age
        self.gender = gender
        self.ethnicity = ethnicity

    def rate(self, v: 'Video', rating: int) -> None:
        v.rate(rating)
        self.videos.append(v)

    def save(self) -> None:
        path = os.path.abspath(os.path.join('static', 'data'))

        with open(os.path.join(path, f"p_{self.pid}.csv"), 'w') as fh:
            fh.write(f"ID,{self.pid}\n")
            fh.write(f"Age,{self.age}\n")
            fh.write(f"Gender,{self.gender}\n")
            fh.write(f"Ethnicity,{self.ethnicity}\n")
            fh.flush()

        with open(os.path.join(path, f"v_{self.pid}.csv"), 'w') as fh:
            for v in self.videos:
                fh.write(f"{v.vid},{v.psi},{v.rating}\n")
            fh.flush()


from dataclasses import dataclass
from datetime import datetime, time

tz_datetime = datetime


@dataclass(frozen=True)
class TimeDelta:
    hr: int
    min: int


@dataclass(frozen=True)
class MilitaryTime:
    def __init__(self, time):
        hr, min = divmod(time, 100)
        assert 0 <= min < 60
        assert 0 <= hr < 24

        object.__setattr__(self, 'hr', hr)
        object.__setattr__(self, 'min', min)

    @classmethod
    def from_hr_min(cls, hr: int, min: int):
        return cls(hr*100 + min)

    @classmethod
    def from_string(cls, military_time_string):
        return cls(int(military_time_string))

    @classmethod
    def extract_from_datetime(cls, dt: datetime):
        return cls.from_hr_min(dt.hour, dt.minute)

    @property
    def time(self):
        return self.hr * 100 + self.min

    def to_time(self, tzinfo) -> time:
        return time(hour=self.hr, minute=self.min, tzinfo=tzinfo)

    def __str__(self):
        return f'{self.hr:02}{self.min:02}'

    def __add__(self, other: TimeDelta):
        min = (self.min + other.min) % 60
        additional_hrs = (self.min + other.min) // 60
        hr = (self.hr + other.hr + additional_hrs) % 24
        return MilitaryTime.from_hr_min(hr, min)

    def __sub__(self, other: TimeDelta):
        min = (self.min - other.min) % 60
        additional_hrs = (self.min - other.min) // 60
        hr = (self.hr - other.hr + additional_hrs) % 24
        return MilitaryTime.from_hr_min(hr, min)

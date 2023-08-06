import calendar
from datetime import datetime
from enum import Enum
from functools import total_ordering


@total_ordering
class WeekDay(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @classmethod
    def extract_from_datetime(cls, dt: datetime):
        return cls[calendar.day_name[dt.weekday()].upper()]

    @classmethod
    def from_string(cls, weekday: str):
        return cls[weekday.upper()]

    def __str__(self):
        return str(self.name)

    def __lt__(self, other):
        return self.value < other.value


import calendar
from datetime import datetime
from enum import Enum


class WeekDay(Enum):
    MONDAY = 'MONDAY'
    TUESDAY = 'TUESDAY'
    WEDNESDAY = 'WEDNESDAY'
    THURSDAY = 'THURSDAY'
    FRIDAY = 'FRIDAY'
    SATURDAY = 'SATURDAY'
    SUNDAY = 'SUNDAY'

    @classmethod
    def extract_from_datetime(cls, dt: datetime):
        return cls[calendar.day_name[dt.weekday()].upper()]

    @classmethod
    def from_string(cls, weekday: str):
        return cls[weekday.upper()]
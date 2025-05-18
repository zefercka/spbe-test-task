from enum import StrEnum


class IntervalEnum(StrEnum):
    """
    Enum for standardized time intervals.
    """
    ONE_MINUTE = "1m"
    TWO_MINUTES = "2m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"
    FIVE_DAYS = "5d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"
    THREE_MONTHS = "3mo"
    
    @classmethod
    def from_str(cls, value: str) -> "IntervalEnum":
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"Invalid interval: {value}")
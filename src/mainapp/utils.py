from datetime import date, datetime, timedelta


def is_rest_day(dt: datetime) -> bool:
    """
    Function for checking if datetime is a rest day
    param dt: datetime
    return: bool
    """
    holidays_set = {
        *(date(2025, 1, d) for d in range(1, 9)),
        date(2025, 5, 1),
        date(2025, 5, 2),
        date(2025, 5, 8),
        date(2025, 5, 9),
    }
    return dt.weekday() >= 5 or dt.date() in holidays_set


def next_day(dt: datetime) -> datetime:
    """
    Function for getting the next day of the week if it's not weekend. \n
    param dt: datetime \n
    return: datetime
    """
    dt += timedelta(days=1)
    while is_rest_day(dt):
        dt += timedelta(days=1)
    return dt

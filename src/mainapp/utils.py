from datetime import datetime, timedelta, time


def make_time(v: float) -> time:
    v_formatted = f'{v:.2f}'
    h, m = map(int, v_formatted.split('.'))
    if 0 <= h <= 23:
        return time(h, m * 60 // 100)


def make_float(v: timedelta) -> float:
    return v.seconds / 3600


def next_day(dt: datetime) -> datetime:
    new_dt = dt + timedelta(days=1)
    if new_dt.weekday() < 5:
        return new_dt
    return next_day(new_dt)

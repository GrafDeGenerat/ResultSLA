from datetime import date, datetime, time, timedelta


def make_time(v: int | float) -> time:
    """
    Function for converting int or float value into time object \n
    param v: int | float \n
    return time
    """
    v_formatted = f"{v:.2f}"
    h, m = map(int, v_formatted.split("."))
    return time(h, m * 60 // 100)


def estimate_sla(today_mode: list, sla: int | float) -> tuple:
    for mode in today_mode:
        f, t = mode
        if f >= t:
            if sla > 24 - (f + t):
                sla -= 24 - (f + t)
                continue
            else:
                return sla, f
        else:
            if sla > t - f:
                sla -= t - f
                continue
            else:
                return sla, f


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
    Recursive function for getting the next day of the week if it's not weekend. \n
    param dt: datetime \n
    return: datetime
    """
    new_dt = dt + timedelta(days=1)
    if is_rest_day(new_dt):
        return next_day(new_dt)
    return new_dt


def make_time_list(
    request_from: float, request_to: float, from_time: float
) -> list[list]:
    """
    Function for making list with working time 'today' \n
    param request_from: float \n
    param request_to: float \n
    param from_time: float \n
    return: list[list]
    """
    if from_time >= request_to and request_from > request_to:
        if from_time < request_from:
            period = [request_from, 0.0]
        else:
            period = [from_time, 0.0]
        return [period]

    elif request_from == request_to:
        if from_time >= request_to:
            period = [from_time, 0]
            return [period]
        else:
            period = [from_time, 0]
            return [period]

    elif from_time >= request_to and request_from < from_time:
        return []

    elif request_to > from_time > request_from and request_from <= request_to:
        period = [from_time, request_to]
        return [period]

    elif from_time < request_to and from_time < request_from:
        if request_from > request_to:
            period1 = [from_time, request_to]
            period2 = [request_from, 0.0]
            return [period1, period2]
        else:
            period = [request_from, request_to]
        return [period]

    else:
        period = [request_from, request_to]
        return [period]

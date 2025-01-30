from datetime import datetime, time, timedelta


def make_time(v: int | float) -> time:
    """
    Function for converting int or float value into time object \n
    param v: int | float \n
    return time
    """
    v_formatted = f"{v:.2f}"
    h, m = map(int, v_formatted.split("."))
    return time(h, m * 60 // 100)


def next_day(dt: datetime) -> datetime:
    """
    Recursive function for getting the next day of the week if it's not weekend. \n
    param dt: datetime \n
    return: datetime
    """
    new_dt = dt + timedelta(days=1)
    if new_dt.weekday() >= 5:
        return next_day(new_dt)
    return new_dt


def make_time_list(
    request_from: float, request_to: float, from_time: float
) -> list[list]:
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

    elif (
        from_time < request_to and request_from <= request_to and from_time > request_from
    ):
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

from datetime import datetime, timedelta

from src.mainapp.schemas import RequestModel, ResponseModel
from src.mainapp.utils import (
    estimate_sla,
    is_rest_day,
    make_time,
    make_time_list,
    next_day,
)


def calculate_deadline(request: RequestModel) -> ResponseModel:
    """
    Main logic with recursive inner function.
    Calculates the deadline for the given request. \n
    param request: RequestModel \n
    return ResponseModel
    """
    current_work_from = request.date.hour + (request.date.minute / 60)

    def inner(
        dt: datetime = request.date,
        work_from: int | float = current_work_from,
        work_to: int | float = request.operating_mode_to,
        sla: int | float = request.sla_time,
    ) -> dict:
        """
        Inner function. First call with defaults args for correct calculate \n
        param dt: datetime \n
        param work_from: float | int \n
        param work_to: float | int \n
        param sla: float | int \n
        return datetime
        """
        if is_rest_day(dt):
            dt = next_day(dt).replace(hour=0, minute=0)
        from_time = dt.hour + dt.minute / 60
        # Add list with working periods of current day
        today_mode = make_time_list(
            request.operating_mode_from,
            work_to,
            from_time,
        )
        # sum all periods of the day
        working_hours = sum(
            24 - (a + b) if a >= b else b - a for a, b in today_mode if today_mode
        )

        if sla > working_hours:
            if today_mode:
                for mode in today_mode:
                    fr, to = mode
                    sla -= 24 - (fr + to) if fr >= to else to - fr
            new_dt = next_day(dt.replace(hour=0, minute=0))
            res = inner(
                dt=new_dt, work_from=request.operating_mode_from, work_to=work_to, sla=sla
            )

            return res

        est_sla, end_time = estimate_sla(today_mode, sla)
        sla_time = make_time(sla)
        fr_time = make_time(end_time)
        dt = dt.replace(hour=fr_time.hour, minute=fr_time.minute)
        res = dt + timedelta(hours=sla_time.hour, minutes=sla_time.minute)

        return {"deadline": res}

    return ResponseModel(**inner())

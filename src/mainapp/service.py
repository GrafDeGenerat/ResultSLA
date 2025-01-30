from datetime import datetime, timedelta

from mainapp.schemas import RequestModel, ResponseModel
from src.mainapp.utils import make_time, make_time_list, next_day


def calculate_deadline(request: RequestModel) -> ResponseModel:
    """
    Main logic with recursive inner function.
    Calculates the deadline for the given request. \n
    param request: RequestModel \n
    return ResponseModel
    """
    dt_float = request.date.hour + (request.date.minute / 60)

    def inner(
        dt: datetime = request.date,
        work_from: int | float = dt_float,
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
        dt_float = dt.hour + dt.minute / 60
        # Add list with working periods of current day
        today_mode = make_time_list(
            request.operating_mode_from,
            work_to,
            dt_float,
        )
        print(f"{today_mode=}")
        # sum all periods of the day
        working_hours = sum(
            24 - (a + b) if a >= b else b - a for a, b in today_mode if today_mode
        )
        print(f"{working_hours=}")
        print(f"{sla=}")
        if sla > working_hours:
            if today_mode:
                for mode in today_mode:
                    fr, to = mode

                    sla -= 24 - (fr + to) if fr >= to else to - fr
                    print(f"{sla=}")

            new_dt = next_day(dt.replace(hour=0, minute=0))
            res = inner(
                dt=new_dt, work_from=request.operating_mode_from, work_to=work_to, sla=sla
            )

            return res

        # Endpoint for func, added estimated SLA
        for mode in today_mode:
            fr, to = mode
            if fr >= to:
                if sla > 24 - (fr + to):
                    sla -= 24 - (fr + to)
                    continue
                else:
                    break
            else:
                if sla > to - fr:
                    sla -= to - fr
                    continue
                else:
                    break

        sla_time = make_time(sla)
        fr_time = make_time(fr)
        dt = dt.replace(hour=fr_time.hour, minute=fr_time.minute)
        res = dt + timedelta(hours=sla_time.hour, minutes=sla_time.minute)

        return {"deadline": res}

    return ResponseModel(**inner())

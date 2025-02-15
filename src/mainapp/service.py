from datetime import timedelta

from src.mainapp.schemas import RequestModel, ResponseModel
from src.mainapp.utils import (
    is_rest_day,
    next_day,
)
from src.timeapp.service import (
    SuperTime,
    TimesCollection,
)


def calculate_deadline(request: RequestModel) -> ResponseModel:
    """
    Main logic with recursive inner function.
    Calculates the deadline for the given request. \n
    param request: RequestModel \n
    return ResponseModel
    """
    if is_rest_day(request.date):
        result_date = next_day(request.date)
        first_work_from = SuperTime(0)
    else:
        result_date = request.date
        first_work_from = SuperTime(request.date.time())

    work_from = SuperTime(request.operating_mode_from)
    work_to = SuperTime(request.operating_mode_to)
    sla = SuperTime(request.sla_time / 60)
    daily_period = TimesCollection(work_from, work_to).intersect(first_work_from)

    while sla > 0:
        day_length = len(daily_period)

        if sla > day_length:
            result_date = next_day(result_date)

        sla, result_time = daily_period - sla
        work_from = SuperTime(request.operating_mode_from)
        daily_period = TimesCollection(work_from, work_to)

    result_date = result_date.replace(hour=0, minute=0, second=0)
    result_date += timedelta(seconds=result_time.total_seconds)
    return ResponseModel(**{"deadline": result_date})

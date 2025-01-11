from datetime import datetime, timedelta
from mainapp.schemas import RequestModel, ResponseModel
from src.mainapp.utils import next_day, make_time, make_float


def calculate_deadline(request: RequestModel) -> ResponseModel:
    dt_float = request.date.hour + request.date.minute / 60
    corrected_sla = request.sla_time
    mode_from = make_time(request.operating_mode_from)

    if request.date.time() < mode_from:
        corrected_sla += make_float(datetime.combine(request.date, mode_from) - request.date)

    def inner(dt=request.date,
              work_from=dt_float,
              work_to=request.operating_mode_to,
              sla=corrected_sla
              ) -> dict:
        if sla > (work_to - work_from):
            new_sla = sla - (work_to - work_from)
            new_dt = next_day(datetime.combine(dt.date(),
                                               make_time(request.operating_mode_from)))
            res = inner(dt=new_dt,
                        work_from=request.operating_mode_from,
                        work_to=request.operating_mode_to,
                        sla=new_sla)
            return res

        res = dt + timedelta(hours=sla)

        return {"deadline": res}

    return ResponseModel(**inner())




import typing

from attack_surface_pypy.models.v1.models import base


class StatsResponseModel(base.BaseModel):
    vm_count: int
    request_count: int
    average_request_time: typing.Optional[float]

# pylint: disable=no-member
from orjson import loads as orjson_loads
import pydantic

from attack_surface_pypy.utils import orjson_dumps


class BaseModel(pydantic.BaseModel):

    class Config:
        frozen = True

        json_dumps = orjson_dumps
        json_loads = orjson_loads

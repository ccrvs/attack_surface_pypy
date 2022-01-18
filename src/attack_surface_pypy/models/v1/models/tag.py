import pydantic

from attack_surface_pypy.models.v1.models import base


class TagModel(base.BaseModel):
    __root__: str = pydantic.Field(...)

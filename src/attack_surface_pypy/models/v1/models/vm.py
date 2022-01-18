import typing

import pydantic

from attack_surface_pypy import types
from attack_surface_pypy.models.v1.models import base, tag


class VMModel(base.BaseModel):
    vm_id: types.VM_ID
    name: str
    tags: typing.FrozenSet[tag.TagModel] = pydantic.Field(default_factory=frozenset)

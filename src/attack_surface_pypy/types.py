import re

import pydantic
import typing_extensions as typing

__all__ = (
    'VM_ID',
    'FW_ID',
)


class _IDType(pydantic.ConstrainedStr):
    min_length = 8
    max_length = 14


class _VmIDType(_IDType):
    regex = re.compile(r'^vm-\w{6,10}$')


class _FwIDType(_IDType):
    regex = re.compile(r'^fw-\w{6,10}$')


VM_ID: typing.TypeAlias = _VmIDType
FW_ID: typing.TypeAlias = _FwIDType

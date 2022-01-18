import typing

import pydantic

from attack_surface_pypy import constants


class Service(pydantic.BaseModel):
    host: str = pydantic.Field('localhost')
    port: int = pydantic.Field(8080, ge=1000, le=65535)  # TODO: maybe borders to constants?


class Domain(pydantic.BaseModel):
    file_path: pydantic.FilePath = pydantic.Field('./.json')  # TODO: consider multiple files?


class ServiceSettings(pydantic.BaseSettings):
    service: Service = pydantic.Field(Service())
    domain: Domain = pydantic.Field(Domain())

    encoding: str = 'utf-8'
    debug: bool = False
    log_level: str = 'INFO'
    traceback_depth: typing.Optional[int] = None
    autoreload: bool = False
    access_log: str = pydantic.Field(constants.HYPERCORN_STDOUT)
    error_log: str = pydantic.Field(constants.HYPERCORN_STDOUT)

    class Config:
        env_prefix = 'as_'
        env_file = '.env'
        env_nested_delimiter = '__'


settings = ServiceSettings()

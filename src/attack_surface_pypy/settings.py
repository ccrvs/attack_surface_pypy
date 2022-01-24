import typing

import pydantic

from attack_surface_pypy import constants


class Service(pydantic.BaseModel):
    host: str = pydantic.Field("0.0.0.0")  # FIXME: bind to all interfaces  # nosec
    port: int = pydantic.Field(8080, ge=1000, le=65535)  # TODO: maybe borders to constants?


class Domain(pydantic.BaseModel):
    file_path: pydantic.FilePath = pydantic.Field("./.json")  # TODO: consider multiple files?


class ServiceSettings(pydantic.BaseSettings):
    service: Service = pydantic.Field(Service())

    encoding: str = "utf-8"
    debug: bool = False
    log_level: str = "ERROR"#'INFO'
    traceback_depth: typing.Optional[int] = None
    autoreload: bool = False
    backlog: int = 4096

    class Config:
        env_prefix = "as_"
        env_file = ".env"
        env_nested_delimiter = "__"


settings = ServiceSettings()

from __future__ import annotations

import pathlib
import typing

from attack_surface_pypy.core import exceptions, probes, utils
from attack_surface_pypy.logging import structlog
from attack_surface_pypy.models.v1.models import base, cloud

T_co = typing.TypeVar("T_co", bound=base.BaseModel, covariant=True)
logger = structlog.get_logger()


class DataLoaderProto(typing.Protocol[T_co]):

    def load(self) -> T_co:
        ...


class CloudDataJSONFileLoader(DataLoaderProto[cloud.CloudEnvironmentModel]):
    _TIMEOUT_SEC = 30

    def __init__(
            self,
            path: typing.Union[str, pathlib.Path],
            probe: probes.DataLoaderProbe,
            timeout: int = _TIMEOUT_SEC,
    ):
        self._path = path
        self._timeout = timeout
        self._probe = probe

        # TODO: maybe switch to domain probing logging?
        self._probe.inited(timeout=timeout, path=path)

    def load(self) -> cloud.CloudEnvironmentModel:
        try:
            # with utils.timeout(self._timeout):
            data_model = cloud.CloudEnvironmentModel.parse_file(self._path)
            self._probe.loaded(path=self._path)
            return data_model
                # async with await trio.open_file(self._path, 'r') as f:
                #     content = await f.read()
                    # self._probe.read(path=self._path)
                    # model = cloud.CloudEnvironmentModel.parse_raw(content)
                    # self._probe.loaded(path=self._path)
                    # return model
        # TODO: ValidationError?
        except TimeoutError as e:
            # FIXME: yes, I know about logger.exception, but it's now working
            self._probe.error(error=e)

            raise exceptions.TimeoutExceededError(self._timeout) from e
        except FileNotFoundError as e:
            self._probe.error(error=e)
            raise exceptions.LoaderFileNotFoundError(self._path) from e
        except TypeError as e:
            self._probe.error(error=e)
            raise exceptions.InvalidFileDataError(str(self._path)) from e
        except OSError as e:
            # TODO: mind retries
            self._probe.failed(error=e)
            raise exceptions.InternalError() from e
        except Exception as e:
            self._probe.failed(error=e)
            raise exceptions.InternalError() from e

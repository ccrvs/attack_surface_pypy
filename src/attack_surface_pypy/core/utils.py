__all__ = ("timeout", )

import contextlib
import typing

import structlog
import trio

logger = structlog.get_logger()


@contextlib.contextmanager
def timeout(seconds: int) -> typing.Generator[None, None, None]:
    # TODO: better to elaborate to incremental timeouts with exponential cutoffs
    try:
        logger.debug("timeout.set_to", seconds=seconds)
        with trio.fail_after(seconds):
            yield
        logger.debug("timeout.gone")
    except trio.TooSlowError as e:
        logger.error("timeout.error", seconds=seconds, error=e)
        raise TimeoutError(seconds) from e

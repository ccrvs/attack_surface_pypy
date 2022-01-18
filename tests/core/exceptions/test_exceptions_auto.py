# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.
from pathlib import Path

from hypothesis import given, strategies as st

import attack_surface_pypy.core.exceptions


@given(message=st.text())
def test_fuzz_InvalidFileDataError(message):
    attack_surface_pypy.core.exceptions.InvalidFileDataError(message=message)


@given(message=st.integers() | st.floats())
def test_fuzz_TimeoutExceededError(message):
    attack_surface_pypy.core.exceptions.TimeoutExceededError(message=message)


@given(message=st.from_regex(r'^vm-\w{6,10}$'))
def test_fuzz_VMNotFoundError(message):
    attack_surface_pypy.core.exceptions.VMNotFoundError(message=message)


@given(message=st.one_of(st.builds(Path), st.text()))
def test_fuzz_LoaderFileNotFoundError(message):
    attack_surface_pypy.core.exceptions.loader.LoaderFileNotFoundError(message=message)

# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import attack_surface_pypy.core.probes
from hypothesis import given, strategies as st


@given(logging_factory=st.functions(), analytics_factory=st.functions())
def test_fuzz_ContainerProbe(logging_factory, analytics_factory):
    attack_surface_pypy.core.probes.ContainerProbe(
        logging_factory=logging_factory, analytics_factory=analytics_factory
    )


@given(logging_factory=st.functions(), analytics_factory=st.functions())
def test_fuzz_DataLoaderProbe(logging_factory, analytics_factory):
    attack_surface_pypy.core.probes.DataLoaderProbe(
        logging_factory=logging_factory, analytics_factory=analytics_factory
    )


@given(logging_factory=st.functions(), analytics_factory=st.functions())
def test_fuzz_DomainProbe(logging_factory, analytics_factory):
    attack_surface_pypy.core.probes.DomainProbe(
        logging_factory=logging_factory, analytics_factory=analytics_factory
    )


@given(logging_factory=st.functions(), analytics_factory=st.functions())
def test_fuzz_RepositoryProbe(logging_factory, analytics_factory):
    attack_surface_pypy.core.probes.RepositoryProbe(
        logging_factory=logging_factory, analytics_factory=analytics_factory
    )


@given(logging_factory=st.functions(), analytics_factory=st.functions())
def test_fuzz_RouteProbe(logging_factory, analytics_factory):
    attack_surface_pypy.core.probes.RouteProbe(
        logging_factory=logging_factory, analytics_factory=analytics_factory
    )

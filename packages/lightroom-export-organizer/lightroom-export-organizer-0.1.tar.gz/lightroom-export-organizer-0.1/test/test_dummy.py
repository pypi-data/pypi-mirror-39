import pytest

from lightroom_export_organizer.greet_world import greet_world


@pytest.mark.parametrize("descriptor", [
    (None),
    ("Big")
])
def test_dummy(descriptor):
    greet_world(descriptor)

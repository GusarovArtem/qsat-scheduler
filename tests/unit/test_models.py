import pytest

from qsat.domain.models import Satellite


def test_satellite_valid():
    # verify that a well-formed satellite object is created without errors
    sat = Satellite(
        name="ISS",
        norad_id=25544,
        tle_line1="1 25544U 98067A   24001.5 .00001 00000-0 00001-4 0 9999",
        tle_line2="2 25544  51.6400 0.0000 0001000 0.0000 0.0000 15.50000000000000",
    )
    assert sat.name == "ISS"
    assert sat.norad_id == 25544

def test_satellite_rejects_bad_norad_id():
    # norad_id must be a positive integer
    with pytest.raises(ValueError):
        Satellite(name="X", norad_id=-1, tle_line1="1 ...", tle_line2="2 ...")
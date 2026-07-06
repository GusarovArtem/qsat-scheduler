from pathlib import Path

import pytest

from qsat.orbits.tle import parse_tle_text

FIXTURES_DIR = Path(__file__).parent.parent.parent / "fixtures"

@pytest.fixture
def tle_text() -> str:
    """ Load sample TLE data from the fixture file. """
    #pytest injects this into any test that declares tle_text as an argument
    return (FIXTURES_DIR / "stations.tle").read_text()

def test_parse_returns_satellites(tle_text: str) -> None:
    result = parse_tle_text(tle_text)
    # fixture has 3 satellites
    assert len(result) == 3

def test_parse_first_satellite_is_iss(tle_text: str) -> None:
    result = parse_tle_text(tle_text)
    assert result[0].name == "ISS (ZARYA)"
    assert result[0].norad_id == 25544
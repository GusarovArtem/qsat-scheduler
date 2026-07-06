from datetime import datetime, timezone
from locale import windows_locale

from qsat.domain.models import Satellite, Target
from qsat.orbits.access import find_access_windows

ISS = Satellite(
    name="ISS (ZARYA)",
    norad_id=25544,
    tle_line1="1 25544U 98067A   24001.50000000  .00001686  00000+0  30788-4 0  9992",
    tle_line2="2 25544  51.6401 183.7890 0002126 336.4130  35.3690 15.49964396434588",
)

WARSAW = Target(name="Warsaw", lat=52.2, lon=21.0, value=10.0)
START = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
END = datetime(2024, 1, 2, 0, 0, 0, tzinfo=timezone.utc)

def test_finds_windows_in_24h():
    windows = find_access_windows(ISS, WARSAW, START, END)
    # ISS orbits ~15x/day, Warsaw at 52 deg N sees several passes
    assert len(windows) > 0

def test_window_times_are_ordered():
    windows = find_access_windows(ISS, WARSAW, START, END)
    for w in windows:
        assert w.rise < w.culminate < w.set_ # comparing by time

def test_window_elevation_exceeds_minimum():
    windows = find_access_windows(ISS, WARSAW, START, END)
    for w in windows: # simple check is max >= min
        assert w.max_elevation_deg >= WARSAW.min_elevation_deg

def test_window_duration_is_reasonable():
    windows = find_access_windows(ISS, WARSAW, START, END)
    for w in windows:
        duration_s = (w.set_ - w.rise).total_seconds()
        # ISS passes last roughly 2-12 minutes
        assert 60 < duration_s < 800

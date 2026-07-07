from datetime import datetime, timedelta, timezone

from qsat.domain.models import Satellite
from qsat.viz.tracks import ground_track

ISS = Satellite(
    name="ISS (ZARYA)",
    norad_id=25544,
    tle_line1="1 25544U 98067A   24001.50000000  .00001686  00000+0  30788-4 0  9992",
    tle_line2="2 25544  51.6401 183.7890 0002126 336.4130  35.3690 15.49964396434588",
)
START = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

def test_ground_track_length():
    end = START + timedelta(minutes=90)
    lons, lats = ground_track(ISS, START, end, step_s=60.0)
    # 90 min / 60 s + 1 = 91 points
    assert len(lons) == len(lats) == 91

def test_ground_track_coords_are_valid():
    end = START + timedelta(minutes=90)
    lons, lats = ground_track(ISS, START, end, step_s=60.0)
    assert all(-180 <= lon <= 180 for lon in lons)
    assert all(-180 <= lat <= 180 for lat in lats)
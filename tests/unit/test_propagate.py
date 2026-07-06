from datetime import datetime, timezone
from qsat.domain.models import Satellite
from qsat.orbits.propagate import subpoint

# Real ISS TLE (approximate - exact values don't matter for sanity checks
ISS = Satellite(
    name="ISS (ZARYA)",
    norad_id=25544,
    tle_line1="1 25544U 98067A   24001.50000000  .00001686  00000+0  30788-4 0  9992",
    tle_line2="2 25544  51.6401 183.7890 0002126 336.4130  35.3690 15.49964396434588",
)
T = datetime(2024,1, 1, 12, 0, 0, tzinfo=timezone.utc)

def test_iss_altitude_is_realistic():
    _,_, alt_km = subpoint(ISS, T)
    #ISS orbits between 400-420lm - allow wider sanity bad
    assert 350 <= alt_km <= 450

def test_iss_lat_within_inclination():
    lat, _, _ = subpoint(ISS, T)
    #ISS inclination is ~51.6 degrees - latitude can never exceed that
    assert abs(lat) <= 52
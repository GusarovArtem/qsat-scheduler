from datetime import datetime
from datetime import timezone

from qsat.domain.models import Satellite, Target
from qsat.orbits.geometry import look_angles
from qsat.orbits.propagate import subpoint

ISS = Satellite(
    name="ISS (ZARYA)",
    norad_id=25544,
    tle_line1="1 25544U 98067A   24001.50000000  .00001686  00000+0  30788-4 0  9992",
    tle_line2="2 25544  51.6401 183.7890 0002126 336.4130  35.3690 15.49964396434588",
)

T = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


def test_elevation_overhead():
    # target placed at the satellite's own subpoint -> elevation must be near 90 degrees
    lat, lon, _ = subpoint(ISS, T)
    target = Target(name="overhead", lat=round(lat, 4), lon=round(lon, 4), value=1.0)
    el, _ = look_angles(ISS, target, T)
    assert el > 85


def test_elevation_below_horizon():
    # target on the far side of Earth -> satellite is below horizon
    lat, lon, _ = subpoint(ISS, T)
    far_target = Target(
        name="far",
        lat=-lat,
        lon=lon + 180 if lon <= 0 else lon - 180,
        value=1.0)
    el, _ = look_angles(ISS, far_target, T)
    assert el < 0

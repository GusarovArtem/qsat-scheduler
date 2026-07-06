from datetime import datetime
from skyfield.api import EarthSatellite, load, wgs84
from qsat.domain.models import Satellite

def subpoint(sat: Satellite, t: datetime) -> tuple[float, float, float]:
    """ Return (lat_deg, lon_deg, alt_lm) of sat at UTC time t. """
    ts = load.timescale() # UTC + time fixes due to Eath slowing
    sky_sat = EarthSatellite(sat.tle_line1, sat.tle_line2, sat.name, ts) # loads TLE and preps SGP4-propagator.

    # Result — vector in geocentric coordinates (Earth center = start of coordinates).
    sky_t = ts.utc(t.year, t.month, t.day, t.hour, t.minute, t.second) #  starts SGP4: calcs where sat in t.

    geocentric = sky_sat.at(sky_t)
    # processe vector on the Earth land by WGS84 model
    subpnt = wgs84.subpoint(geocentric) # (same ellipse that in the GPS). Returns lat, lon and h
    return (
        subpnt.latitude.degrees,
        subpnt.longitude.degrees,
        subpnt.elevation.km
    )
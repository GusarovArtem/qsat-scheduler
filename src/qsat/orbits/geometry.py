from datetime import datetime

from skyfield.api import EarthSatellite, load, wgs84

from qsat.domain.models import Satellite, Target


def look_angles(sat: Satellite, target: Target, t: datetime) -> tuple[float, float]:
    """ Return (elevation_deg, azimuth,deg) of sat as seen from target at UTC time t. """
    ts = load.timescale()
    sky_sat = EarthSatellite(sat.tle_line1, sat.tle_line2, sat.name, ts) # vector observer -> satellite (topocentric)
    observer = wgs84.latlon(target.lat, target.lon) #observer from Earth land
    sky_t = ts.utc(t.year, t.month, t.day, t.hour, t.minute, t.second)
    topocentric = (sky_sat - observer).at(sky_t)
    alt, az, _ = topocentric.altaz() # returns (altitude, azimuth, distance)
    return alt.degrees, az.degrees

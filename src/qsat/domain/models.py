from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Satellite:
    """ A satellite identified by its NORAD catalogue number and TLE orbit data """
    name: str
    norad_id: int
    tle_line1: str
    tle_line2: str
    def __post_init__(self) -> None:
        # Python calls __post_init automatically after __init__
        # the only place to validate fields on a frozen dataclass
        if self.norad_id <= 0:
            raise ValueError(f"norad_id must be positive, got {self.norad_id}")
        if not self.tle_line1.startswith("1 "):
            raise ValueError(f"tle_line1 must start with '1 ', got {self.tle_line1}")
        if not self.tle_line2.startswith("2 "):
            raise ValueError(f"tle_line2 must start with '2 ', got {self.tle_line2}")

@dataclass(frozen=True)
class Target:
    """ An imaging target on Earth's surface with a priority value."""
    name: str
    lat: float                       # degrees, -90..90
    lon: float                       # degrees, -180..180
    value: float                     # relative priority weight, must be positive
    min_elevation_deg: float = 10.0  # default min elevation for imaging


    def __post_init__(self) -> None:
        if not -90 <= self.lat <= 90:
            raise ValueError(f"lat must be in [-90, 90], got {self.lat}")
        if not -180 <= self.lon <= 180:
            raise ValueError(f"lat must be in [-180, 180], got {self.lon}")
        if self.value <= 0:
            raise ValueError(f"value must be positive, got {self.value}")

@dataclass(frozen=True)
class AccessWindow:
    """ One continious pass of sat above target's horizon. """
    sat: Satellite
    target: Target
    rise: datetime # ↑ rise
    culminate: datetime # ↑ peak
    set_:datetime #set_ because is a Python build-in name
    max_elevation_deg: float
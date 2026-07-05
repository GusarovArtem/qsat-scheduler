from dataclasses import dataclass


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
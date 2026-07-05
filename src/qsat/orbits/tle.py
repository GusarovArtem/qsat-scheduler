import time
from pathlib import Path

import requests

from qsat.domain.models import Satellite


def parse_tle_text(text: str) -> list[Satellite]:
    """ Parse a multi-satellite TLE text block into a list of Satellite objects. """
    # strip blank lines so we always get clean 3-line groups
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    satellites = []
    #every 3 consecutive lines = pne satellite: name, line1, line2
    for i in range(0, len(lines), 3):
        name = lines[i]
        line1 = lines[i + 1]
        line2 = lines[i + 2]
        # NORAD id lives in columns 2-7 of line 1 (the TLE format spec)
        norad_id = int(line1[2:7])
        satellites.append(
            Satellite(name=name, norad_id=norad_id, tle_line1=line1, tle_line2=line2)
        )
    return satellites


CELESTRAK_BASE = "https://celestrak.org/NORAD/elements/gp.php"

def fetch_tle_group(group: str, cache_dir: Path, max_age_hours: float = 6.0) -> list[Satellite]:
        """ Fetch a TLE  group from CelesTrak; serve from local cache if fresh enough. """
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / f"{group}.tle"
        # check cache freshness before hitting the network
        if cache_file.exists():
            age_hours = (time.time() - cache_file.stat().st_mtime) / 3600
            if age_hours < max_age_hours:
                return parse_tle_text(cache_file.read_text())
        url = f"{CELESTRAK_BASE}?GROUP={group}&FORMAT=tle"
        try:
            response = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "qsat-scheduler/0.1"}
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            if cache_file.exists():
                # stale cache is better than crashing when offline
                return parse_tle_text(cache_file.read_text())
            raise RuntimeError(f"Cannot reach TLE for '{group}', no cache available") from exc
        cache_file.write_text(response.text)
        return parse_tle_text(response.text)


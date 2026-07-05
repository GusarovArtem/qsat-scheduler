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
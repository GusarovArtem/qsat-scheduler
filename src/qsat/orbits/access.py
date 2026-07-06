from datetime import datetime, timedelta

from qsat.domain.models import Satellite, Target, AccessWindow
from qsat.orbits.geometry import look_angles


# i →  0    1    2    3    4    5    6
# el: -5°  -2°  +8° +43° +12°  -3°  -8°
#           ↑         ↑          ↑
#        rise(i=1)  peak(i=3)  set(j=5)
#                               i=j=5 → continue with 5

def find_access_windows(
        sat: Satellite,
        target: Target,
        start: datetime,
        end: datetime,
        step_s: float = 60.0
) -> list[AccessWindow]:
    """ Return all passes of sat above target between start abd end (UTC). """
    min_el = target.min_elevation_deg
    
    # build a grid of times and pre-compute elevation at each point
    times: list[datetime] = []
    t = start
    while t <= end:
        times.append(t)
        t += timedelta(seconds=step_s)
        
    # [0] - we take only elevation from (elevation, azimuth)
    elevations: list[float] = [look_angles(sat, target, t)[0] for t in times]
    
    windows: list[AccessWindow] = []
    i = 0
    while i < len(times) - 1:
        # detect rise elevation crosses min_el from below
        if elevations[i] < min_el <= elevations[i + 1]:
            rise = times[i + 1]
            peak_el = elevations[i + 1]
            peak_t = times[i + 1]

            # scan forward inside the window to find peak and set
            j = i + 1
            while j < len(times) - 1 and elevations[j] >= min_el:
                if elevations[j] > peak_el:
                    peak_el = elevations[j]
                    peak_t = times[j]
                j+= 1

            windows.append(AccessWindow(
                sat=sat,
                target=target,
                rise=rise,
                culminate=peak_t,
                set_=times[j],
                max_elevation_deg=peak_el
            ))
            i = j # jump past this window
        else:
            i += 1

    return windows

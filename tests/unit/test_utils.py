from qsat.utils import clamp


def test_clamp_within_range():
    # 5 is inside the clamp - we do not touch it
    assert clamp(5, 0, 10) == 5

def test_clamp_below_min():
    # -3 is smaller than min - we return min
    assert clamp(-3, 0, 10) == 0

def test_clamp_below_max():
    # 15 is higher  than max - we return max
    assert clamp(15, 0, 10) == 10

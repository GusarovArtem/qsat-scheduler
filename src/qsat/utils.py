def clamp(value: float, min_val: float, max_val: float) -> float:
    """ Return value compared to min_val, max_val. """
    # built-in max/min compose cleanly - no if/else needed
    return max(min_val, min(value, max_val))
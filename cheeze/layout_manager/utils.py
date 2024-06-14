def _float0(val):
    if isinstance(val, (float, int)):
        return val
    else:
        return 0
    
def _collides_rect(point: tuple[float, float], pos: tuple[float, float], size: tuple[float, float]) -> bool:
    return pos[0] <= point[0] <= pos[0] + size[0] and pos[1] <= point[1] <= pos[1]+size[1]
import enum

class RotationAxis(enum.Enum):
    CENTER = 0

def rotate_newleft(pos: tuple[float, float], size: tuple[float, float], posbounding: tuple[float, float], sizebounding: tuple[float, float], axis: RotationAxis, rot: float):
    """
    Return the new left position of the bounding rectangle

    It takes the initial position of unrotated rectangle along with size,
    position of bounding rect and size of bounding rect after rotation (assuming bounding rect.topleft = initial.topleft),
    axis of rotation, and value of rotation in radians
    """

    match axis:
        case RotationAxis.CENTER:
            x = pos[0] + (size[0] - sizebounding[0])/2
            y = pos[1] + (size[1] - sizebounding[1])/2
            return (x, y)
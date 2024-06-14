import enum
from . import units

class MainAxisAlignment(enum.Enum):
    """
    Alignment along the main axis, used mostly with LayoutSequence
    """
    start = 0
    center = 1
    end = 2
    space_around = 3
    space_between = 4

class CrossAxisAlignment(enum.Enum):
    """
    Alignment along the cross axis, used mostly with LayoutSequence
    """
    start = 0
    center = 1
    end = 2

def align(space: float, spaces: list[float], alignment):
    return globals()["align_"+alignment.name](space, list(spaces))

def align_start(space: float, spaces: list[float]):
    """
    given a total amount of space, align the given spaces at the start and return the resultant positions

    [(1)(2)(3)                   ]
    """
    pos = 0
    for x in spaces:
        yield pos
        pos += x

def align_end(space: float, spaces: list[float]):
    """
    given a total amount of space, align the given spaces at the end and return the resultant positions
    [                   (1)(2)(3)]
    """
    pos = space - sum(spaces)
    for x in spaces:
        yield pos
        pos += x

def align_center(space: float, spaces: list[float]):
    """
    given a total amount of space, align the given spaces at the center and return the resultant positions
    [          (1)(2)(3)         ]
    """
    pos = (space - sum(spaces))/2
    for x in spaces:
        yield pos
        pos += x

def align_space_around(space: float, spaces: list[float]):
    """
    given a total amount of space, align the given spaces with padding around them and return the resultant positions
    [    (1)     (2)     (3)     ]
    """
    free_space = space - sum(spaces)
    free_spacer = free_space / (len(spaces)+1)
    pos = free_spacer
    for x in spaces:
        yield pos
        pos += x + free_spacer

def align_space_between(space: float, spaces: list[float]):
    """
    given a total amount of space, align the given spaces with padding between them and return the resultant positions
    [(1)         (2)          (3)]

    in case that there is only a single object, the object is centered
    [            (1)             ]
    """
    if len(spaces) < 1:
        return align_center(space, spaces)
    free_space = space - sum(spaces)
    free_spacer = free_space / (len(spaces)-1)
    pos = 0
    for x in spaces:
        yield pos
        pos += x + free_spacer
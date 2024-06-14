import enum

class EventType(enum.Enum):
    CLICK = 0
    ACTIVE = 1
    UNACTIVE = 2
    HOVER = 3
    UNHOVER = 4
    FOCUS = 5
    UNFOCUS = 6
    KEYPRESS = 7
    SHORTCUT = 8


class Event:
    """
    An event object, it is passed according to layoutobject tree. An object in layoutobject tree can be passthrough
    to allow event passing. If an element in layout tree is not pass through, the event is consumed by the said widget
    """
    def __init__(self, type: EventType, *, pos: tuple[float, float] = None, key: str = None) -> None:
        self.type = type
        self.pos = pos
        self.key = key

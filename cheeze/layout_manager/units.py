import enum
from .utils import _collides_rect

class UNIT(enum.Enum):
    """
    The unit enum
    """
    px = 0
    percent = 1
    f = 2
    vw = 3
    vh = 4

# Internally used conversion table to convert from string unit to the unit enum
_UNITS = {
    "%": UNIT.percent,
    "px": UNIT.px,
    "vw": UNIT.vw,
    "vh": UNIT.vh,
    "f": UNIT.f
}

_UNITS_REVERSED = {v: k for k, v in _UNITS.items()}

# The actual Unit object used for calculations etc...
class LUnit:
    """
    The Unit of a given layout it can be
    
    * pixels (px)
    * percentage (%)
    * flex (f)
    * viewport width % (vw)
    * viewport height % (vh)
    """

    def __init__(self, *args) -> None:

        # If the arguement is provided as a single string "4 px"
        # The string must be space separated
        if isinstance(args[0], str):
            val, unit = args[0].split(' ', 1)
            self.val = float(val)
            self.unit = _UNITS[unit]

        # if the argument is provided as 2-argument pair of (value: int, unit: str/Unit Enum)
        elif isinstance(args[0], (float, int)):
            self.val = args[0]

            if len(args) <= 1:
                self.unit = UNIT.px

            # Check the second argument
            elif isinstance(args[1], (UNIT, int)):
                self.unit = args[1]
            else:
                self.unit = _UNITS[1]  # Else just convert the string to proper unit...
        
        elif isinstance(args[0], LUnit):  # If the said instance already a LUnit
            self.unit = args[0].unit
            self.val = args[0].val
        else:
            raise TypeError(f"Unknown LUnit constructor args: {args}")

    # Make sure that the units match for any maths operation
    def _check_math(self, other: "LUnit") -> None:
        if isinstance(other, (float, int)):  # Given regular arithmetic, auto convert to LUnit
            other = LUnit(other, self.unit)
        assert self.unit == other.unit, "Different Units cannot be added"
        return other
        
    # Below are the classic addition, subtraction, multiplication and division functions
    def __add__(self, other: "LUnit") -> "LUnit":
        other = self._check_math(other)
        return LUnit(self.val + other.val, self.unit)
    
    def __sub__(self, other: "LUnit") -> "LUnit":
        other = self._check_math(other)
        return LUnit(self.val - other.val, self.unit)

    def __mul__(self, other: "LUnit") -> "LUnit":
        other = self._check_math(other)
        return LUnit(self.val * other.val, self.unit)

    def __truediv__(self, other: "LUnit") -> "LUnit":
        other = self._check_math(other)
        return LUnit(self.val / other.val, self.unit)
    
    def abs(self, space: float, viewport_space: "LUnit2"):
        """
        Given an absolute amount of space in pixels.
        the returend space is an absolute LUnit that does not exceed the given space
        the returned LUnit's unit is UNIT.px

        Special case for flex units, all the space is occupied instead!
        So, the layout objects giving flex sized units space should automatically
        divide the space!
        """
        match self.unit:
            case UNIT.px:
                return LUnit(min(space, self.val), UNIT.px)
            case UNIT.percent:
                return LUnit(min(space, self.val*space/100), UNIT.px)
            case UNIT.vh:
                return LUnit(min(space, min(self.val, 100)*viewport_space.y.val/100), UNIT.px)
            case UNIT.vw:
                return LUnit(min(space, min(self.val, 100)*viewport_space.x.val/100), UNIT.px)
            case UNIT.f:
                return LUnit(space, UNIT.px)
            case _:
                raise TypeError(f"Unknown Unit Type: {self.unit}")
    
    def __repr__(self) -> str:
        return f"{self.val}{_UNITS_REVERSED[self.unit]}"
    
    def __abs__(self) -> int:
        return self.val
    
    def as_float(self) -> float:
        return self.val

class LUnit2:
    """
    2 Dimensional Unit
    """
    def __init__(self, x: LUnit, y: LUnit) -> None:
        if isinstance(x, str):
            self.x = LUnit(x)
        elif isinstance(x, tuple):
            self.x = LUnit(*x)
        elif isinstance(x, (float, int)):
            self.x = LUnit(x, UNIT.px)
        else:
            self.x = x
        
        if isinstance(y, str):
            self.y = LUnit(y)
        elif isinstance(y, tuple):
            self.y = LUnit(*y)
        elif isinstance(y, (float, int)):
            self.y = LUnit(y, UNIT.px)
        else:
            self.y = y

    def __add__(self, others: "LUnit2") -> "LUnit2":
        if isinstance(others, tuple):  # If the other unit is a tuple(int, int)
            return LUnit2(self.x + others[0], self.y + others[1])
        return LUnit2(self.x + others.x, self.y + others.y)
    
    def __sub__(self, others: "LUnit2") -> "LUnit2":
        if isinstance(others, tuple):
            return LUnit2(self.x - others[0], self.y - others[1])
        return LUnit2(self.x - others.x, self.y - others.y)
    
    def __mul__(self, others: "LUnit2") -> "LUnit2":
        if isinstance(others, tuple):
            return LUnit2(self.x * others[0], self.y * others[1])
        return LUnit2(self.x * others.x, self.y * others.y)
    
    def __truediv__(self, others: "LUnit2") -> "LUnit2":
        if isinstance(others, tuple):
            return LUnit2(self.x / others[0], self.y / others[1])
        return LUnit2(self.x / others.x, self.y / others.y)
    
    def abs_x(self, *args) -> "LUnit2":
        """Abs function for the x axis"""
        return LUnit2(self.x.abs(*args), self.y)

    def abs_y(self, *args) -> "LUnit2":
        """Abs function for the y axis"""
        return LUnit2(self.x, self.y.abs(*args))
    
    def abs(self, x_space, y_space, *args) -> "LUnit2":
        """Abs function for both the axis"""
        return LUnit2(self.x.abs(x_space, *args), self.y.abs(y_space, *args))
    
    def with_x(self, arg: LUnit) -> "LUnit2":
        """Change the x component of the LUnit object and return a new object"""
        return LUnit2(LUnit(arg), self.y)
    
    def with_y(self, arg: LUnit) -> "LUnit2":
        """Change the y component of the LUnit object and return a new object"""
        return LUnit2(self.x, LUnit(arg))
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def as_float(self) -> tuple[float, float]:
        return (self.x.val, self.y.val)
    
class LRect:
    """
    A simple rectangle with all sorts of functions
    """
    def __init__(self, pos: tuple[float, float], size: tuple[float, float]) -> None:
        self.pos = pos
        self.size = size

    def collides_with(self, point: tuple[float, float]) -> bool:
        return _collides_rect(point, self.pos, self.size)
    
    def collides_withr(self, rect: "LRect") -> bool:
        if isinstance(rect, tuple):
            rect = LRect(rect)
        
        if self.is_zero() or rect.is_zero():
            return False
        
        # If one rectangle is left to the other
        if self.pos[0] > (rect.pos[0] + rect.size[0]) or rect.pos[0] > (self.pos[0] + self.size[0]):
            return False
    
        # If one rectangle is above other
        if self.pos[1] > (rect.pos[1] + rect.size[1]) or rect.pos[1] > (self.pos[1] + self.size[1]):
            return False
    
        return True
    
    def is_zero(self) -> bool:
        """
        If the rectangle is zero in size
        """
        return self.size[0] <= 0 or self.size[1] <= 0
        

    def as_float(self) -> tuple[float, float, float, float]:
        """
        returns (x, y, w, h)
        """
        return (*self.pos, *self.size)
    
    def as_int(self) -> tuple[int, int, int, int]:
        """
        similar to as_float but returns integers instead
        """
        return (int(self.pos[0]), int(self.pos[1]), int(self.size[0]), int(self.size[1]))
    
    def __add__(self, r: "LRect") -> "LRect":
        """
        Returns a rectangle that encompasses the given rectangle
        """
        if self.is_zero():
            return r
        elif r.is_zero():
            return self
        
        left = min(self.pos[0], r.pos[0])
        top = min(self.pos[1], r.pos[1])
        right = max(self.pos[0]+self.size[0], r.pos[0]+r.size[0])
        bottom = max(self.pos[1]+self.size[1], r.pos[1]+r.size[1])

        w = right-left
        h = bottom-top

        return LRect((left, top), (w, h))
    
    def clip(self, r: "LRect") -> "LRect":
        """
        Clip the rectangle to the bounds of a given rectangle.
        Essentially, get the intersection of the two rectangles
        """
        if self.is_zero():
            return r
        elif r.is_zero():
            return self
        
        if isinstance(r, tuple):
            r = LRect(r[:2], r[2:])

        left = max(self.pos[0], r.pos[0])
        top = max(self.pos[1], r.pos[1])
        right = min(self.pos[0]+self.size[0], r.pos[0]+r.size[0])
        bottom = min(self.pos[1]+self.size[1], r.pos[1]+r.size[1])

        w = right-left
        h = bottom-top

        return LRect((left, top), (w, h))
    
    def __repr__(self) -> str:
        return f"LRect({self.pos}, {self.size})"
    
    def __hash__(self) -> int:
        return hash((*self.pos, *self.size))
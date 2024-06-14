from .layout_object import LayoutObject
from .units import LUnit2, LUnit, UNIT
from .utils import _float0

class LayoutSimple(LayoutObject):
    """
    A Simple LayoutObject which doesn't have any children and simply occupies
    a given amount of size and is also provided a minimum preferred size!

    This shall be used by widgets that needn't do anything about children and 
    is simply concerned with itself.
    """
    def __init__(self, size: LUnit2, preferred: tuple[float, float] = (None, None)) -> None:
        super().__init__()
        self.dim = size
        self.preferred = preferred

    def prefer(self) -> None:

        # If either of the values are set to be pixels, automatically set the preferred size
        # to be the actual preferred needed at most! max of pixel value in self.dim and current
        # value of self.preferred.
        if self.dim.x.unit == UNIT.px:
            self.preferred = (max(self.dim.x.val, _float0(self.preferred[0])), _float0(self.preferred[1]))
        if self.dim.y.unit == UNIT.px:
            self.preferred = (_float0(self.preferred[0]), max(self.dim.y.val, _float0(self.preferred[1])))

    def __repr__(self):
        return "Simple"+super().__repr__()
    
    def layout_representation(self):
        return "Simple"+super().layout_representation()
from .units import LUnit, LUnit2
import abc
from .utils import _collides_rect

class LayoutObject(abc.ABC):
    """
    Abstract class for LayoutObjects

    Contains 4 instance variables:
    1. dim: Wanted Dimensions
    2. pos: Rendered Position
    3. rendered: Rendered Dimensions
    4. preferred: Preferred Minimum Absolute Dimensions

    Components of preferred dimensions can have either a float value
    indicating a minimum size wanted in pixels or None indicating
    that their is no preference
    """
    def __init__(self) -> None:
        self.dim = LUnit2(0, 0)

        self.pos = LUnit2(0, 0)
        self.rendered = LUnit2(0, 0)
        
        self.preferred: tuple[float, float] = (None, None)

    def render(self, space: LUnit2, viewport: LUnit2, offset: LUnit2) -> None:
        """
        Given the amount of space available for the said layoutobject, and viewport
        dimensions, calculate the layout object's absolute rendered dimensions
        and position in pixels
        """
        self.rendered = self.dim.abs(space.x.val, space.y.val, viewport)
        self.pos = offset

    def prefer(self) -> None:
        """
        Set the layout object's preferred minimum dimensions.
        """
        pass
    
    def calculate(self, space: LUnit2, viewport: LUnit2, offset: LUnit2 = LUnit2(0, 0)) -> None:
        """
        Simply run prefer methods of all children items
        and then render them based on calculated preferences!
        """
        self.prefer()
        self.render(space, viewport, offset)

    def __repr__(self):
        """
        Actual positions and values
        """
        return f"[x={self.pos.x} y={self.pos.y} w={self.rendered.x} h={self.rendered.y}]"
    
    def layout_representation(self):
        return f"[x={self.dim.x} y={self.dim.y}" + ("" if self.preferred[0] is None else f" minx={self.preferred[0]}") + ("" if self.preferred[1] is None else f" miny={self.preferred[1]}") + "]"
    
    def collides_with(self, point: tuple[int, int]) -> bool:
        """
        If the layout object collides with the given point, return true
        """
        return _collides_rect(point, self.pos.as_float(), self.rendered.as_float())
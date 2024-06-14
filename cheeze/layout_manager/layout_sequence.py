from .layout_object import LayoutObject 
from .units import LUnit2, LUnit, UNIT
from .alignment import MainAxisAlignment, CrossAxisAlignment
from . import alignment
from .utils import _float0
import textwrap

from functools import partial

class LayoutSequence(LayoutObject):
    """
    LayoutSequence is used for widgets that have items in a sequence
    such as Row, Column, etc...
    This layout object also allows for alignment within it. 
    """
    def __init__(
            self, 
            size: LUnit2 = ("1f", "1f"), *,
            main_axis = "x",
            cross_axis = "y",
            main_axis_align: MainAxisAlignment = MainAxisAlignment.start,
            cross_axis_align: CrossAxisAlignment = CrossAxisAlignment.start,
            children: list[LayoutObject] = None
        ) -> None:
        
        # This gets called before init, because the init methods directly accesses the property pos.
        if children is None:
            self.children = []
        else:
            self.children = children
        self._pos = LUnit2(0, 0)


        super().__init__()
    
        self.dim = size
        self.main_axis = main_axis
        self.cross_axis = cross_axis
        self.main_axis_num = 0 if main_axis == "x" else 1    # The index of the size tuple for the main
        self.cross_axis_num = 0 if cross_axis == "x" else 1  # and cross axis respectively
        self.main_axis_align = main_axis_align
        self.cross_axis_align = cross_axis_align


        assert (main_axis, cross_axis) in (('x', 'y'), ('y', 'x')), "Both main axis and cross axis have to be opposite"

        

    def prefer(self) -> None:
        """
        Automatically set preferred sizes!
        """
        total_size_main = 0
        total_size_cross = 0
        
        # Calculate the minimum preffered size based on the children!
        for x in self.children:
            x.prefer()

            # Get the minimal dimensions of the said items!
            total_size_main += _float0(x.preferred[self.main_axis_num])
            total_size_cross = max(total_size_cross, _float0(x.preferred[self.cross_axis_num]))
        
        if self.main_axis == "x":
            self.preferred = (total_size_main, total_size_cross)
        else:
            self.preferred = (total_size_cross, total_size_main)

        # Check the main axis, if it has absolute value, automatically
        # set the size of this layout's sequence total main axis size to that
        if getattr(self.dim, self.main_axis).unit == UNIT.px:
            if self.main_axis == "x":
                self.preferred = (self.dim.x.val, self.preferred[1])
            else:
                self.preferred = (self.preferred[0], self.dim.y.val)
        
        # Do the same as above for cross axis
        if getattr(self.dim, self.cross_axis).unit == UNIT.px:
            if self.cross_axis == "x":
                self.preferred = (self.dim.x.val, self.preferred[1])
            else:
                self.preferred = (self.preferred[0], self.dim.y.val)

    def render(self, space: LUnit2, viewport: LUnit2, offset: LUnit2) -> None:
        self.rendered = self.dim.abs(space.x.val, space.y.val, viewport)
        space = self.rendered

        # Distribute absolute and percentage spacing across main axis
        main_axis_size = getattr(space, self.main_axis).val
        total_size = 0

        # To get the occupied size for children!
        for x in self.children:
            x_main = getattr(x.dim, self.main_axis)  # Get the LUnit for the child's axis that is main axis for this sequence
            if x_main.unit in (UNIT.px, UNIT.percent, UNIT.vh, UNIT.vw):  # If the unit in question works based on total size
                
                x.render(space, viewport, offset)

                # If the child decides to take more space than that we have
                if total_size + getattr(x.rendered, self.main_axis).val > main_axis_size:
                    x.rendered = getattr(x.rendered, "with_"+self.main_axis)(main_axis_size-total_size)  # Constain the size! by using the respective with_x or with_y method
                total_size = min(total_size + getattr(x.rendered, self.main_axis).val, main_axis_size)  # Make sure, total size does not exceed main axis size


        flex_count = 0
        flex_space_left = main_axis_size-total_size
        # Repeat the above step for flex children!
        for x in self.children:
            x_main = getattr(x.dim, self.main_axis)  
            if x_main.unit in (UNIT.f, ):
                flex_count += x_main.val
        
        # If we do have flex objects
        if flex_count != 0:
            # FIRST PASS to check for minimum size preferences
            # Calculate the value in pixels of 1f
            flex_unit_val = flex_space_left/flex_count

            extensible_objects = []

            # Check for minimum sized preferences and allocate minimum size preferences to those with need!
            for x in self.children:
                x_main = getattr(x.dim, self.main_axis)  
                if x_main.unit in (UNIT.f, ):
                    # If the minimum size is not satisfied, take the minimum size preference as the
                    # object's assigned size
                    if _float0(x.preferred[self.main_axis_num]) > flex_unit_val*x_main.val:
                        x.render(getattr(space, "with_"+self.main_axis)(x.preferred[self.main_axis_num]), viewport, offset)
                        flex_count -= x_main.val  # Remove it from actively assignable flex object count
                        flex_space_left -= x.preferred[self.main_axis_num]  # Remove the assigend space to this object from the rest
                    else:  # The object can be extended
                        extensible_objects.append(x)

        
        # SECOND PASS to distrobute sizes for left over flex objects
        if flex_count > 0:
            flex_unit_val = flex_space_left/flex_count

            # Render each child with given flex object also providing the size for the said flex object
            for x in extensible_objects:  # Extensible objects is the objects that haven't been assigned a size after minimum size filtering
                x_main = getattr(x.dim, self.main_axis)
                x.render(getattr(space, "with_"+self.main_axis)(flex_unit_val*x_main.val), viewport, offset)


        # All of the above was to allocate space! now, to align items with position!

        # Main axis alignment
        main_align = alignment.align(
            getattr(space, self.main_axis).val,
            map(lambda x: getattr(x.rendered, self.main_axis).val, self.children),
            self.main_axis_align
        )

        # Apply the alignment to the positions along with proper offset too
        for align, x in zip(main_align, self.children):
            if self.main_axis == "x":
                x.pos = LUnit2(
                    x.pos.x + offset.x + align,
                    x.pos.y + offset.y + next(alignment.align(space.y.val, (x.rendered.y.val,), self.cross_axis_align)),
                )
            elif self.main_axis == "y":
                x.pos = LUnit2(
                    x.pos.x + offset.x + next(alignment.align(space.x.val, (x.rendered.x.val,), self.cross_axis_align)),
                    x.pos.y + offset.y + align,
                )

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, position: LUnit2):
        for x in self.children:
            x.pos = position + (x.pos - self._pos)  #  Offset the children element positions in a way to work with the new position

        self._pos = position

    def __repr__(self):
        r = ("Row" if self.main_axis == "x" else "Column") + super().__repr__()[:-1] + "\n"
        for x in self.children:
            r += textwrap.indent(repr(x), "  ") + "\n"
        r += "]"
        return r
    
    def layout_representation(self):
        r = ("Row" if self.main_axis == "x" else "Column") + super().layout_representation()[:-1] + "\n"
        for x in self.children:
            r += textwrap.indent(x.layout_representation(), "  ") + "\n"
        r += "]"
        return r
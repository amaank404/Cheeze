from .utils import _collides_rect
from .units import LRect
from typing import Any

class ShaderBounds():
    """
    Shader Boundaries, A Shader shall not draw outside this boundary.
    A shader may contain children. When the collides_with method is run,
    this object returns all the drawable children that need to be redrawn.

    an optional parent parameter may be provided that links the shaderbounds to its parent shader!

    A shader may contain a tree of these ShaderBound objects to make for a more comprehensive draw area checking!

    A ShaderBounds object tree should be maintained at the root by the App
    """
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], *, children: list["ShaderBounds"] = None, drawable: bool, partial_shader: bool, parent) -> None:
        self.pos = pos
        self.size = size

        self.rendered = LRect(pos, size)

        self.drawable = drawable
        self.partial_shader = partial_shader
        self.parent = parent

        if children is None:
            self.children = []
        else:
            self.children = children

    def check_reshade(self, point: tuple[float, float]) -> list[tuple[Any, list[tuple[float, float, float, float]]]]:
        """
        Check what shaderbound objects are to be reshaded.

        If the said shaderbound object is a partial shader, it will be listed as follows
        [ShaderBound, [(x, y, w, h), ...]]

        if the said shaderbound object is not a partial shader, it will be listed as follows
        [ShaderBound, None]

        this function is recursive in nature and will try to visit all shaderbound objects
        """
        reshade = []
        
        if self.rendered.is_zero():
            return reshade

        # A note to the future self, yes, the below covers all the cases
        # and does not miss out on any combination of drawable/partial_shader
        if self.drawable and not self.partial_shader:  # If its a whole shader

            # If the point collides with our whole shader, append itself to reshade queue and also append all drawable children
            if self.rendered.collides_with(point):
                reshade.append((self, None))
                reshade.extend((x, None) for x in self.get_drawable_children())
        
                return reshade

        # If we are a partial shader or we are not drawble
        elif self.partial_shader or not self.drawable:
            if self.rendered.collides_with(point):

                reshadable_regions = ()  # All reshadable regions for this current partial shader

                reshade_temp = []

                for x in self.children:
                    child_reshades = x.check_reshade(point)

                    # If we are a partial shader and drawble, we need to get the partial reshade regions
                    if len(child_reshades) != 0 and self.drawable:
                        for (x, regions) in child_reshades:
                            if regions is None:  # If the said reshade item is not partial in nature
                                reshadable_regions.append(x.rendered.to_float())
                            else:
                                reshadable_regions.extend(regions)

                        # TODO: Make sure that the reshadable region lies inside the actual bounding box of this shader!
                    
                    reshade_temp.extend(child_reshades)

                # If we are a partial shader and drawable with partial regions pending
                if self.drawable and len(reshadable_regions) > 0: 
                    reshade.append((self, reshadable_regions))

                reshade.extend(child_reshades)
        
        return reshade

    def get_drawable_children(self):
        """
        Returns all drawable children recursively
        """
        drawable_children = []
        for x in self.children:
            if x.drawable:  # Add the child itself if its drawable
                drawable_children.append(x)
            drawable_children.extend(x.get_drawable_children())
        return drawable_children

    def add_child(self, child):
        self.children.append(child)
        self.calculate_child_bounds()

    def remove_child(self, child):
        self.children.remove(child)
        self.calculate_child_bounds()

    def calculate_child_bounds(self):
        """
        Get the minimum size bounding box that encompasses all children recursively and self
        """
        for x in self.children:
            x.calculate_child_bounds()
        self.rendered = LRect(self.pos, self.size)
        self.rendered += sum(x.rendered for x in self.children)

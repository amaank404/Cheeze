from .utils import _collides_rect
from .units import LRect
from typing import Any, Self
import textwrap

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
        self.root_shaderbounds = None

        if children is None:
            self.children = []
        else:
            self.children = children

    def check_reshade(self, rect: tuple[float, float, float, float]) -> list[tuple[Any, list[tuple[float, float, float, float]]]]:
        """
        Check what shaderbound objects are to be reshaded.

        If the said shaderbound object is a partial shader, it will be listed as follows
        [ShaderBound, [(x, y, w, h), ...]]

        if the said shaderbound object is not a partial shader, it will be listed as follows
        [ShaderBound, None]

        this function is recursive in nature and will try to visit all shaderbound objects
        """

        if isinstance(rect, tuple):
            assert len(rect) == 4, "Collidable rectangle can only be a 4 float tuple!"
            rect = LRect(rect[:2], rect[2:])
        reshade = []

        # This shader boundaries shading area, no shading should exceed this
        shadable_area_rect = self.get_shadable_rect()
        
        if self.rendered.is_zero():
            return reshade

        # A note to the future self, yes, the below covers all the cases
        # and does not miss out on any combination of drawable/partial_shader
        if self.drawable and not self.partial_shader:  # If its a whole shader
            
            # If the point collides with our whole shader, append itself to reshade queue and also append all drawable children
            if self.rendered.collides_withr(rect):
                reshade.append((self, None))
                reshade.extend((x, None) for x in self.get_drawable_children())

                return reshade

        # If we are a partial shader or we are not drawble
        elif self.partial_shader or not self.drawable:
            if self.rendered.collides_withr(rect):
                reshadable_regions = set()  # All reshadable regions for this current partial shader

                reshade_temp = []

                # If we are a partial shader and drawable, then extend the area of the rectangle clipped to our render region
                if self.drawable:
                    self_reshade_region = rect.clip(LRect(self.pos, self.size))
                    if not self_reshade_region.is_zero():
                        reshadable_regions.add(self_reshade_region.as_float())

                for x in self.children:
                    child_reshades = x.check_reshade(rect)

                    # If we are a partial shader and drawble, we need to get the partial reshade regions
                    if len(child_reshades) != 0 and self.drawable:
                        for (x, regions) in child_reshades:
                            if regions is None:  # If the said reshade item is not partial in nature
                                reshadable_regions.add(x.rendered.clip(shadable_area_rect).as_float())
                            else:
                                for y in reshadable_regions:
                                    reshadable_regions.add(shadable_area_rect.clip(LRect(y[:2], y[2:])).as_float())
                    
                    reshade_temp.extend(child_reshades)

                # If we are a partial shader and drawable with partial regions pending
                if self.drawable and len(reshadable_regions) > 0: 
                    # Optimization: Check if the reshadable region is more or equal to self!
                    # In case the area covered by reshadables is more, we are doing extra work and we should instead
                    # just do the whole shading region!
                    total_reshadable_regions_size = 0
                    for x in reshadable_regions:
                        total_reshadable_regions_size += x[2] * x[3]

                    # if the total reshadable is more than 98% of the self size. 98% was choosen to account for floating point
                    # inaccuracies.
                    if total_reshadable_regions_size >= 0.98 * shadable_area_rect.size[0] * shadable_area_rect.size[1]:
                        reshade.append((self, None))
                    else:
                        reshade.append((self, list(reshadable_regions)))

                reshade.extend(reshade_temp)
        
        return reshade

    def get_drawable_children(self) -> list["ShaderBounds"]:
        """
        Returns all drawable children recursively
        """
        drawable_children = []
        for x in self.children:
            if x.drawable:  # Add the child itself if its drawable
                drawable_children.append(x)
            drawable_children.extend(x.get_drawable_children())
        return drawable_children
    
    def get_children(self) -> list["ShaderBounds"]:
        """
        Returns all children recursively
        """
        children = []
        for x in self.children:
            children.append(x)
            children.extend(x.get_drawable_children())
        return children

    def add_child(self, child: Self):
        self.children.append(child)
        self.calculate_child_bounds()
        child.set_root_shader_bounds(self.root_shaderbounds)

    def remove_child(self, child: Self):
        self.children.remove(child)
        self.calculate_child_bounds()
        child.set_root_shader_bounds(self.root_shaderbounds)

    def calculate_child_bounds(self):
        """
        Get the minimum size bounding box that encompasses all children recursively and self
        """
        for x in self.children:
            x.calculate_child_bounds()
        self.rendered = LRect(self.pos, self.size)
        for x in self.children:
            self.rendered += x.rendered

    def set_root_shader_bounds(self, root):
        self.root_shaderbounds = root
        for x in self.children:
            x.set_root_shader_bounds(root)

    def __repr__(self) -> str:
        if self.children:
            r = f"ShaderBounds(init: {LRect(self.pos, self.size)}, real: {self.rendered}\n"
            for x in self.children:
                r += textwrap.indent(repr(x), "  ")+"\n"
            r += ")"
            return r
        else:
            return f"ShaderBounds(init: {LRect(self.pos, self.size)}, real: {self.rendered})"

    def get_shadable_rect(self):
        """
        return the shadable region as a rect
        """
        return LRect(self.pos, self.size)
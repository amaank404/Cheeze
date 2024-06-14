import abc
from ..layout_manager.shader_bounds import ShaderBounds
from ..layout_manager.layout_object import LayoutObject

class ShaderObject(abc.ABC):
    """
    A ShaderObject defines how to draw a certain widget.

    Shader objects can also be partial in nature which allows for drawing parts of the graphic onto
    the display buffer. Only one shader can be attached to a widget. Each shader has a
    accompanying shader boundary. Shader boundary can contain children shader boundary.

    Widgets are required to add children shader boundaries to their own shader's boundary or else
    a reshade won't occur!
    """
    def __init__(self, shadername: str, *, partial_shader: bool) -> None:
        self.shadername = shadername
        self.partial_shader = partial_shader  # Determines if the shader allows partial redraws
        self.shader_bounds = None
        self.build_context = None

    def set_build_context(self, buildcontext):
        self.build_context = buildcontext

    def shade(self, *, regions: list[tuple[float, float, float, float]] = None, **kwargs) -> None:
        """
        Shade on the given surface with the given keyword arguments
        
        if the shader is a partial shader, it is also provided with regions to shade in (x, y, w, h) format!

        No shader must exceed their shading boundaries. If they do, it will lead to
        graphical glitches that are hard to track!
        """
        pass

    def calculate_shader_boundary(self, layout_object: LayoutObject):
        """
        Calculate the shader boundary object for this shader
        """
        self.shader_bounds = ShaderBounds(layout_object.pos.as_float(), layout_object.rendered.as_float(), drawable=False, partial_shader=False, parent=self)

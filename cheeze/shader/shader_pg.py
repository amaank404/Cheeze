import pygame as pg

from ..layout_manager.layout_object import LayoutObject
from ..layout_manager.shader_bounds import ShaderBounds
from .shader_object import ShaderObject

class ShaderPygame(ShaderObject):
    def __init__(self, shadername: str) -> None:
        super().__init__(shadername)

    def shade(self, *, regions: list[tuple[float, float, float, float]] = None, surf: pg.Surface, **kwargs):
        """
        This is the default shader method for ShaderPygame, please implement it!
        """
        if regions is None:
            regions = [self.shader_bounds.rendered.as_float()]
        for x in regions:
            surf.fill((255, 255, 255), pg.Rect(x))

    def calculate_shader_boundary(self, layout_object: LayoutObject):
        self.shader_bounds = ShaderBounds(layout_object.pos.as_float(), layout_object.rendered.as_float(), drawable=False, partial_shader=False, parent=self)
        self.shader_bounds.calculate_child_bounds()
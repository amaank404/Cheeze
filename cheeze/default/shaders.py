from ..shader.shader_pg import ShaderPygame
from ..shader import *
import pygame as pg


class LabelShader(ShaderPygame):
    def __init__(self, *, text: str, style: str = "normal") -> None:
        super().__init__("label")
        self.style = style
        self.text = text
    
    def set_build_context(self, buildcontext):
        super().set_build_context(buildcontext)
        self.set_text(self.text)
    
    def set_text(self, text):
        self.text = text
        self.label_surface = self.build_context.text_theme.get_style_font(self.style).render(self.text, True, self.build_context.text_theme.get_style().color)
        

def get_default_shaderpack():
    return ShaderPack(
        "default",
        LabelShader
    )

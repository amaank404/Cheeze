from .text_theme import TextTheme
from ..shader.shader_pack import ShaderPack
from .color_theme import ColorTheme

class BuildContext:
    def __init__(self, *, shader_pack: ShaderPack, text_theme: TextTheme, color_theme: ColorTheme, scaling: float) -> None:
        self.scaling = scaling
        self.shader_pack = shader_pack
        self.text_theme = text_theme
        self.color_theme = color_theme

        # Set the build context
        for v in self.shader_pack.shaders.items():
            v.set_build_context(self)
        self.text_theme.set_build_context(self)
        self.color_theme.set_build_context(self)
        
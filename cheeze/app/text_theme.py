from .font_loader import FontLoader
import dataclasses

@dataclasses.dataclass(kw_only=True, frozen=True, unsafe_hash=True)
class TextStyle:
    """
    A text style object
    """
    font: str
    size: int
    bold: bool = False
    italic: bool = False
    color: str

    def with_changes(self, **kwargs):
        args = {
            "font": self.font,
            "size": self.size,
            "bold": self.bold,
            "italic": self.italic,
        }

        args.update(kwargs)
        return TextStyle(**args)

class TextTheme:
    """
    Text theme for the app. Requires a font loader object
    """
    def __init__(self, *, font_loader: FontLoader, **kwargs: dict[str, TextStyle]) -> None:
        self.font_loader = font_loader
        self.font_cache = {}
        self.styles: dict[str, TextStyle] = kwargs
        self.build_context = None

    def get_style(self, style: str):
        return self.styles[style]
    
    def get_style_font(self, style: str):
        styleobj = self.styles[style]

        # Return the cached font
        if style in self.font_cache:
            return self.font_cache[style]
        
        # Load the font from disk
        font = self.font_loader.get_font(
            font_name=styleobj.font,
            font_size=styleobj.size,
            font_bold=styleobj.bold,
            font_italic=styleobj.italic
        )

        self.font_cache[style] = font
        return font
    
    def with_changes(self, **kwargs: dict[str, TextStyle]):
        new_styles = self.styles.copy()
        new_styles.update(kwargs)

        return TextTheme(font_loader=self.font_loader, **new_styles)
    
    def set_build_context(self, build_context):
        self.font_loader.set_build_context(build_context)
        self.build_context = build_context
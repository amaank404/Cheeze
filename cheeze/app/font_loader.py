from typing import Any
import abc

class FontLoader(abc.ABC):
    def __init__(self) -> None:
        self.build_context = None

    def get_font(self, *, font_name: str, font_size: int, font_bold: bool, font_italic: bool, **kwargs) -> Any:
        raise TypeError(f"class {self.__class__.__name__} does not provide a loading mechanism")
    
    def set_build_context(self, build_context):
        self.build_context = build_context
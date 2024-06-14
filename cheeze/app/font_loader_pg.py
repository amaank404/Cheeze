from .font_loader import FontLoader
import pygame
from pathlib import Path

class FontLoaderPygame(FontLoader):
    def __init__(self, search_directory: Path) -> None:
        self.search_directory = Path(search_directory)

    def get_font(self, *, font_name: str, font_size: int, font_bold: bool, font_italic: bool) -> pygame.font.FontType:
        if font_name in pygame.font.get_fonts():
            return pygame.font.SysFont(font_name, int(font_size*self.build_context.scaling), font_bold, font_italic)
        return pygame.font.Font(self.search_directory/font_name+".ttf", font_size, font_bold, font_italic)
        
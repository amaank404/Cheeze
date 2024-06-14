from ..app import TextStyle, TextTheme
from ..app.font_loader_pg import FontLoaderPygame
from pathlib import Path

def get_default_text_theme():
    return TextTheme(
        font_loader=FontLoaderPygame(Path(__file__).parent/"fonts"),
        normal = TextStyle(
            font="Arial",
            size=12,
            color="text",
        ),
        heading = TextStyle(
            font="Arial",
            size=24,
            color="text",
        )
    )
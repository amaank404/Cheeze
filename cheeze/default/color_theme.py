from ..app.color_theme import ColorTheme

def get_default_color_theme():
    return ColorTheme(
        background = (100, 100, 100),
        text = (255, 255, 255)
    )
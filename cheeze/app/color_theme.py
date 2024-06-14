class ColorTheme:
    """
    Color Theme for the app
    """
    def __init__(
            self, **kwargs: dict[str, tuple]
        ) -> None:
        self._colors = {
            **kwargs
        }

        self.build_context = None

    def __getitem__(self, key: str):
        return self._colors[key]
    
    def with_changes(self, **kwargs: dict[str, tuple]):
        new_colors = self._colors.copy()
        new_colors.update(kwargs)

        return ColorTheme(**new_colors)
    
    def set_build_context(self, build_context):
        self.build_context = build_context
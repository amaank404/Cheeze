from .animation_object import AnimationObject
from .result import AnimationResult

class AnimationFade(AnimationObject):
    def __init__(self, *, reverse: bool = False, duration: float = 1) -> None:
        super().__init__(reverse=reverse)

    def next_frame(self, dt: float):
        return AnimationResult()
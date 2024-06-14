import abc
from .result import AnimationResult

class AnimationObject(abc.ABC):
    """
    An animation object keeps the state of the animation inside it.
    with every advancement in the animation, it returns a AnimationResult object.
    AnimationResult object contains the shader to be used
    """
    reversable = False
    def __init__(self, *, reverse: bool = False) -> None:
        self.reverse = reverse
        self.build_context = None

    def next_frame(self, dt: float) -> AnimationResult:
        """
        Returns an AnimationResult object, if None is returned, animation
        object's lifecycle has ended and it can be destroyed.
        """
        pass

    def previous_frame(self, dt: float) -> AnimationResult:
        """
        Same as next_frame but called only if reverse is set to True.
        Returning None means the animation object's lifecycle has ended
        and it can be destroyed.
        """
        if not self.reversable():
            raise TypeError("This animation is not reversible")

    @classmethod
    def reversable(cls):
        """
        Tells if the animation class allows reversal
        """
        return cls.reversable

    def set_reverse(self, reverse: bool):
        """
        Reverse the animation!
        """
        if self.reversable():
            self.reverse = reverse
        else:
            raise TypeError("This animation is not reversible in nature!")

    def set_build_context(self, build_context):
        self.build_context = build_context
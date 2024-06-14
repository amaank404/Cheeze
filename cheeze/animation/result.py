import dataclasses
from .rotation import RotationAxis

@dataclasses.dataclass(kw_only=True)
class AnimationResult:
    """
    An implementation independent AnimationResult object
    which contains required transformations on an object.

    keep in mind that these values are not scaled according to buildcontext!
    scaling of these values is done by animation shader!

    ## translate
    Move the draw position relative to initial draw position
    by given number of pixels. pixels provided here are unscaled.

    ## rotate
    Rotate the given draw surface by certain amount of radians

    ## rotate_axis
    What point of the surface stays in the fixed position when performing rotate.
    As of now, only the centeral axis is available for rotatation

    ## opacity
    Ranges 0 (transparent) to 1 (opaque)

    ## scale
    Scaling of pixels on individual axis x and y provided as a tuple

    for eg, scaling by two on the x axis only = (2.0, 1.0)

    ## smoothscale
    Should the scaling be smooth in nature
    """
    translate: tuple[float, float] = None
    rotate: float = None
    rotate_axis: RotationAxis = RotationAxis.CENTER
    opacity: float = None  # Ranges 0 to 1
    scale: tuple[float, float] = None
    smoothscale: bool = True
    
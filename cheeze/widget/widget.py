import abc
from ..app.build_context import BuildContext
from ..shader.shader_object import ShaderObject
from ..event.event_object import Event
from ..animation.animation_object import AnimationObject, AnimationResult
from ..layout_manager.layout_object import LayoutObject

class Widget(abc.ABC):
    """
    An abstract widget class
    """
    def __init__(self, shader: str) -> None:
        self._shader_name = shader
        self.shader: ShaderObject = None
        self.layout_object: LayoutObject = None
        self.animation: list[AnimationObject] = []

    def set_build_context(self, build_context: BuildContext):
        """
        This method should only be run once at the start of the app or initialization
        of a new widget.
        """
        self.build_context = build_context
        self.shader_cls = build_context.shader_pack.shaders[self._shader_name]
        for x in self.animation:
            x.set_build_context(build_context)
        if self.shader is not None:
            self.shader.set_build_context(build_context)
        self.init()
            
    def init(self):
        """
        set_build_context method automatically runs this method and sets a self.shader_cls
        shader_cls is the Shader associated with this object which needs to be initialized.

        This method should be overridden to do all the post buildcontext initialization!
        """
        self.shader = self.shader_cls()

    def event(self, evt: Event):
        """
        Handle events given to this object!
        """
        pass

    def render_frame(self, dt: float):
        """
        Not meant to be overridden, but this is the render pipeline to incorporate both
        animation and shader!

        dt is time since last frame in seconds
        """

        animationresult = None       
        while len(self.animation) > 0:  # Keep doing this as long as there are animations and we don't have a proper animation result object
            animationresult = self.animation[0].next_frame()
            if animationresult is None:
                self.animation.pop(0)
            else:
                break
        
        if animationresult is None:  # Direct shading
            self.shader.shade()
            
    
    def add_animation(self, animation: AnimationObject):
        self.animation.append(animation)
        animation.set_build_context(self.build_context)
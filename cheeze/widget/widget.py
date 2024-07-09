import abc
from ..app.build_context import BuildContext
from ..shader.shader_object import ShaderObject
from ..event.event_object import Event
from ..animation.animation_object import AnimationObject, AnimationResult
from ..layout_manager.layout_object import LayoutObject
from typing import Union, Self
import enum

class WidgetState(enum.Enum):
    DYNAMIC = 0
    STATIC = 1

class Widget(abc.ABC):
    """
    An abstract widget class
    """
    def __init__(self, shader: str) -> None:
        self._shader_name = shader
        self.shader: ShaderObject = None
        self.layout_object: LayoutObject = None
        self.reshade_: bool = False
        self.state_: WidgetState = WidgetState.STATIC
        self.animation_result_ = None
        self.animation: list[AnimationObject] = []
        self.child: Union[list[Self], Self, None] = None

    def set_build_context(self, build_context: BuildContext):
        """
        This method should only be run once at the start of the app or initialization
        of a new widget.
        """
        self.build_context = build_context
        self.shader_cls = build_context.shader_pack.shaders[self._shader_name]

        # Set animation build context
        for x in self.animation:
            x.set_build_context(build_context)

        # Set shader build context
        if self.shader is not None:
            self.shader.set_build_context(build_context)

        # Set children Buildcontext
        if self.child is None:
            pass
        elif isinstance(self.child, list):
            for x in self.child:
                x.set_build_context(build_context)
        elif isinstance(self.child, Widget):
            self.child.set_build_context(build_context)

        self.init()
            
    def init(self):
        """
        set_build_context method automatically runs this method and sets a self.shader_cls
        shader_cls is the Shader associated with this object which needs to be initialized.

        This method should be overridden to do all the post buildcontext initialization!
        and this method should call this method as super().init() in the overriden
        function.
        """
        # self.shader = self.shader_cls()

        if self.child is None:
            pass
        elif isinstance(self.child, list):
            for x in self.child:
                x.init()
        elif isinstance(self.child, Widget):
            self.child.init()

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
            animationresult = self.animation[0].next_frame(dt)
            if animationresult is None:
                self.animation.pop(0)
            else:
                break
        
        self.animation_result_ = animationresult

        # Do children animations
        if self.child is None:
            pass
        elif isinstance(self.child, list):
            for x in self.child:
                x.render_frame(dt)
        elif isinstance(self.child, Widget):
            self.child.render_frame(dt)
    
    def add_animation(self, animation: AnimationObject):
        self.animation.append(animation)
        animation.set_build_context(self.build_context)

    def queue_reshade(self):
        self.reshade_ = True

    
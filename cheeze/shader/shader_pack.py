from .shader_object import ShaderObject

class ShaderPack:
    """
    A collection of shaders. Has a shaderpack_name
    """
    def __init__(self, shaderpack_name: str, *args: list[ShaderObject]) -> None:
        self.name = shaderpack_name
        self.shaders = {}
        for x in args:
            self.shaders[x.name] = x
        self.build_context = None

    def set_build_context(self, build_context):
        self.build_context = build_context
        for x in self.shaders.items():
            x.set_build_context(build_context)
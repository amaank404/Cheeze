import pygame
from .build_context import BuildContext
from ..widget.widget import Widget

class AppPygame:
    def __init__(self, initial_size: tuple[int, int] = (700, 500), *, scaling: float = 1, build_context: BuildContext, fps: int = 60, child: Widget) -> None:
        pygame.init()
        self.initial_size = initial_size
        self.scaling = scaling
        self.build_context = build_context
        self.running = False
        self.fps = fps
        self.shader_bounds_root = None
        self.clock = pygame.time.Clock()
        self.child = child
        self.child.set_build_context(build_context)
        self.static_surface: pygame.Surface = None

    def run(self):
        """
        Run the app with pygame backend
        """

        # Initialize surfaces
        self.surf = pygame.display.set_mode(self.initial_size)
        self.static_surface = pygame.Surface(self.initial_size)
        self.dynamic_surface = pygame.Surface(self.initial_size)
        
        self.running = True
        self.clock = pygame.time.Clock()

        while self.running:
            dt = self.clock.tick(self.fps)/1000  # Delta time
            for evt in pygame.event.get():
                match evt.type:
                    case pygame.QUIT:
                        self.running = False

            # Setup all the animation frames
            self.child.render_frame(dt)

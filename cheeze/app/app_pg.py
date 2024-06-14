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
    
    def run(self):
        """
        Run the app with pygame backend
        """
        self.surf = pygame.display.set_mode(self.initial_size)
        self.running = True
        self.clock = pygame.time.Clock()
        while self.running:
            for evt in pygame.event.get():
                match evt.type:
                    case pygame.QUIT:
                        self.running = False
        
        dt = self.clock.tick(self.fps)/1000  # Delta time

        
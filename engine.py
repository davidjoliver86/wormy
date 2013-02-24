import pygame

WIDTH = 800
HEIGHT = 600

class Colors(object):
    RED = (255,0,0)
    GREEN = (0,255,0)
    WHITE = (255,255,255)
    BLACK = (0,0,0)

class Engine(object):
    _surface = None

    def __init__(self, **kw):
        title = kw.get('title', 'Untitled')
        fps = kw.get('fps', 15)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.font = pygame.font.SysFont(None, 20)

    @property
    def surface(self):
        if not self._surface:
            self._surface = pygame.display.set_mode((WIDTH, HEIGHT))
        return self._surface


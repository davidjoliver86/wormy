import sys
import pygame
import random
from engine import Engine, Colors

BOXSIZE = 20
LENGTH = 800
HEIGHT = 600
CELL_LENGTH = LENGTH / BOXSIZE
CELL_HEIGHT = HEIGHT / BOXSIZE
DIRECTION_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)


class Box(Engine):
    def draw(self, *a, **kw):
        raise NotImplementedError

    def draw_rect(self, x, y, color):
        rect = pygame.Rect(x*BOXSIZE, y*BOXSIZE, BOXSIZE, BOXSIZE)
        pygame.draw.rect(self.surface, color, rect)


class Apple(Box):
    DEFAULT_POINT_VALUE = 1000
    color = Colors.RED

    def __init__(self):
        self.randomize_pos()
        self.point_value = self.DEFAULT_POINT_VALUE

    def randomize_pos(self):
        self.x = random.randint(0,CELL_LENGTH-1)
        self.y = random.randint(0,CELL_HEIGHT-1)

    def draw(self):
        self.draw_rect(self.x, self.y, self.color)

    def update_score(self, reset=False):
        if reset:
            points_to_add, self.point_value = self.point_value, self.DEFAULT_POINT_VALUE
            return points_to_add
        self.point_value = self.point_value * 995 / 1000


class Worm(Box):
    UP = (0,-1)
    LEFT = (-1,0)
    RIGHT = (1,0)
    DOWN = (0,1)
    color = Colors.GREEN

    def __init__(self):
        self.size = 5
        self.x = [CELL_LENGTH/2]
        self.y = [CELL_HEIGHT/2]
        self.direction = self.RIGHT

    def move(self):
        x, y = self.direction
        self.x.insert(0, self.x[0] + x)
        self.y.insert(0, self.y[0] + y)
        if len(self.x) > self.size:
            self.x.pop()
        if len(self.y) > self.size:
            self.y.pop()

    def grow(self):
        self.size += 2

    def draw(self):
        for x, y in zip(self.x, self.y):
            self.draw_rect(x, y, self.color)

    def get_segments(self):
        return (self.x[0], self.y[0]), zip(self.x[1:], self.y[1:])

    def set_direction(self, key):
        if key == pygame.K_UP and self.direction != self.DOWN:
            self.direction = self.UP
        if key == pygame.K_DOWN and self.direction != self.UP:
            self.direction = self.DOWN
        if key == pygame.K_LEFT and self.direction != self.RIGHT:
            self.direction = self.LEFT
        if key == pygame.K_RIGHT and self.direction != self.LEFT:
            self.direction = self.RIGHT


def play(engine):
    surface = engine.surface
    worm = Worm()
    apple = Apple()
    score = 0

    while True:
        # key handling
        for event in pygame.event.get():
            if event.key in DIRECTION_KEYS:
                worm.set_direction(event.key)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # move worm; update apple score
        worm.move()
        apple.update_score()

        # collision detection
        if apple.x == worm.x[0] and apple.y == worm.y[0]:
            worm.grow()
            apple.randomize_pos()
            score += apple.update_score(True)
        head, body = worm.get_segments()
        if head in body:
            game_over(engine, 'You ate yourself!')
        if head[0] < 0 or head[1] < 0 or head[0] >= CELL_LENGTH or head[1] >= CELL_HEIGHT:
            game_over(engine, 'You fell off!')

        # draw stuff
        draw(surface, worm, apple)
        draw_score(engine, score)
        pygame.display.update()
        engine.clock.tick(engine.fps)

def game_over(engine, message):
    gameover = engine.font.render("GAME OVER - {0}".format(message), 1, Colors.RED)
    playagain = engine.font.render("Press space to play again or ESC to quit.", 1, Colors.WHITE)
    engine.surface.blit(gameover, (10, 10))
    engine.surface.blit(playagain, (10, 30))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                play(engine)

def draw(surface, *objects):
    surface.fill((0,0,0))
    for obj in objects:
        obj.draw()

def draw_score(engine, score):
    off_x, off_y = (10,10)
    surf = engine.font.render("Score: {0}".format(score), 1, Colors.WHITE)
    x, y = (engine.surface.get_width() - surf.get_width() - off_x), off_y
    engine.surface.blit(surf, (x,y))


if __name__ == '__main__':
    try:
        assert (not LENGTH % BOXSIZE) and (not HEIGHT % BOXSIZE)
    except AssertionError:
        print 'uneven box size'
        sys.exit(1)
    pygame.init()
    pygame.event.set_allowed(None)
    pygame.event.set_allowed(2)
    play(Engine(title="It's wormylicious!"))

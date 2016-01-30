import pygame
import math

# some simple vector helper functions, stolen from http://stackoverflow.com/a/4114962/142637
def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]

def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]    

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def normalize(v):
    vmag = magnitude(v)
    return [ v[i]/vmag  for i in range(len(v)) ]

class Ship(object):
    def __init__(self):
        self.x, self.y = (0, 0)
        self.set_target((0, 0))
        self.speed = 5.0

    @property
    def pos(self):
        return self.x, self.y

    # for drawing, we need the position as tuple of ints
    # so lets create a helper property
    @property
    def int_pos(self):
        return map(int, self.pos)

    @property
    def target(self):
        return self.t_x, self.t_y

    @property
    def int_target(self):
        return map(int, self.target)   

    def set_target(self, pos):
        self.t_x, self.t_y = pos

    def update(self):
        # if we won't move, don't calculate new vectors
        if self.int_pos == self.int_target:
            return 

        target_vector = sub(self.target, self.pos) 

        # a threshold to stop moving if the distance is to small.
        # it prevents a 'flickering' between two points
        if magnitude(target_vector) < 2: 
            return

        # apply the ship's speed to the vector
        move_vector = [c * self.speed for c in normalize(target_vector)]

        # update position
        self.x, self.y = add(self.pos, move_vector)

    def draw(self, s):
        pygame.draw.circle(s, (255, 0 ,0), self.int_pos, 2)

pygame.init()
quit = False
s = pygame.display.set_mode((300, 300))
c = pygame.time.Clock()
ship = Ship()

while not quit:
    quit = pygame.event.get(pygame.QUIT)
    if pygame.event.get(pygame.MOUSEBUTTONDOWN):
        ship.set_target(pygame.mouse.get_pos())
    pygame.event.poll()
    ship.update()
    s.fill((0, 0, 255))
    ship.draw(s)
    pygame.display.flip()
    c.tick(60)
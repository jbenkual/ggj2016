import pygame
import math
import random
import os
import sys

screenWidth = 800
screenHeight = 800
numCultists = 0
lineMaximum = 15

door1 = (200,400)
door2 = (600,400)
door3 = (400,500)
POD = (600,135)
PODSize = (120,80)
doorSize = (20,20)
random.seed()

score = [20,0,0,0,0]
# 0: Number of Colored in Pit
# 1: # of Reds
# 2: # of Greens
# 3: # of Blues
# 4: # of Browns

t = 500 #miliseconds

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

class Cultist(object):
    def __init__(self):
        global numCultists
        self.listIndex = numCultists
        numCultists = numCultists + 1
        self.x, self.y = (screenWidth / 2, 0)
        self.update_target()
        self.speed = 10.0
        self.assigned = False
        self.destination = 0
        

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

    def update_target(self):
        offset = (20 * self.listIndex)
        self.set_target((round(screenWidth / 2), round(300 - offset)))

    def set_target(self, pos):
        #print pos
        self.t_x, self.t_y = pos

    def set_color(self, red, green, blue):
        self.r = red
        self.g = green
        self.b = blue

    def update(self):
        # if we won't move, don't calculate new vectors
        if abs(self.int_pos[0] - self.int_target[0]) < 2 and abs(self.int_pos[1] - self.int_target[1]) < 2 :
            if(self.assigned):
                if(self.team == 4 and self.destination >= 1 and self.destination <= 3):
                    score[self.team] += 1
                elif(self.team < 4 and self.destination == 4):
                    score[0] -= 1
                elif(self.team == self.destination and self.team !=4): # add point & remove if correct color & gate
                    score[self.team] += 1
                return True # kill if wrong color at gate
            return False # arrived at destination, but not at a gate yet

        target_vector = sub(self.target, self.pos) 

        # a threshold to stop moving if the distance is to small.
        # it prevents a 'flickering' between two points
        if magnitude(target_vector) < 10: # slow down when close to destination
            self.speed = 1

        if magnitude(target_vector) < 1: 
            return False

        # apply the ship's speed to the vector
        move_vector = [c * self.speed for c in normalize(target_vector)]

        # Add side to side movement when "walking"


        # update position
        self.x, self.y = add(self.pos, move_vector)
        return False

    def draw(self, s):
        pygame.draw.circle(s, (self.r, self.g, self.b), self.int_pos, 5)


def addCultist() :
    if(numCultists >= lineMaximum):
        return
    cultist = Cultist()
    cultists.append(cultist)
    team = random.randint(1,5)
    cultist.team = team
    if(team == 1):
        cultist.set_color(255,0,0)
    elif(team == 2):
        cultist.set_color(0,102,0)
    elif(team == 3):
        cultist.set_color(0,0,255)
    else:
        cultist.set_color(155,95,55)
        cultist.team = 4

def moveToRoom(num):
    global numCultists
    if(numCultists <= 0): #exit if list is empty
        return


    cultists[0].assigned = True
    cultists[0].destination = num

    if(num == 666):
        cultists[0].set_target(POD)
        cultists[0].destination = 4
    if(num == 1):
        cultists[0].set_target(door1)
    if(num == 2):
        cultists[0].set_target(door2)
    if(num == 3):
        cultists[0].set_target(door3)

    assigned.append(cultists.pop(0))
    numCultists = numCultists - 1

    for i in range(0, numCultists):
        cultists[i].listIndex = i
        cultists[i].update_target()




pygame.init()
quit = False
s = pygame.display.set_mode((800, 600))
c = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 15)

background = pygame.image.load('overall.png')
gate_1 = pygame.image.load('gate-1.png')
gate_2 = pygame.image.load('gate-2.png')
gate_3 = pygame.image.load('gate-3.png')

cultists = [] # create array for cultists
assigned = [] # cultists going somewhere



CREATE_CULTIST = pygame.USEREVENT+1
pygame.time.set_timer(CREATE_CULTIST, t)

while not quit:
    quit = pygame.event.get(pygame.QUIT)
    #if pygame.event.get(pygame.MOUSEBUTTONDOWN):
        #addCultist()
        #cultist.set_target(pygame.mouse.get_pos())

    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            #print e.key
            if(e.key == 276): # right arrow
                moveToRoom(1)
            if(e.key == 275): # down arrow
                moveToRoom(2)
            if(e.key == 274): # left arrow
                moveToRoom(3)
            if(e.key == 273): # up arrow
                moveToRoom(666)
        if e.type == CREATE_CULTIST:
            t = t - 1

            if t < 250:
                t = 50
            pygame.time.set_timer(CREATE_CULTIST, t)
            addCultist()


    pygame.event.poll()
    for i in cultists:
        i.update()

    count = len(assigned)
    while (count > 0) :
        count = count - 1
        remove = assigned[count].update()
        if(remove):
            assigned.pop(count)

    s.fill((225,225,225))
    s.blit(background, (0,0))
    s.blit(gate_1, (door1))
    s.blit(gate_3, (door2))
    s.blit(gate_2, (door3))

    for i in range(0, numCultists):
        cultists[i].draw(s)

    for a in assigned:
        a.draw(s)

    pygame.draw.rect(s, (255, 0 ,0), (door1[0]-doorSize[0]/2, door1[1]-doorSize[1]/2, doorSize[0], doorSize[1]), 5)
    pygame.draw.rect(s, (0, 102 ,0), (door2[0]-doorSize[0]/2, door2[1]-doorSize[1]/2, doorSize[0], doorSize[1]), 5)
    pygame.draw.rect(s, (0, 0 ,255), (door3[0]-doorSize[0]/2, door3[1]-doorSize[1]/2, doorSize[0], doorSize[1]), 5)
    pygame.draw.rect(s, (0, 0 ,0), (POD[0]-PODSize[0]/2, POD[1]-PODSize[1]/2, PODSize[0], PODSize[1]), 5)

    #Jobraldon

    label = myfont.render("Lives " + str(score[0]), 1, (255,150,0))
    s.blit(label, (100, 60))
    label = myfont.render("Red Cultists " + str(score[1]), 1, (255,0,0))
    s.blit(label, (100, 80))
    label = myfont.render("Green Cultists " + str(score[2]), 1, (0,102,0))
    s.blit(label, (100, 100))
    label = myfont.render("Blue Cultists " + str(score[3]), 1, (0,0,255))
    s.blit(label, (100, 120))
    label = myfont.render("Infiltrators " + str(score[4]), 1, (155,95,55))
    s.blit(label, (100, 140))

    pygame.display.flip() # RENDER THE SCREEN
    c.tick(60) # END OF FRAME CALCULATIONS
    
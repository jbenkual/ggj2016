import pygame
import math
import random
import os
import sys

screenWidth = 800
screenHeight = 800
numCultists = 0
lineMaximum = 15
victoryAmount = 10

door1 = (170,404)
door2 = (645,404)
door3 = (400,530)
POD = (600,135)
PODSize = (120,80)
doorSize = (20,20)
random.seed()

score = [20,0,0,0,0]
ritual1 = False
ritual2 = False
ritual3 = False
# 0: Number of Colored in Pit
# 1: # of Reds
# 2: # of Greens
# 3: # of Blues
# 4: # of Browns

t = 600 #miliseconds

def checkRitual():
    global ritual1
    global ritual2
    global ritual3
    if(score[1] >= victoryAmount and ritual1 == False):
        ritual1 = True
        playMusic(1)
    elif(score[2] >= victoryAmount and ritual2 == False):
        ritual2 = True
        playMusic(2)
    elif(score[3] >= victoryAmount and ritual3 == False):
        ritual3 = True
        playMusic(3)

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


class Blood(object):
    def __init__(self):
        self.x = 570 + random.randint(1,70)
        self.y = 120 + random.randint(1,55)

    @property
    def pos(self):
        return self.x, self.y

    # for drawing, we need the position as tuple of ints
    # so lets create a helper property
    @property
    def int_pos(self):
        return map(int, self.pos)

    def set_color(self, red, green, blue):
        self.r = red
        self.g = green
        self.b = blue
    def draw(self, s):
        pygame.draw.circle(s, (self.r, self.g, self.b), self.int_pos, 1)

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
                elif(self.team < 4 and self.destination >= 1 and score[self.destination] > 0) :
                    score[self.destination] -= 1
                if self.destination == 4:
                    bld = Blood()
                    bld.set_color(self.r, self.g, self.b)
                    bloodList.append(bld)

                checkRitual()
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
        for i in range(1,10):
            room = random.randint(1,3)
            moveToRoom(room)
        return
    cultist = Cultist()
    cultists.append(cultist)
    team = random.randint(1,4)
    cultist.team = team
    if(team == 1 and score[team] < victoryAmount):
        cultist.set_color(255,0,0)
    elif(team == 2 and score[team] < victoryAmount):
        cultist.set_color(0,102,0)
    elif(team == 3 and score[team] < victoryAmount):
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

    if(num == 666 or num == 4):
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
pygame.mixer.init()

#load sounds


quit = False
s = pygame.display.set_mode((800, 600))
c = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 15)

musicPlaying = True;
gamePaused = True;
background = pygame.image.load('overall.png')
gate_1 = pygame.image.load('gate-1.png')
gate_2 = pygame.image.load('gate-2.png')
gate_3 = pygame.image.load('gate-3.png')
goblin_down = pygame.image.load('goblin-down.png')
goblin_right = pygame.image.load('goblin-right.png')
goblin_left = pygame.image.load('goblin-left.png')
monster = pygame.image.load('img/monster.jpg')
cultists = [] # create array for cultists
assigned = [] # cultists going somewhere
bloodList = []

CREATE_CULTIST = pygame.USEREVENT+1
STOP_MUSIC = pygame.USEREVENT+2
pygame.time.set_timer(CREATE_CULTIST, t)

dirvar = 4

def playMusic(num):
    global STOP_MUSIC
    if(num == 1):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sound/GameJamTribe.wav')
        pygame.mixer.music.play(0)
        pygame.time.set_timer(STOP_MUSIC, 6000)
    if(num == 2):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sound/SoylentLovesRobots.wav')
        pygame.mixer.music.play(0)
        pygame.time.set_timer(STOP_MUSIC, 7000)
    if(num == 3):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sound/GregorianGameJam.wav')
        pygame.mixer.music.play(0)
        pygame.time.set_timer(STOP_MUSIC, 7500)


while not quit:
    quit = pygame.event.get(pygame.QUIT)
    #if pygame.event.get(pygame.MOUSEBUTTONDOWN):
        #addCultist()
        #cultist.set_target(pygame.mouse.get_pos())

    if(score[1] >= victoryAmount and score[2] >= victoryAmount and score[3] >= victoryAmount) :
        s.fill((225,225,225))
        s.blit(monster, ((200,0)))
        label = myfont.render("The Elder Gods are satisfied!", 1, (155,95,55))
        s.blit(label, (250, 565))
        pygame.display.flip() # RENDER THE SCREEN
        c.tick(60) # END OF FRAME CALCULATIONS
        continue
    if score[4] >= 20 or score[0] <= 0:
        s.fill((225,225,225))
        s.blit(monster, ((200,0)))
        label = myfont.render("The Elder Gods are displeased!", 1, (155,95,55))
        s.blit(label, (250, 565))
        pygame.display.flip() # RENDER THE SCREEN
        c.tick(60) # END OF FRAME CALCULATIONS
        continue

    
    for e in pygame.event.get():
        if e.type == STOP_MUSIC:
            pygame.mixer.music.stop()
        if e.type == pygame.KEYDOWN:
            gamePaused == False;
            #print e.key
            if(e.key == 276): # right arrow
                moveToRoom(1)
                dirvar = 1
            if(e.key == 275): # down arrow
                moveToRoom(2)
                dirvar = 2
            if(e.key == 274): # left arrow
                moveToRoom(3)
                dirvar = 3
            if(e.key == 273): # up arrow
                moveToRoom(666)
                dirvar = 4
        if e.type == CREATE_CULTIST:
            t = t - 1

            if t < 250:
                t = 50
            pygame.time.set_timer(CREATE_CULTIST, t)
            addCultist()
    pygame.event.poll()
    # if(gamePaused == True) :
    #     continue

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
    s.blit(gate_1, (door1[0] - 16, door1[1]-20))
    s.blit(gate_2, (door2[0] - 16, door2[1]-20))
    s.blit(gate_3, (door3[0] - 16, door3[1]-20))

    for i in range(0, numCultists):
        cultists[i].draw(s)

    for a in assigned:
        a.draw(s)

    for b in bloodList:
        b.draw(s)

    if dirvar == 1:
        s.blit(goblin_left, ((300,430)))
    if dirvar == 2:
        s.blit(goblin_right, ((500,430)))
    if dirvar == 3:
        s.blit(goblin_down, ((410,430)))
    if dirvar == 4:
        s.blit(goblin_right, ((510,135)))


    # pygame.draw.rect(s, (255, 0 ,0), (door1[0]-doorSize[0]/2, door1[1]-doorSize[1]/2, doorSize[0], doorSize[1]), 5)
    # pygame.draw.rect(s, (0, 102 ,0), (door2[0]-doorSize[0]/2, door2[1]-doorSize[1]/2, doorSize[0], doorSize[1]), 5)
    # pygame.draw.rect(s, (0, 0 ,255), (door3[0]-doorSize[0]/2, door3[1]-doorSize[1]/2, doorSize[0], doorSize[1]), 5)
    # pygame.draw.rect(s, (0, 0 ,0), (POD[0]-PODSize[0]/2, POD[1]-PODSize[1]/2, PODSize[0], PODSize[1]), 5)

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
    
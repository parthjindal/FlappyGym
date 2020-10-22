
from itertools import cycle
import random
import sys
import time
import pygame
from pygame.locals import *
from constants import *

# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

class Bird():
    def __init__(self):
        self.playerx = 0
        self.playery = 0
        self.playerRot = 0
        self.playerVelY = 0
        self.playerVelRot = 0
        self.playerFlapAcc = 0
        self.playerMaxVelY = 0
        self.playerMinVelY = 0
        self.playerRotThr = 0
        self.playerFlapped = False
        self.score = 0
        self.upperPipes=[]
        self.lowerPipes=[]
        self.pipeVelX = 0


def initialize():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)

    # select random background sprites
    randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
    IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

    # select random player sprites
    randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
    IMAGES['player'] = (
        pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
        pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
        pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
    )

    # select random pipe sprites
    pipeindex = random.randint(0, len(PIPES_LIST) - 1)
    IMAGES['pipe'] = (
        pygame.transform.rotate(
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
        pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
    )

    # hismask for pipes
    HITMASKS['pipe'] = (
        getHitmask(IMAGES['pipe'][0]),
        getHitmask(IMAGES['pipe'][1]),
    )

    # hitmask for player
    HITMASKS['player'] = (
        getHitmask(IMAGES['player'][0]),
        getHitmask(IMAGES['player'][1]),
        getHitmask(IMAGES['player'][2]),
    )


def showWelcomeAnimation(bird):
    """Shows welcome screen animation of flappy bird"""
    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    bird.playerx = int(SCREENWIDTH * 0.2)
    bird.playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    basex = 0
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # player shm for up-down motion on welcome screen
    playerShmVals = {'val': 0, 'dir': 1}

    # draw sprites
    SCREEN.blit(IMAGES['background'], (0,0))
    SCREEN.blit(IMAGES['player'][0],
    (bird.playerx, bird.playery + playerShmVals['val']))
    SCREEN.blit(IMAGES['message'], (messagex, messagey))
    SCREEN.blit(IMAGES['base'], (basex, BASEY))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first flap sound and return values for mainGame
                SOUNDS['wing'].play()
                return {
                    'playery': bird.playery + playerShmVals['val'],
                    'basex': basex,
                    'playerIndexGen': playerIndexGen,
                }

    # adjust playery, playerIndex, basex
    if (loopIter + 1) % 5 == 0:
        playerIndex = 0
    loopIter = (loopIter + 1) % 30
    basex = 0
    playerShm(playerShmVals)

  

def mainGame(movementInfo,bird):
    bird.score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    bird.playerx, bird.playery = int(SCREENWIDTH * 0.2), movementInfo['playery']

    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    bird.upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    bird.lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    bird.pipeVelX = -4
    # player velocity, max velocity, downward accleration, accleration on flap
    bird.playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
    bird.playerMaxVelY =  5   # max vel along Y, max descend speed
    bird.playerMinVelY =  -8   # min vel along Y, max ascend speed
    bird.playerAccY    =   1   # players downward accleration
    bird.playerRot     =  45   # player's rotation
    bird.playerVelRot  =   3   # angular speed
    bird.playerRotThr  =  20   # rotation threshold
    bird.playerFlapAcc =  -4  # players speed on flapping
    bird.playerFlapped = False # True when player flaps


def execute(event,bird):
    upperPipes = bird.upperPipes
    lowerPipes = bird.lowerPipes

    if event == 0:
        bird.playerFlapped = False
    if event == 1:
        if bird.playery > -2 * IMAGES['player'][0].get_height():
            bird.playerVelY = bird.playerFlapAcc
            bird.playerFlapped = True
            SOUNDS['wing'].play()
    
    # check for score
    playerMidPos = bird.playerx + IMAGES['player'][0].get_width() / 2
    for pipe in bird.upperPipes:
        pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
        if pipeMidPos <= playerMidPos < pipeMidPos + 4:
            bird.score += 1
            SOUNDS['point'].play()

    basex=0

    # rotate the player
    if bird.playerRot > -90:
        bird.playerRot -= bird.playerVelRot

    # player's movement
    if bird.playerVelY < bird.playerMaxVelY and not bird.playerFlapped:
        bird.playerVelY += bird.playerAccY
    if bird.playerFlapped:
        bird.playerFlapped = False
        # more rotation to cover the threshold (calculated in visible rotation)
        bird.playerRot = 45

    playerHeight = IMAGES['player'][0].get_height()
    bird.playery += min(bird.playerVelY, BASEY - bird.playery - playerHeight)

    # move pipes to left
    for uPipe, lPipe in zip(bird.upperPipes, bird.lowerPipes):
        uPipe['x'] += bird.pipeVelX
        lPipe['x'] += bird.pipeVelX

    # add new pipe when first pipe is about to touch left of screen
    if 0 < upperPipes[0]['x'] < 5:
        newPipe = getRandomPipe()
        bird.upperPipes.append(newPipe[0])
        bird.lowerPipes.append(newPipe[1])

    # remove first pipe if its out of the screen
    if bird.upperPipes[0]['x'] <bird.playerx -IMAGES['pipe'][0].get_width():
        bird.upperPipes.pop(0)
        bird.lowerPipes.pop(0)
    # draw sprites
    SCREEN.blit(IMAGES['background'], (0,0))

    for uPipe, lPipe in zip(bird.upperPipes, bird.lowerPipes):
        SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
        SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

    SCREEN.blit(IMAGES['base'], (basex, BASEY))
    # print score so player overlaps the score
    showScore(bird.score)

    # Player rotation has a threshold
    visibleRot = bird.playerRotThr
    if bird.playerRot <= bird.playerRotThr:
        visibleRot = bird.playerRot
    
    playerSurface = pygame.transform.rotate(IMAGES['player'][0], visibleRot)
    SCREEN.blit(playerSurface, (bird.playerx, bird.playery))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def showGameOverScreen(crashInfo):
    """crashes the player down ans shows gameover image"""
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2
    playerRot = crashInfo['playerRot']
    playerVelRot = 7

    basex = crashInfo['basex']

    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    # play hit and die sounds
    SOUNDS['hit'].play()
    if not crashInfo['groundCrash']:
        SOUNDS['die'].play()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # player y shift
        if playery + playerHeight < BASEY - 1:
            playery += min(playerVelY, BASEY - playery - playerHeight)

        # player velocity change
        if playerVelY < 15:
            playerVelY += playerAccY

        # rotate only when it's a pipe crash
        if not crashInfo['groundCrash']:
            if playerRot > -90:
                playerRot -= playerVelRot

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        showScore(score)

        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx,playery))

        FPSCLOCK.tick(FPS)
        pygame.display.update()


def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
         playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask


# Game 1 Reaction Time Game, A letter shows up and you have to click the key
# on the keyboard

import pygame
import time
import random

pygame.init()

right = 0
wrong = 0
tries = 0
totalTime = 0

startfont = pygame.font.SysFont("monospace", 60)
myfont = pygame.font.SysFont("monospace", 150)
displayFont = pygame.font.SysFont("monospace", 30)

w_width = 1000
w_height = 600
win = pygame.display.set_mode((w_width,w_height))
win.fill((0,0,0))
pygame.display.update()


def update():
    global time1, totalTime
    pygame.draw.rect(win, (0,0,0), (0,0,w_width,100))
    totalTime = time.time() - time1
    label = displayFont.render('Time: ' + str(round(totalTime,2)),1,(255,255,255))
    win.blit(label,(10,10))
    label = displayFont.render('Remaining: ' + str(26 - tries),1,(255,255,255))
    win.blit(label, (w_width - 20 - label.get_width(),10))
    label = displayFont.render('Correct: ' + str(right),1,(0,255,0))
    win.blit(label, (w_width-38-label.get_width(),40))
    label = displayFont.render('Incorrect: ' + str(wrong),1,(255,0,0))
    win.blit(label, (w_width - 37 - label.get_width(),70))
    label = displayFont.render('+' + str(2.5*wrong) + 's', 1, (255,0,0))
    win.blit(label, (220, 10))
    pygame.display.update()

def showLetter():
    letter = generateKey()
    label = myfont.render(letter, 1, (255,255,255))
    win.blit(label, (random.randrange(100,w_width - 100 - label.get_width()), random.randrange(100,w_height-label.get_height())))
    pygame.display.update()
    return letter
    
def correct():
    global right
    right += 1

def incorrect():
    global wrong
    wrong += 1

def generateKey():
    r = random.randrange(0,26)
    return chr(65 + r)

def startCount():
    win.fill((0,0,0))
    label = myfont.render('3',1,(255,255,255))
    win.blit(label, (w_width/2 - label.get_width()/2,w_height/2-label.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)
    win.fill((0,0,0))
    label = myfont.render('2',1,(255,255,255))
    win.blit(label, (w_width/2 - label.get_width()/2,w_height/2-label.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)
    win.fill((0,0,0))
    label = myfont.render('1',1,(255,255,255))
    win.blit(label, (w_width/2 - label.get_width()/2,w_height/2-label.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)


def endScreen():
    global totalTime
    totalTime += 2.5 * wrong
    if tries == 26:
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                    pygame.quit()



def start():
    global time1, tries, right, wrong, totalTime

    play = True
    first = False
    time1 = 0
    while play:
        label = startfont.render('Press Any Key to Begin...', 1, (255,255,255))
        win.blit(label, (w_width/2 - label.get_width()/2,w_height/2-label.get_height()/2))
        pygame.display.update()
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                startCount()
                update()
                totalTime = 0
                tries = 0
                right = 0
                wrong = 0
                time1 = time.time()
                while tries < 26:
                    tries += 1
                    win.fill((0,0,0))
                    correctKey = showLetter()
                    gameLoop = True
                    while gameLoop:
                        first = True
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                gameLoop = False
                                tries = 100
                                play = False
                            if event.type == pygame.KEYDOWN:
                                pressed = pygame.key.get_pressed()
                                for i in range(len(pressed)):
                                    if pressed[i] == 1:
                                        usrPressed = pygame.key.name(i)

                                if usrPressed.lower() == correctKey.lower():
                                    correct()
                                else:
                                    incorrect()
                                gameLoop = False
                        update()
                endScreen()
    pygame.quit()


start()
